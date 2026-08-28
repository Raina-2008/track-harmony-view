import { initializeApp, getApps, type FirebaseApp } from "firebase/app";
import { getDatabase, type Database } from "firebase/database";

export const firebaseConfig = {
  apiKey: import.meta.env["VITE_FIREBASE_API_KEY"] ?? "",
  authDomain: "train-train-80645.firebaseapp.com",
  databaseURL:
    "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "train-train-80645",
  storageBucket: "train-train-80645.firebasestorage.app",
  messagingSenderId: "422158434914",
  appId: "1:422158434914:web:034528c085b88324b5073b",
};

export const isFirebaseConfigured = () => Boolean(firebaseConfig.apiKey);

let app: FirebaseApp | null = null;
let database: Database | null = null;

/** Lazily create the Realtime Database handle (browser only). */
export function getDb(): Database | null {
  if (typeof window === "undefined") return null;
  if (!isFirebaseConfigured()) return null;
  try {
    if (!app) app = getApps()[0] ?? initializeApp(firebaseConfig);
    if (!database) database = getDatabase(app);
    return database;
  } catch {
    return null;
  }
}
