"""
P2 - Predictive AI Model
======================================================================
Watches raw sensor data written by the simulator (P1) at /sensors/{sectionId},
turns it into a 0-100 health score per track section, writes the score back
to /sections/{sectionId}/healthScore (the dashboard already reads this path
live via useRealtime("/sections", ...)), and auto-generates a maintenance
block request in /blockRequests when a section's health goes Critical.

WHAT P1 NEEDS TO WRITE for this to work (agree this with them):
/sensors/{sectionId} = {
    "vibration":   0-10   (higher = worse)
    "temperature": 0-100  (deg C, higher = worse)
    "axleLoad":    0-40   (tonnes, higher = worse)
}
Section IDs should match the ones already in the frontend's mock data:
BPL-ET, NGP-BPL, BSP-NGP, VSKP-BBS, MAS-GNT, ET-JBP, BBS-KUR, GNT-BZA

WHAT THIS SCRIPT WRITES:
/sections/{sectionId}/healthScore  -> int, 0-100   (dashboard reads this, updates on EVERY reading)
/alerts                            -> pushes a new Alert once a severity change holds for
                                       CONFIRM_STREAK readings in a row (avoids alert spam
                                       from a sensor jittering right on a threshold)
/blockRequests                     -> pushes a request for P3's optimizer to read, same
                                       debounce rule applies

This blends TWO things into the final score:
1. A rule-based weighted formula (compute_health_score) - transparent, easy
   to explain to judges.
2. An IsolationForest anomaly-detection model (ml_anomaly_score) trained by
   train_model.py - genuine unsupervised ML, flags readings that don't look
   like "normal" track behavior even if no single field crosses a hard limit.

SETUP — LOCAL TESTING (one-time):
1. Ask P4 (whoever owns the Firebase console) for a "service account key":
   Firebase console -> Project settings -> Service accounts -> Generate new
   private key. Save the downloaded file as serviceAccountKey.json in this
   same folder. Do NOT commit this file to git (it's a secret).
2. pip install -r requirements.txt
3. python train_model.py        (produces health_model.joblib, run once)
4. python health_scoring.py

SETUP — RENDER DEPLOYMENT:
Same convention as backend/firebase_init.py already uses in this repo:
set an environment variable FIREBASE_CREDENTIALS_JSON on Render, with the
ENTIRE contents of serviceAccountKey.json pasted in as the value. No local
file needed on Render — the script checks the env var first automatically.

TESTING WITHOUT P1's SIMULATOR READY YET:
Open the Firebase console -> Realtime Database, and manually add data at
/sensors/BSP-NGP with e.g. {"vibration": 8, "temperature": 70, "axleLoad": 30}.
You should see this script print a low score and fire an alert + block request.
"""

import os
import time
import uuid
import json
from datetime import datetime

import joblib
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

# ---- ML MODEL ----------------------------------------------------------------
# Resolved relative to THIS file, not the current working directory, so it
# works whether you run it from ai-model/ or from the repo root.
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_model.joblib")

try:
    _bundle = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise SystemExit(
        f"Could not find {MODEL_PATH}\n"
        "Run 'python train_model.py' first to generate it, then try again."
    )

ML_MODEL = _bundle["model"]
FEATURE_ORDER = _bundle["feature_order"]

# Blend weight: how much the ML anomaly score influences the final number,
# vs. the plain rule-based formula. 0.5 = equal say. Raise this once you
# trust the model more (e.g. after retraining on real sensor history).
ML_BLEND_WEIGHT = 0.5


def ml_anomaly_score(reading: dict) -> int:
    """
    Runs the trained IsolationForest on one reading and returns a 0-100
    score in the SAME direction as compute_health_score (higher = healthier).
    """
    features = np.array([[reading.get(f, 0) for f in FEATURE_ORDER]])
    raw = ML_MODEL.decision_function(features)[0]   # roughly -0.5..0.5
    # Squash to 0-100. Clamping first avoids wild swings from outlier inputs.
    clamped = max(-0.5, min(0.5, raw))
    return round((clamped + 0.5) * 100)

# ---- CONFIG ----------------------------------------------------------------

SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "serviceAccountKey.json")
DATABASE_URL = "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app"

# Weighted scoring formula. Weights must sum to 1. Tune these once you see
# real-ish numbers from P1's simulator.
WEIGHTS = {"vibration": 0.4, "temperature": 0.3, "axleLoad": 0.3}
MAX_VALUES = {"vibration": 10, "temperature": 100, "axleLoad": 40}

