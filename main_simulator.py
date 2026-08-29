import json
import os
import random
import sys
import time
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# =====================================================================
# 1. FILE PATHS & FIREBASE INITIALIZATION
# =====================================================================
KEY_PATH = "firebase_key.json"
CSV_PATH = "train_schedule.csv"
JSON_PATH = "defects.json"

# Verify required files exist before running
for file_path in [KEY_PATH, CSV_PATH, JSON_PATH]:
    if not os.path.exists(file_path):
        print(f"❌ Error: Required file '{file_path}' not found in directory.")
        sys.exit(1)

print("🔑 Initializing Firebase Admin SDK...")
try:
    cred = credentials.Certificate(KEY_PATH)

    # Automatically extract database URL from firebase_key.json if possible,
    # or replace with your exact Realtime Database URL string below
    # Hardcode your exact regional Firebase Realtime Database URL
    FIREBASE_DB_URL = (
        "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app"
    )
    firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})
    print(f"✅ Successfully connected to Firebase ({FIREBASE_DB_URL}).")
except Exception as e:
    print(f"❌ Firebase connection failed: {e}")
    sys.exit(1)

# Realtime Database node references
telemetry_node = db.reference("telemetry")
sensors_node = db.reference("sensors")
system_status_node = db.reference("system_status")

# =====================================================================
# 2. LOAD LOCAL DATASETS (WITH ROBUST SCOPING & FALLBACKS)
# =====================================================================
print("📊 Loading datasets...")

# --- A. Load Kaggle CSV Schedule ---
active_schedules = []
try:
    schedule_df = pd.read_csv(CSV_PATH)
    
    # Standardize column names (lowercase & remove whitespace)
    schedule_df.columns = schedule_df.columns.str.strip().str.lower()
    
    # Auto-detect train identifier column
    train_col = None
    for col in ['train_number', 'train_no', 'trainno', 'train_id', 'number']:
        if col in schedule_df.columns:
            train_col = col
            break

    if train_col:
        unique_trains = schedule_df[train_col].unique()[:8]
        active_schedules = schedule_df[schedule_df[train_col].isin(unique_trains)].to_dict(orient="records")
        print(f"✅ Loaded timetable for {len(unique_trains)} active trains from CSV.")
    else:
        active_schedules = schedule_df.head(10).to_dict(orient="records")
        print(f"✅ Loaded {len(active_schedules)} schedule records from CSV.")

except Exception as e:
    print(f"❌ Failed to parse '{CSV_PATH}': {e}")
    sys.exit(1)


# --- B. Load Defect JSON Logs ---
sensor_assets = []
try:
    with open(JSON_PATH, "r") as f:
        defects_data = json.load(f)

    if isinstance(defects_data, dict):
        sensor_assets = defects_data.get("defects", [])
    elif isinstance(defects_data, list):
        sensor_assets = defects_data

    print(f"✅ Loaded {len(sensor_assets)} asset defect records from JSON.")

except Exception as e:
    print(f"⚠️ Warning: Failed to parse '{JSON_PATH}': {e}")
    print("🔄 Initializing default fallback sensor assets...")
    
# Fallback safety check to guarantee sensor_assets is never empty
if not sensor_assets:
    sensor_assets = [
        {
            "asset_id": "TRACK_ENG_101",
            "department": "Engineering",
            "location": "SEC-DELHI-KM42",
            "defect_type": "Rail Micro-Fracture",
            "vibration_hz": 3.5,
            "urgency": "HIGH"
        },
        {
            "asset_id": "OHE_TRAC_204",
            "department": "Traction_OHE",
            "location": "SEC-AGRA-KM18",
            "defect_type": "Wire Tension Drop",
            "vibration_hz": 4.1,
            "urgency": "MEDIUM"
        }
    ]

