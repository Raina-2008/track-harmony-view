import time
import random
import threading
from flask import Flask
from firebase_init import get_db

db = get_db()
app = Flask(__name__)

def tick():
    new_health = random.randint(35, 95)
    new_availability = round(random.uniform(85, 99), 1)
    db.reference("/sections/BPL-ET").update({
        "healthScore": new_health,
        "availability": new_availability
    })
    print("Updated BPL-ET health:", new_health)

def background_loop():
    while True:
        tick()
        time.sleep(5)

@app.route("/")
def home():
    return "Simulator is running."

if __name__ == "__main__":
    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=10000)