CRITICAL_THRESHOLD = 45   # below this -> Critical, fires a block request
WARNING_THRESHOLD = 70    # below this (and >= critical) -> Warning

# Section -> department, needed so alerts/requests match the frontend's types.
# Extend/edit this to match whatever P1 and P4 actually agree on.
SECTION_DEPT = {
    "BPL-ET": "TDMS", "NGP-BPL": "SMMS", "BSP-NGP": "TMS", "VSKP-BBS": "TMS",
    "MAS-GNT": "TMS", "ET-JBP": "TMS", "BBS-KUR": "SMMS", "GNT-BZA": "SMMS",
}

# ---- FIREBASE SETUP ----------------------------------------------------------

def init_firebase():
    """
    Matches the convention already used in backend/firebase_init.py by your
    teammate: on Render, set an env var FIREBASE_CREDENTIALS_JSON containing
    the ENTIRE contents of serviceAccountKey.json as one string. Locally, just
    keep using the serviceAccountKey.json file next to this script — no env
    var needed for that case.
    """
    env_creds = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if env_creds:
        try:
            cred_dict = json.loads(env_creds)
        except json.JSONDecodeError as e:
            raise SystemExit(
                f"FIREBASE_CREDENTIALS_JSON is set but isn't valid JSON: {e}\n"
                "Paste the ENTIRE contents of serviceAccountKey.json as the value, unmodified."
            )
        cred = credentials.Certificate(cred_dict)
    elif os.path.exists(SERVICE_ACCOUNT_PATH):
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    else:
        raise SystemExit(
            f"No credentials found. Either:\n"
            f"  - set env var FIREBASE_CREDENTIALS_JSON (for Render), or\n"
            f"  - place serviceAccountKey.json at {SERVICE_ACCOUNT_PATH} (for local testing)\n"
            "Get it from Firebase console -> Project settings -> Service accounts -> "
            "Generate new private key."
        )

    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})


# ---- SCORING -----------------------------------------------------------------

def sanitize_reading(reading: dict) -> dict:
    """
    Coerces every expected field to a float, defaulting to 0 for anything
    missing, non-numeric, or None. Sensor data from the field (or a flaky
    simulator) will eventually send something malformed — this makes sure
    that never takes down the whole listener.
    """
    clean = {}
    for field in ("vibration", "temperature", "axleLoad"):
        raw = reading.get(field, 0)
        try:
            value = float(raw)
            if value < 0 or value != value:  # negative or NaN
                value = 0.0
        except (TypeError, ValueError):
            print(f"  [warn] bad value for '{field}': {raw!r} -> using 0")
            value = 0.0
        clean[field] = value
    return clean


def compute_health_score(reading: dict) -> int:
    """Turn raw sensor values into one 0-100 health score. Higher = healthier."""
    penalty = 0.0
    for field, weight in WEIGHTS.items():
        raw = reading.get(field, 0)
        capped = min(raw, MAX_VALUES[field])
        normalized = capped / MAX_VALUES[field]   # 0-1, higher = worse
        penalty += weight * normalized
    score = 100 - (penalty * 100)
    return max(0, min(100, round(score)))


def severity_for(score: int) -> str:
    if score < CRITICAL_THRESHOLD:
        return "Critical"
    if score < WARNING_THRESHOLD:
        return "Warning"
    return "Normal"


# ---- FIREBASE WRITES ----------------------------------------------------------

def update_section_health(section_id: str, score: int):
    db.reference(f"/sections/{section_id}/healthScore").set(score)


def push_alert(section_id: str, score: int, severity: str):
    dept = SECTION_DEPT.get(section_id, "TMS")
    alert = {
        "id": f"AL-{uuid.uuid4().hex[:6].upper()}",
        "section": section_id,
        "dept": dept,
        "message": f"Health score changed to {score} ({severity})",
        "severity": severity,
        "time": datetime.now().strftime("%H:%M"),
        "acknowledged": False,
    }
    db.reference("/alerts").push(alert)


def push_block_request(section_id: str, score: int):
    """Handoff node for P3's optimizer to read and turn into a real schedule block."""
    dept = SECTION_DEPT.get(section_id, "TMS")
    request = {
        "id": f"REQ-{uuid.uuid4().hex[:6].upper()}",
        "section": section_id,
        "dept": dept,
        "reason": f"Health score critical ({score})",
        "requestedAt": datetime.now().isoformat(),
        "status": "Pending",
    }
    db.reference("/blockRequests").push(request)


