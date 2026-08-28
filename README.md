# Rail Block Maestro

Build a React + TypeScript + Vite app called "ABPS — Rail Block Planning System". Dark navy theme (#0a0f1e bg, #111827 cards). Use shadcn/ui, Tailwind, Recharts, react-leaflet, React Router v6.

Firebase (hardcode this config):

ts


import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';
export const db = getDatabase(initializeApp({
  apiKey: "@secret:GOOGLE_API_KEY ",
  authDomain: "train-train-80645.firebaseapp.com",
  databaseURL: "https://train-train-80645-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "train-train-80645",
  storageBucket: "train-train-80645.firebasestorage.app",
  messagingSenderId: "422158434914",
  appId: "1:422158434914:web:034528c085b88324b5073b"
}));
Use onValue() listeners. Fall back to mock data if Firebase empty.

Colors: TMS=#3b82f6, TDMS=#f97316, SMMS=#a855f7, Critical=#ef4444, Warning=#f59e0b

6 pages with dark collapsible sidebar:

/ Dashboard — 4 KPI cards (Asset Availability%, Critical Defects, Blocks Today, AI Score), Leaflet map with Indian railway sections colored by health score (green/yellow/orange/red), mini Gantt for today, live alerts feed with acknowledge button

/gantt Planner — Full Gantt chart, filter by dept/status/date range, click block opens modal with details + Approve/Reject buttons

/defects Defects — Table with filters, tabs: All/Overdue/Critical/AI Prioritized (sorted by urgency score 0-100)

/analytics Analytics — Health score cards per section, line chart (planned vs actual blocks), stacked bar chart (dept activity by day)

/corridor Corridor — Space-time train path diagram, block window availability table with AI-recommended slots marked ⭐

/settings Settings — Firebase connection status, demo mode toggle, threshold sliders

Mock data: 8 sections (BPL-ET, NGP-BPL, BSP-NGP, VSKP-BBS, MAS-GNT), 15 defects, 10 blocks, trains 12951/12301/12627, 5 alerts.

vercel.json: {"rewrites":[{"source":"/(.*)","destination":"/index.html"}]}

Build Dashboard first, then remaining pages. Keep TypeScript types simple to avoid errors.

Background: Railway maintenance for fixed infrastructure of Engineering, Traction Distribution, and Signal & Telecommunication departments is currently planned independently. Each department requests maintenance blocks/disconnections via the BDMS system. This planning process is decentralized and manual. This often leads to inefficient block utilization, poor coordination, and suboptimal scheduling,which may reduce asset availability and impact train operations. Detailed Description: Maintenance data-such as defects and overdue tasksâ€”is maintained separately in systems like Track Management System (TMS), Signalling Maintenance & Management System (SMMS), and Traction Distribution Management System (TDMS). Meanwhile, the Control Office Application (COA) manages block corridor availability. Without integration and coordinated scheduling, maintenance blocks/disconnections are not optimally planned, resulting in asset downtime and reduced availability of fixed infrastructure for train operation.Your task is to develop an Automatic Block Planning system that integrates maintenance, defects and corridor data to generate optimized block schedules. The system should prioritize maintenance activities to minimize asset downtime and maximize the availability of critical infrastructure, ensuring uninterrupted train operations. Expected Solution: Participants should build an Al system that includes:

1. Integration of maintenance data (defects, overdue maintenance) from TMS, SMMS, and TDMS with corridor block and block availability as per the Train Time Table and the goods trains forecast from the Control Office.

2. Uses AI/ML algorithms to prioritize and schedule maintenance tasks based on criticality, urgency, and impact on asset availability.

3. Optimize block scheduling to maximize asset uptime by minimizing downtime and efficiently coordinating multi-department activities.

4. Provides block plans over multiple time horizons-weekly and monthlyâ€”to support both short-term and long-term maintenance.

The solution should transform current decentralized and manual block planning into a data-driven, coordinated process that maximizes asset availability, improves safety, and supports reliable train operations.

Here is the updated data pipeline architecture using **Firebase** as the real-time data sync, database, and event engine.

By replacing WebSocket/Redis/PostgreSQL with **Firebase Realtime Database (or Cloud Firestore)**, your backend becomes simpler, as Firebase handles real-time data streaming to the React dashboard automatically out of the box.

---

```

                                  [ REAL-TIME SIMULATOR ]

                               (Python Synthetic Generator)

                                             │

             ┌───────────────────────────────┴───────────────────────────────┐

             │                                                               │

     [ Track Sensors ]                                            [ Train Telemetry ]

 (Vibration, Temp, Axle Load)                                  (Train ID, Speed, Section)

             │                                                               │

             └───────────────────────────────┬───────────────────────────────┘

                                             │

                                             ▼ Direct Firebase Admin SDK Writes

                   ┌───────────────────────────────────────────────────┐

                   │           FIREBASE REALTIME DATABASE              │

                   │                (Cloud Data Hub)                   │

                   │                                                   │

                   │  • /telemetry (Train positions & speeds)          │

                   │  • /sensors   (Track health logs)                 │

                   │  • /schedule  (Active blocks & timetables)        │

                   └───────┬───────────────────────────────────┬───────┘

                           │                                   │

       Listens for updates │                                   │ Real-time Firebase SDK

       via Cloud Functions │                                   │ listener (Auto-Sync)

       or Python Listener  │                                   │

                           ▼                                   ▼

          ┌───────────────────────────────────┐  ┌───────────────────────────┐

          │      AI OPTIMIZATION ENGINE       │  │    FRONTEND DASHBOARD     │

          │              (Python)             │  │       (React / UI)        │

          └────────────────┬──────────────────┘  └─────────────▲─────────────┘

                           │                                   │

             ┌─────────────┴─────────────┐                     │

             │                           │                     │

             ▼                           ▼                     │

┌───────────────────────────┐ ┌───────────────────────────┐    │

│ 1. Predictive ML Model    │ │ 2. Constraint Optimizer   │    │

│  (Asset Health Scoring)   │ │    (Google OR-Tools)      │    │

└────────────┬──────────────┘ └────────────┬──────────────┘    │

             │                             │                   │

             │ Health Score < Threshold    │                   │

             └─► Auto-Generates Block ─────┘                   │

                 Request                                       │

                                           │                   │

                                           ▼ Writes Optimized  │

                                             Schedule Back     │

                                           ┌───────────────────┴───────────┐

                                           │ Overwrites /schedule node     │

                                           │ in Firebase Realtime Database │

                                           └───────────────────────────────┘

```

---

### What Changes with Firebase in the Pipeline?

1. **No Custom WebSocket Server Needed:**

* **Before:** You needed FastAPI/Node.js to handle WebSocket handshakes and stream data to the UI.

* **Now:** Firebase handles live streaming natively. When Python updates a node in Firebase, all connected React web apps update instantly via the `onValue()` listener.

2. **Unified Data & Caching Layer:**

* **Before:** Redis was used for live in-memory state and PostgreSQL/MongoDB for persistence.

* **Now:** **Firebase Realtime Database** acts as both your real-time state engine and persistent storage.

3. **Data Flow Lifecycle:**

* **Step 1 (Simulator):** Python simulator uses `firebase-admin` SDK to write telemetry and sensor readings directly to Firebase nodes (e.g., `db.reference('/telemetry').update(...)`).

* **Step 2 (AI Engine):** Your Python AI script runs a background listener on Firebase nodes. When new sensor data arrives, the **Predictive ML Model** scores asset health. If maintenance is needed, it triggers the **Google OR-Tools Optimizer**.

* **Step 3 (Re-optimization & Output):** The optimizer calculates the optimal block schedule and writes the result back to the `/schedule` node in Firebase.

* **Step 4 (UI Update):** The React frontend's Firebase listener detects changes on `/schedule` and instantly re-renders the Gantt chart and track map without needing a page refresh or API polling.

---

### Updated Team Ownership (Adjusted for Firebase)

| Team Member | Module Ownership | Core Deliverables |

| --- | --- | --- |

| **Person 1** | **Simulation Layer** | Python event-generator script writing directly to Firebase nodes. |

| **Person 2** | **Predictive AI Model** | Python ML script listening to Firebase `/sensors`, computing health scores, and auto-flagging blocks. |

| **Person 3** | **Constraint Optimizer** | Google OR-Tools CP-SAT solver script reading timetables from Firebase and writing back recalculated schedules. |

| **Person 4** | **Firebase & Database Config** | Firebase project setup, security rules, data structure schemas, and backend helper scripts. |

| **Person 5** | **Frontend UI / Map** | React Gantt view & Map subscribing to Firebase realtime snapshot hooks. |

| **Person 6** | **Integration & Pitch** | End-to-end demo flow testing, slides, problem-statement alignment. |

build only front end

This project was built with [Lovable](https://lovable.dev).

**Live app**: https://track-harmony-view.lovable.app

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/5960dd9a-5da0-4522-b5b4-05d55d237b00).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
