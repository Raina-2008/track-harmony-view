export type Dept = "TMS" | "TDMS" | "SMMS";
export type Severity = "Critical" | "Warning" | "Normal";
export type BlockStatus = "Planned" | "Approved" | "Rejected" | "In Progress" | "Completed";

export type Section = {
  id: string;
  name: string;
  zone: string;
  healthScore: number;
  availability: number;
  from: [number, number];
  to: [number, number];
  openDefects: number;
};

export type Defect = {
  id: string;
  section: string;
  dept: Dept;
  description: string;
  severity: Severity;
  reportedOn: string;
  dueOn: string;
  overdue: boolean;
  urgencyScore: number;
  status: "Open" | "Assigned" | "Closed";
};

export type Block = {
  id: string;
  section: string;
  dept: Dept;
  activity: string;
  date: string;
  start: number; // hours, 0-24
  end: number;
  status: BlockStatus;
  aiScore: number;
  trainsImpacted: number;
};

export type Alert = {
  id: string;
  section: string;
  dept: Dept;
  message: string;
  severity: Severity;
  time: string;
  acknowledged: boolean;
};

export type TrainPath = {
  id: string;
  name: string;
  points: { km: number; hour: number }[];
};

export type Slot = {
  id: string;
  section: string;
  window: string;
  durationMin: number;
  trainsAffected: number;
  aiRecommended: boolean;
  confidence: number;
};
