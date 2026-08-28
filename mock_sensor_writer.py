"""
Mock Sensor Writer (for testing health_scoring.py only)
======================================================================
This is NOT P1's real simulator. It's a throwaway script so you (P2) can
test your health-scoring logic end-to-end right now, without waiting for
P1's actual simulator to be ready.

It writes fake sensor readings to /sensors/{sectionId} every few seconds,
occasionally spiking one section into "bad" territory so you can watch
health_scoring.py react: score drops -> alert fires -> block request fires.

SETUP: same serviceAccountKey.json as health_scoring.py, same folder.
RUN THIS IN A SEPARATE TERMINAL while health_scoring.py is also running.

  python mock_sensor_writer.py

Delete this file once P1's real simulator is ready — don't demo with it.
"""

import random
import time

import firebase_admin
from firebase_admin import credentials, db

SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"
DATABASE_URL = "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app"

SECTION_IDS = [
    "BPL-ET", "NGP-BPL", "BSP-NGP", "VSKP-BBS",
    "MAS-GNT", "ET-JBP", "BBS-KUR", "GNT-BZA",
]


def init_firebase():
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})


def normal_reading() -> dict:
    """Healthy-ish random values."""
    return {
        "vibration": round(random.uniform(0.5, 3.5), 2),
        "temperature": round(random.uniform(20, 45), 1),
        "axleLoad": round(random.uniform(10, 22), 1),
    }


def bad_reading() -> dict:
    """A deliberately bad reading, useful for demoing the AI trigger live."""
    return {
        "vibration": round(random.uniform(7, 10), 2),
        "temperature": round(random.uniform(70, 95), 1),
        "axleLoad": round(random.uniform(28, 38), 1),
    }


def main():
    init_firebase()
    print("Writing mock sensor data every 4s. Ctrl+C to stop.")
    print("Every ~8th tick, one random section gets a deliberate spike.")

    tick = 0
    while True:
        tick += 1
        for section_id in SECTION_IDS:
            db.reference(f"/sensors/{section_id}").set(normal_reading())

        if tick % 8 == 0:
            spiked_section = random.choice(SECTION_IDS)
            print(f"  -> spiking {spiked_section}")
            db.reference(f"/sensors/{spiked_section}").set(bad_reading())

        time.sleep(4)


if __name__ == "__main__":
    main()
