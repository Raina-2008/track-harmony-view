import os
import json
import firebase_admin
from firebase_admin import credentials, db

if os.environ.get("FIREBASE_CREDENTIALS_JSON"):
    cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def get_db():
    return db