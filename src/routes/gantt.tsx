import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { PageHeader, DeptTag } from "@/components/ui-bits";
import { Gantt, blockWindow } from "@/components/gantt";
import { useRealtime } from "@/hooks/use-realtime";
import { BLOCKS } from "@/lib/mock-data";
import type { Block } from "@/lib/types";

export const Route = createFileRoute("/gantt")({
  head: () => ({
    meta: [
      { title: "Block Planner — ABPS Rail Block Planning" },
      {
        name: "description",
        content:
          "Multi-department Gantt planner for maintenance blocks with approval workflow and AI scheduling scores.",
      },
      { property: "og:title", content: "Block Planner — ABPS" },
      {
        property: "og:description",
        content: "Multi-department Gantt planner with block approval workflow.",
      },
    ],
  }),
  component: Planner,
});

function Planner() {
  const { data: blocks } = useRealtime("/schedule", BLOCKS);
  const [dept, setDept] = useState("all");
  const [status, setStatus] = useState("all");
  const [from, setFrom] = useState("2026-08-28");
  const [to, setTo] = useState("2026-08-30");
  const [selected, setSelected] = useState<Block | null>(null);
  const [decisions, setDecisions] = useState<Record<string, string>>({});

  const filtered = blocks.filter(
    (b) =>
      (dept === "all" || b.dept === dept) &&
      (status === "all" || b.status === status) &&
      b.date >= from &&
      b.date <= to,
  );

  const decide = (b: Block, verdict: "Approved" | "Rejected") => {
    setDecisions((d) => ({ ...d, [b.id]: verdict }));
    setSelected(null);
    toast.success(`${b.id} ${verdict.toLowerCase()}`, {
      description: `${b.section} · ${b.activity}`,
    });
  };

  return (
    <div>
      <PageHeader
        title="Block Planner"
        subtitle="Weekly and daily horizon — optimised across departments"
      />

      <Card className="mb-4">
        <CardContent className="flex flex-wrap items-end gap-3 pt-6">
          <Field label="Department">
            <Select value={dept} onValueChange={setDept}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All departments</SelectItem>
                <SelectItem value="TMS">TMS</SelectItem>
                <SelectItem value="TDMS">TDMS</SelectItem>
                <SelectItem value="SMMS">SMMS</SelectItem>
              </SelectContent>
            </Select>
          </Field>
          <Field label="Status">
            <Select value={status} onValueChange={setStatus}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All statuses</SelectItem>
                <SelectItem value="Planned">Planned</SelectItem>
                <SelectItem value="Approved">Approved</SelectItem>
                <SelectItem value="In Progress">In Progress</SelectItem>
                <SelectItem value="Completed">Completed</SelectItem>
                <SelectItem value="Rejected">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </Field>
          <Field label="From">
            <Input
              type="date"
              value={from}
              onChange={(e) => setFrom(e.target.value)}
              className="w-40"
            />
          </Field>
          <Field label="To">
            <Input
              type="date"
              value={to}
              onChange={(e) => setTo(e.target.value)}
              className="w-40"
            />
          </Field>
        </CardContent>
      </Card>

      {[...new Set(filtered.map((b) => b.date))].sort().map((date) => (
        <Card key={date} className="mb-4">
          <CardHeader>
            <CardTitle className="text-base">{date}</CardTitle>
          </CardHeader>
          <CardContent>
            <Gantt
              blocks={filtered.filter((b) => b.date === date)}
              onSelect={setSelected}
            />
          </CardContent>
        </Card>
      ))}

      <Dialog open={!!selected} onOpenChange={(o) => !o && setSelected(null)}>
        <DialogContent>
          {selected && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  {selected.id} <DeptTag dept={selected.dept} />
                </DialogTitle>
              </DialogHeader>
              <dl className="space-y-2 text-sm">
                <Row k="Section" v={selected.section} />
                <Row k="Activity" v={selected.activity} />
                <Row k="Date" v={selected.date} />
                <Row k="Window" v={blockWindow(selected)} />
                <Row
                  k="Duration"
                  v={`${(selected.end - selected.start).toFixed(1)} h`}
                />
                <Row k="Trains impacted" v={String(selected.trainsImpacted)} />
                <Row k="AI score" v={String(selected.aiScore)} />
                <Row
                  k="Status"
                  v={decisions[selected.id] ?? selected.status}
                />
              </dl>
              <DialogFooter>
                <Button
                  variant="secondary"
                  onClick={() => decide(selected, "Rejected")}
                >
                  Reject
                </Button>
                <Button onClick={() => decide(selected, "Approved")}>Approve</Button>
              </DialogFooter>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1">
      <span className="block text-xs text-muted-foreground">{label}</span>
      {children}
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex justify-between gap-4 border-b border-border/60 pb-1">
      <dt className="text-muted-foreground">{k}</dt>
      <dd className="text-right font-medium">{v}</dd>
    </div>
  );
}