# ---- LISTENER LOGIC -----------------------------------------------------------

# Remembers each section's last CONFIRMED severity so we only fire a new
# alert/request once a change has held for CONFIRM_STREAK readings in a row
# — not on every single noisy reading. Prevents alert spam when a sensor
# value sits right on a threshold and jitters back and forth.
last_severity: dict[str, str] = {}
pending_severity: dict[str, str] = {}
pending_streak: dict[str, int] = {}
CONFIRM_STREAK = 2  # how many readings in a row before a severity change counts


def score_and_publish(section_id: str, reading: dict):
    """Scores one section's reading and writes score/alert/request as needed."""
    reading = sanitize_reading(reading)

    rule_score = compute_health_score(reading)
    ml_score = ml_anomaly_score(reading)
    score = round((1 - ML_BLEND_WEIGHT) * rule_score + ML_BLEND_WEIGHT * ml_score)
    severity = severity_for(score)

    print(f"[{section_id}] rule={rule_score} ml={ml_score} final={score} severity={severity}")

    # The live score updates on every reading, unfiltered — the dashboard
    # should always show the current number, even before an alert confirms.
    update_section_health(section_id, score)

    confirmed = last_severity.get(section_id)
    if severity == confirmed:
        # Back to the confirmed state — clear any pending change in progress.
        pending_severity[section_id] = None
        pending_streak[section_id] = 0
        return

    if pending_severity.get(section_id) == severity:
        pending_streak[section_id] = pending_streak.get(section_id, 0) + 1
    else:
        pending_severity[section_id] = severity
        pending_streak[section_id] = 1

    if pending_streak[section_id] >= CONFIRM_STREAK:
        push_alert(section_id, score, severity)
        if severity == "Critical":
            push_block_request(section_id, score)
        last_severity[section_id] = severity
        pending_severity[section_id] = None
        pending_streak[section_id] = 0


def handle_sensor_update(event):
    """
    Called automatically by Firebase whenever /sensors changes.

    IMPORTANT: the very first event after listen() is called is always a
    full snapshot of the ENTIRE /sensors node (path "/", data = a dict of
    every section at once) — not a single section. Every event after that
    is a per-section update (path "/{sectionId}", data = one reading). Both
    shapes are handled below so nothing gets silently skipped on startup.

    The whole body is wrapped in try/except: this callback runs on Firebase's
    own background thread, so an uncaught exception here can silently kill
    the listener with no crash visible on your terminal — the dashboard would
    just stop updating mid-demo with no obvious reason why. One bad event
    should never be able to take down every future update.
    """
    try:
        section_id = event.path.strip("/")
        reading = event.data

        if not section_id:
            # Full snapshot (startup, or the whole /sensors node was replaced/wiped).
            if isinstance(reading, dict):
                for child_id, child_reading in reading.items():
                    if isinstance(child_reading, dict):
                        score_and_publish(child_id, child_reading)
            return

        if not isinstance(reading, dict):
            return  # a single section was deleted/nulled out — nothing to score

        score_and_publish(section_id, reading)

    except Exception as e:
        print(f"  [error] failed to process update at {event.path!r}: {e!r} — skipping, still listening")


def init_firebase_with_retry():
    """
    Retries Firebase initialization on transient errors (network blips, DNS
    hiccups, Firebase briefly unreachable). Does NOT retry a missing/invalid
    service account key — that's a real configuration problem, not a
    transient one, so it fails fast with a clear message instead of looping
    forever on something retrying can't fix.
    """
    delay = 2
    while True:
        try:
            init_firebase()
            print("Firebase initialized.")
            return
        except SystemExit:
            raise  # missing serviceAccountKey.json - not something to retry
        except Exception as e:
            print(f"  [startup error] {e!r} - retrying in {delay}s...")
            time.sleep(delay)
            delay = min(delay * 2, 30)


def attach_listener_with_retry():
    """Same idea as above, but for actually attaching the /sensors listener."""
    delay = 2
    while True:
        try:
            db.reference("/sensors").listen(handle_sensor_update)
            print("Connected. Listening on /sensors for live updates... (Ctrl+C to stop)")
            return
        except Exception as e:
            print(f"  [connection error] {e!r} - retrying in {delay}s...")
            time.sleep(delay)
            delay = min(delay * 2, 30)


def main():
    init_firebase_with_retry()
    attach_listener_with_retry()

    # listen() runs in its own background thread, so keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
