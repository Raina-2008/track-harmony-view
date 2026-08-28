import type { ReactNode } from "react";
import { cn } from "@/lib/utils";
import type { Dept, Severity } from "@/lib/types";

export function PageHeader({
  title,
  subtitle,
  right,
}: {
  title: string;
  subtitle?: string;
  right?: ReactNode;
}) {
  return (
    <header className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        {subtitle && (
          <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p>
        )}
      </div>
      {right}
    </header>
  );
}

export const deptClass: Record<Dept, string> = {
  TMS: "bg-tms/15 text-tms border-tms/40",
  TDMS: "bg-tdms/15 text-tdms border-tdms/40",
  SMMS: "bg-smms/15 text-smms border-smms/40",
};

export const deptBar: Record<Dept, string> = {
  TMS: "bg-tms/70 border-tms",
  TDMS: "bg-tdms/70 border-tdms",
  SMMS: "bg-smms/70 border-smms",
};

export function DeptTag({ dept }: { dept: Dept }) {
  return (
    <span
      className={cn(
        "inline-flex rounded border px-1.5 py-0.5 text-[11px] font-medium",
        deptClass[dept],
      )}
    >
      {dept}
    </span>
  );
}

export function SeverityTag({ severity }: { severity: Severity }) {
  const map: Record<Severity, string> = {
    Critical: "bg-critical/15 text-critical border-critical/40",
    Warning: "bg-warning/15 text-warning border-warning/40",
    Normal: "bg-ok/15 text-ok border-ok/40",
  };
  return (
    <span
      className={cn(
        "inline-flex rounded border px-1.5 py-0.5 text-[11px] font-medium",
        map[severity],
      )}
    >
      {severity}
    </span>
  );
}

export function healthClass(score: number) {
  if (score >= 80) return "text-ok";
  if (score >= 60) return "text-warning";
  if (score >= 45) return "text-tdms";
  return "text-critical";
}

export function healthHex(score: number) {
  if (score >= 80) return "#22c55e";
  if (score >= 60) return "#f59e0b";
  if (score >= 45) return "#f97316";
  return "#ef4444";
}

export function fmtHour(h: number) {
  const hh = Math.floor(h) % 24;
  const mm = Math.round((h - Math.floor(h)) * 60);
  return `${String(hh).padStart(2, "0")}:${String(mm).padStart(2, "0")}`;
}
