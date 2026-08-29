from firebase_init import get_db

db = get_db()

sections = {
    "BPL-ET": {"id": "BPL-ET", "name": "Bhopal - Itarsi", "zone": "WCR", "healthScore": 62, "availability": 91.4, "from": [23.2599, 77.4126], "to": [22.6142, 77.7625], "openDefects": 4},
    "NGP-BPL": {"id": "NGP-BPL", "name": "Nagpur - Bhopal", "zone": "CR", "healthScore": 84, "availability": 96.2, "from": [21.1458, 79.0882], "to": [23.2599, 77.4126], "openDefects": 2},
    "BSP-NGP": {"id": "BSP-NGP", "name": "Bilaspur - Nagpur", "zone": "SECR", "healthScore": 41, "availability": 87.1, "from": [22.0797, 82.1409], "to": [21.1458, 79.0882], "openDefects": 5},
    "VSKP-BBS": {"id": "VSKP-BBS", "name": "Visakhapatnam - Bhubaneswar", "zone": "ECoR", "healthScore": 73, "availability": 93.8, "from": [17.6868, 83.2185], "to": [20.2961, 85.8245], "openDefects": 3},
    "MAS-GNT": {"id": "MAS-GNT", "name": "Chennai - Guntur", "zone": "SCR", "healthScore": 55, "availability": 89.6, "from": [13.0827, 80.2707], "to": [16.3067, 80.4365], "openDefects": 4},
    "ET-JBP": {"id": "ET-JBP", "name": "Itarsi - Jabalpur", "zone": "WCR", "healthScore": 91, "availability": 97.9, "from": [22.6142, 77.7625], "to": [23.1815, 79.9864], "openDefects": 1},
    "BBS-KUR": {"id": "BBS-KUR", "name": "Bhubaneswar - Khurda Road", "zone": "ECoR", "healthScore": 78, "availability": 95.1, "from": [20.2961, 85.8245], "to": [20.1809, 85.6203], "openDefects": 2},
    "GNT-BZA": {"id": "GNT-BZA", "name": "Guntur - Vijayawada", "zone": "SCR", "healthScore": 34, "availability": 84.3, "from": [16.3067, 80.4365], "to": [16.5062, 80.648], "openDefects": 6}
}
db.reference("/sections").set(sections)