# =====================================================================
# 3. SIMULATION LOOP ENGINE
# =====================================================================
def run_rail_grid_simulation():
    print("\n🚀 RAIL-GRID SIMULATOR LIVE — Streaming to Firebase & Vercel Dashboard...\n")
    step = 0

    while True:
        step += 1
        current_time_str = time.strftime("%H:%M:%S")

        # -------------------------------------------------------------
        # A. TRAIN TELEMETRY & ROUTE DELAYS
        # -------------------------------------------------------------
        train_updates = {}

        for idx, row in enumerate(active_schedules):
            # Safe key lookups supporting multiple dataset formats
            train_id = str(row.get("train_number", row.get("train_no", row.get("train_id", 12951 + idx))))
            station = str(row.get("station_code", row.get("station", f"SEC_STN_{idx}")))
            sched_arr = str(row.get("arrival", row.get("arrival_time", row.get("scheduled_arrival", "12:00"))))
            train_name = str(row.get("train_name", row.get("name", f"Express {train_id}")))

            # Inject realistic dynamic delay fluctuations
            base_delay = (idx * 4 + step * 2) % 40
            is_incident = random.random() < 0.12  # 12% chance of sudden signal hold
            delay_mins = base_delay + (15 if is_incident else 0)

            status = "ON_TIME"
            if delay_mins > 20:
                status = "CRITICAL_DELAY"
            elif delay_mins > 5:
                status = "MINOR_DELAY"

            train_payload = {
                "train_id": train_id,
                "train_name": train_name,
                "current_station": station,
                "scheduled_arrival": sched_arr,
                "delay_mins": delay_mins,
                "status": status,
                "speed_kmh": 0 if status == "CRITICAL_DELAY" else random.randint(60, 110),
                "last_ping": current_time_str
            }

            train_updates[train_id] = train_payload

        # Push batch update to Firebase /telemetry
        telemetry_node.update(train_updates)

        # -------------------------------------------------------------
        # B. TRACK SENSOR DEGRADATION & DEFECT LOGS
        # -------------------------------------------------------------
        sensor_updates = {}

        for asset in sensor_assets:
            asset_id = str(asset.get("asset_id", "AST_UNK"))
            dept = str(asset.get("department", "Engineering"))

            # Fluctuate sensor vibration readings dynamically
            base_vibration = float(asset.get("vibration_hz", 3.5))
            vibration_spike = round(base_vibration + random.uniform(-0.4, 1.6), 2)

            # Calculate asset health score based on strain
            health_score = max(10, min(100, int(100 - (vibration_spike * 9))))
            block_required = health_score < 45 or asset.get("urgency", "").upper() == "HIGH"

            sensor_payload = {
                "asset_id": asset_id,
                "department": dept,
                "location_section": asset.get("location", "SEC-A-B"),
                "defect_type": asset.get("defect_type", "General Wear"),
                "vibration_hz": vibration_spike,
                "health_score": health_score,
                "block_required": block_required,
                "recommended_block_mins": 45 if block_required else 0,
                "last_updated": current_time_str
            }

            sensor_updates[asset_id] = sensor_payload

        # Push batch update to Firebase /sensors
        sensors_node.update(sensor_updates)

        # -------------------------------------------------------------
        # C. GLOBAL HEARTBEAT & SYSTEM STATUS
        # -------------------------------------------------------------
        system_status_node.set({
            "active": True,
            "heartbeat": current_time_str,
            "step_count": step,
            "active_trains_count": len(train_updates),
            "flagged_defects_count": sum(1 for s in sensor_updates.values() if s["block_required"])
        })

        print(f"[{current_time_str}] Step #{step} | Synced {len(train_updates)} Trains & {len(sensor_updates)} Sensor Assets to Firebase.")

        # Stream update frame every 3 seconds
        time.sleep(3)

if __name__ == "__main__":
    try:
        run_rail_grid_simulation()
    except KeyboardInterrupt:
        print("\n⛔ Simulation paused by user.")
        system_status_node.update({"active": False})
        sys.exit(0)