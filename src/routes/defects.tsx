import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PageHeader, DeptTag, SeverityTag } from "@/components/ui-bits";
import { useRealtime } from "@/hooks/use-realtime";
import { DEFECTS } from "@/lib/mock-data";
import type { Defect } from "@/lib/types";

export const Route = createFileRoute("/defects")({
  head: () => ({
    meta: [
      { title: "Defect Register — ABPS Rail Block Planning" },
      {
        name: "description",
        content:
          "Unified TMS, TDMS and SMMS defect register with overdue tracking and AI urgency prioritisation.",
      },
      { property: "og:title", content: "Defect Register — ABPS" },
      {
        property: "og:description",
        content: "Unified defect register with AI urgency prioritisation.",
      },
    ],
  }),
  component: Defects,
});

function Defects() {
  const { data: defects } = useRealtime("/defects", DEFECTS);
  const [dept, setDept] = useState("all");
  const [section, setSection] = useState("all");
  const [q, setQ] = useState("");

  const base = defects.filter(
    (d) =>
      (dept === "all" || d.dept === dept) &&
      (section === "all" || d.section === section) &&
      (q === "" ||
        `${d.id} ${d.description} ${d.section}`.toLowerCase().includes(q.toLowerCase())),
  );

  const views = {
    all: base,
    overdue: base.filter((d) => d.overdue),
    critical: base.filter((d) => d.severity === "Critical"),
    ai: [...base].sort((a, b) => b.urgencyScore - a.urgencyScore),
  };

  const sections = [...new Set(defects.map((d) => d.section))];

  return (
    <div>
      <PageHeader
        title="Defect Register"
        subtitle="Consolidated feed from TMS, TDMS and SMMS"
      />

      <Card className="mb-4">
        <CardContent className="flex flex-wrap items-center gap-3 pt-6">
          <Input
            placeholder="Search defects…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="w-64"
          />
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
          <Select value={section} onValueChange={setSection}>
            <SelectTrigger className="w-48">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All sections</SelectItem>
              {sections.map((s) => (
                <SelectItem key={s} value={s}>
                  {s}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      <Tabs defaultValue="all">
        <TabsList>
          <TabsTrigger value="all">All ({views.all.length})</TabsTrigger>
          <TabsTrigger value="overdue">Overdue ({views.overdue.length})</TabsTrigger>
          <TabsTrigger value="critical">Critical ({views.critical.length})</TabsTrigger>
          <TabsTrigger value="ai">AI Prioritized</TabsTrigger>
        </TabsList>
        {Object.entries(views).map(([key, rows]) => (
          <TabsContent key={key} value={key}>
            <Card>
              <CardContent className="pt-6">
                <DefectTable rows={rows} />
              </CardContent>
            </Card>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  );
}

function DefectTable({ rows }: { rows: Defect[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Section</TableHead>
          <TableHead>Dept</TableHead>
          <TableHead>Description</TableHead>
          <TableHead>Severity</TableHead>
          <TableHead>Due</TableHead>
          <TableHead className="text-right">Urgency</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((d) => (
          <TableRow key={d.id}>
            <TableCell className="font-mono text-xs">{d.id}</TableCell>
            <TableCell>{d.section}</TableCell>
            <TableCell>
              <DeptTag dept={d.dept} />
            </TableCell>
            <TableCell className="max-w-[320px] truncate">{d.description}</TableCell>
            <TableCell>
              <SeverityTag severity={d.severity} />
            </TableCell>
            <TableCell className={d.overdue ? "text-critical" : ""}>
              {d.dueOn}
              {d.overdue && " · overdue"}
            </TableCell>
            <TableCell className="text-right">
              <div className="flex items-center justify-end gap-2">
                <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
                  <div
                    className={
                      d.urgencyScore >= 85
                        ? "h-full bg-critical"
                        : d.urgencyScore >= 60
                          ? "h-full bg-warning"
                          : "h-full bg-ok"
                    }
                    style={{ width: `${d.urgencyScore}%` }}
                  />
                </div>
                <span className="w-6 text-xs font-medium">{d.urgencyScore}</span>
              </div>
            </TableCell>
          </TableRow>
        ))}
        {rows.length === 0 && (
          <TableRow>
            <TableCell colSpan={7} className="text-center text-muted-foreground">
              No defects match these filters.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}