defects = {
    "TMS-1041": {"id": "TMS-1041", "section": "BSP-NGP", "dept": "TMS", "description": "Rail fracture risk - high vibration at KM 412/3", "severity": "Critical", "reportedOn": "2026-08-21", "dueOn": "2026-08-26", "overdue": True, "urgencyScore": 96, "status": "Open"},
    "SMMS-2210": {"id": "SMMS-2210", "section": "GNT-BZA", "dept": "SMMS", "description": "Point machine 34B intermittent detection failure", "severity": "Critical", "reportedOn": "2026-08-23", "dueOn": "2026-08-27", "overdue": True, "urgencyScore": 93, "status": "Assigned"},
    "TDMS-3155": {"id": "TDMS-3155", "section": "BPL-ET", "dept": "TDMS", "description": "OHE contact wire wear beyond 20% at KM 88", "severity": "Critical", "reportedOn": "2026-08-24", "dueOn": "2026-08-29", "overdue": False, "urgencyScore": 88, "status": "Open"},
    "TMS-1045": {"id": "TMS-1045", "section": "MAS-GNT", "dept": "TMS", "description": "Ballast deficiency over 1.2 km stretch", "severity": "Warning", "reportedOn": "2026-08-19", "dueOn": "2026-08-25", "overdue": True, "urgencyScore": 81, "status": "Open"},
    "SMMS-2213": {"id": "SMMS-2213", "section": "BSP-NGP", "dept": "SMMS", "description": "Axle counter reset frequency above threshold", "severity": "Warning", "reportedOn": "2026-08-22", "dueOn": "2026-08-30", "overdue": False, "urgencyScore": 74, "status": "Assigned"},
    "TDMS-3160": {"id": "TDMS-3160", "section": "GNT-BZA", "dept": "TDMS", "description": "Insulator flashover reported at SP-12", "severity": "Critical", "reportedOn": "2026-08-25", "dueOn": "2026-08-28", "overdue": False, "urgencyScore": 90, "status": "Open"},
    "TMS-1050": {"id": "TMS-1050", "section": "VSKP-BBS", "dept": "TMS", "description": "Weld defect suspected - USFD follow-up due", "severity": "Warning", "reportedOn": "2026-08-18", "dueOn": "2026-08-24", "overdue": True, "urgencyScore": 79, "status": "Open"},
    "SMMS-2220": {"id": "SMMS-2220", "section": "NGP-BPL", "dept": "SMMS", "description": "Signal lamp voltage drift at S-114", "severity": "Normal", "reportedOn": "2026-08-26", "dueOn": "2026-09-05", "overdue": False, "urgencyScore": 41, "status": "Open"},
    "TDMS-3164": {"id": "TDMS-3164", "section": "ET-JBP", "dept": "TDMS", "description": "Dropper snapped, span 22", "severity": "Warning", "reportedOn": "2026-08-25", "dueOn": "2026-09-01", "overdue": False, "urgencyScore": 63, "status": "Assigned"},
    "TMS-1053": {"id": "TMS-1053", "section": "BPL-ET", "dept": "TMS", "description": "Track geometry - twist exceeds limit at KM 91/5", "severity": "Critical", "reportedOn": "2026-08-26", "dueOn": "2026-08-29", "overdue": False, "urgencyScore": 87, "status": "Open"},
    "SMMS-2224": {"id": "SMMS-2224", "section": "MAS-GNT", "dept": "SMMS", "description": "Cable insulation resistance low - loop 7", "severity": "Warning", "reportedOn": "2026-08-20", "dueOn": "2026-08-27", "overdue": True, "urgencyScore": 76, "status": "Open"},
    "TDMS-3170": {"id": "TDMS-3170", "section": "BSP-NGP", "dept": "TDMS", "description": "Neutral section arcing observed", "severity": "Warning", "reportedOn": "2026-08-27", "dueOn": "2026-09-03", "overdue": False, "urgencyScore": 68, "status": "Open"},
    "TMS-1058": {"id": "TMS-1058", "section": "BBS-KUR", "dept": "TMS", "description": "Level crossing surface degradation LC-42", "severity": "Normal", "reportedOn": "2026-08-24", "dueOn": "2026-09-08", "overdue": False, "urgencyScore": 35, "status": "Assigned"},
    "SMMS-2231": {"id": "SMMS-2231", "section": "VSKP-BBS", "dept": "SMMS", "description": "Relay room temperature alarm recurring", "severity": "Normal", "reportedOn": "2026-08-27", "dueOn": "2026-09-10", "overdue": False, "urgencyScore": 29, "status": "Open"},
    "TDMS-3175": {"id": "TDMS-3175", "section": "NGP-BPL", "dept": "TDMS", "description": "Earthing continuity check overdue - 12 masts", "severity": "Warning", "reportedOn": "2026-08-15", "dueOn": "2026-08-23", "overdue": True, "urgencyScore": 72, "status": "Open"}
}
db.reference("/defects").set(defects)

blocks = {
    "BLK-2001": {"id": "BLK-2001", "section": "BSP-NGP", "dept": "TMS", "activity": "Rail renewal + tamping", "date": "2026-08-28", "start": 1.5, "end": 4.5, "status": "Approved", "aiScore": 94, "trainsImpacted": 2},
    "BLK-2002": {"id": "BLK-2002", "section": "GNT-BZA", "dept": "SMMS", "activity": "Point machine replacement", "date": "2026-08-28", "start": 2, "end": 4, "status": "Approved", "aiScore": 91, "trainsImpacted": 1},
    "BLK-2003": {"id": "BLK-2003", "section": "BPL-ET", "dept": "TDMS", "activity": "OHE wire renewal", "date": "2026-08-28", "start": 5, "end": 8, "status": "Planned", "aiScore": 82, "trainsImpacted": 4},
    "BLK-2004": {"id": "BLK-2004", "section": "MAS-GNT", "dept": "TMS", "activity": "Ballast screening", "date": "2026-08-28", "start": 10, "end": 13, "status": "In Progress", "aiScore": 77, "trainsImpacted": 3},
    "BLK-2005": {"id": "BLK-2005", "section": "VSKP-BBS", "dept": "SMMS", "activity": "Axle counter calibration", "date": "2026-08-28", "start": 14, "end": 15.5, "status": "Planned", "aiScore": 69, "trainsImpacted": 2},
    "BLK-2006": {"id": "BLK-2006", "section": "NGP-BPL", "dept": "TDMS", "activity": "Mast earthing audit", "date": "2026-08-29", "start": 1, "end": 3, "status": "Planned", "aiScore": 74, "trainsImpacted": 1},
    "BLK-2007": {"id": "BLK-2007", "section": "ET-JBP", "dept": "TMS", "activity": "USFD testing", "date": "2026-08-29", "start": 6, "end": 9, "status": "Planned", "aiScore": 61, "trainsImpacted": 5},
    "BLK-2008": {"id": "BLK-2008", "section": "BBS-KUR", "dept": "SMMS", "activity": "Cable megger + relay room AC", "date": "2026-08-29", "start": 12, "end": 14, "status": "Rejected", "aiScore": 44, "trainsImpacted": 6},
    "BLK-2009": {"id": "BLK-2009", "section": "BSP-NGP", "dept": "TDMS", "activity": "Neutral section repair", "date": "2026-08-30", "start": 2, "end": 5, "status": "Approved", "aiScore": 88, "trainsImpacted": 2},
    "BLK-2010": {"id": "BLK-2010", "section": "BPL-ET", "dept": "TMS", "activity": "Track geometry correction", "date": "2026-08-30", "start": 22, "end": 24, "status": "Completed", "aiScore": 85, "trainsImpacted": 1}
}
db.reference("/schedule").set(blocks)

