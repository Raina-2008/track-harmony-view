import { useEffect, useState } from "react";
import { ref, onValue } from "firebase/database";
import { getDb } from "@/lib/firebase";

export type ConnState = "connecting" | "live" | "mock";

/**
 * Subscribes to a Firebase Realtime Database path with onValue().
 * Falls back to the provided mock data when Firebase is unavailable or empty.
 */
export function useRealtime<T>(path: string, fallback: T) {
  const [data, setData] = useState<T>(fallback);
  const [state, setState] = useState<ConnState>("connecting");

  useEffect(() => {
    const db = getDb();
    if (!db) {
      setData(fallback);
      setState("mock");
      return;
    }
    const unsub = onValue(
      ref(db, path),
      (snap) => {
        const value = snap.val();
        if (value == null || (Array.isArray(value) && value.length === 0)) {
          setData(fallback);
          setState("mock");
          return;
        }
        setData((Array.isArray(fallback) ? Object.values(value) : value) as T);
        setState("live");
      },
      () => {
        setData(fallback);
        setState("mock");
      },
    );
    return () => unsub();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [path]);

  return { data, state } as const;
}
