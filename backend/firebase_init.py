import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app"
})

def get_db():
    return db