alerts = {
    "AL-01": {"id": "AL-01", "section": "BSP-NGP", "dept": "TMS", "message": "Vibration spike detected - health score dropped to 41", "severity": "Critical", "time": "11:42", "acknowledged": False},
    "AL-02": {"id": "AL-02", "section": "GNT-BZA", "dept": "SMMS", "message": "Point machine 34B failed detection 3x in an hour", "severity": "Critical", "time": "11:18", "acknowledged": False},
    "AL-03": {"id": "AL-03", "section": "BPL-ET", "dept": "TDMS", "message": "OHE wear crossed 20% - block request auto-generated", "severity": "Warning", "time": "10:55", "acknowledged": False},
    "AL-04": {"id": "AL-04", "section": "MAS-GNT", "dept": "TMS", "message": "Ballast screening block running 22 min behind", "severity": "Warning", "time": "10:07", "acknowledged": True},
    "AL-05": {"id": "AL-05", "section": "VSKP-BBS", "dept": "SMMS", "message": "Relay room temperature back within limits", "severity": "Normal", "time": "09:31", "acknowledged": True}
}
db.reference("/alerts").set(alerts)

train_paths = {
    "12951": {"id": "12951", "name": "12951 Rajdhani Exp", "points": [{"km": 0, "hour": 0.5}, {"km": 60, "hour": 1.4}, {"km": 140, "hour": 2.6}, {"km": 220, "hour": 3.9}, {"km": 300, "hour": 5.1}]},
    "12301": {"id": "12301", "name": "12301 Howrah Rajdhani", "points": [{"km": 0, "hour": 3}, {"km": 70, "hour": 4.2}, {"km": 150, "hour": 5.6}, {"km": 240, "hour": 7.1}, {"km": 300, "hour": 8.2}]},
    "12627": {"id": "12627", "name": "12627 Karnataka Exp", "points": [{"km": 0, "hour": 8.5}, {"km": 80, "hour": 10.1}, {"km": 170, "hour": 12}, {"km": 250, "hour": 13.7}, {"km": 300, "hour": 15}]}
}
db.reference("/telemetry").set(train_paths)

slots = {
    "SL-1": {"id": "SL-1", "section": "BSP-NGP", "window": "01:30 - 04:30", "durationMin": 180, "trainsAffected": 2, "aiRecommended": True, "confidence": 94},
    "SL-2": {"id": "SL-2", "section": "GNT-BZA", "window": "02:00 - 04:00", "durationMin": 120, "trainsAffected": 1, "aiRecommended": True, "confidence": 91},
    "SL-3": {"id": "SL-3", "section": "BPL-ET", "window": "05:00 - 08:00", "durationMin": 180, "trainsAffected": 4, "aiRecommended": False, "confidence": 66},
    "SL-4": {"id": "SL-4", "section": "MAS-GNT", "window": "10:00 - 13:00", "durationMin": 180, "trainsAffected": 3, "aiRecommended": False, "confidence": 58},
    "SL-5": {"id": "SL-5", "section": "VSKP-BBS", "window": "14:00 - 15:30", "durationMin": 90, "trainsAffected": 2, "aiRecommended": True, "confidence": 83},
    "SL-6": {"id": "SL-6", "section": "ET-JBP", "window": "23:00 - 02:00", "durationMin": 180, "trainsAffected": 1, "aiRecommended": True, "confidence": 89}
}
db.reference("/slots").set(slots)

print("Seed data written successfully.")