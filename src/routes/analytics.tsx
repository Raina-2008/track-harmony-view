import { createFileRoute } from "@tanstack/react-router";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader, healthClass } from "@/components/ui-bits";
import { useRealtime } from "@/hooks/use-realtime";
import { DEPT_ACTIVITY, PLANNED_VS_ACTUAL, SECTIONS } from "@/lib/mock-data";

export const Route = createFileRoute("/analytics")({
  head: () => ({
    meta: [
      { title: "Analytics — ABPS Rail Block Planning" },
      {
        name: "description",
        content:
          "Section health scoring, planned versus actual block execution and department activity analytics.",
      },
      { property: "og:title", content: "Analytics — ABPS" },
      {
        property: "og:description",
        content: "Health scoring, block execution and department activity analytics.",
      },
    ],
  }),
  component: Analytics,
});

const axis = { stroke: "var(--color-muted-foreground)", fontSize: 12 };
const tooltipStyle = {
  background: "var(--color-card)",
  border: "1px solid var(--color-border)",
  borderRadius: 8,
  color: "var(--color-foreground)",
};

function Analytics() {
  const { data: sections } = useRealtime("/sections", SECTIONS);

  return (
    <div>
      <PageHeader
        title="Analytics"
        subtitle="Asset availability trends and multi-department execution quality"
      />

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {sections.map((s) => (
          <Card key={s.id}>
            <CardContent className="pt-6">
              <div className="flex items-baseline justify-between">
                <span className="text-sm font-medium">{s.id}</span>
                <span className={`text-2xl font-semibold ${healthClass(s.healthScore)}`}>
                  {s.healthScore}
                </span>
              </div>
              <p className="mt-1 truncate text-xs text-muted-foreground">
                {s.name} · {s.zone}
              </p>
              <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full bg-primary"
                  style={{ width: `${s.availability}%` }}
                />
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">
                Availability {s.availability}% · {s.openDefects} open defects
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-6 grid gap-4 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Planned vs actual blocks</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={PLANNED_VS_ACTUAL}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="day" {...axis} />
                <YAxis {...axis} />
                <Tooltip contentStyle={tooltipStyle} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="planned"
                  stroke="var(--color-tms)"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="var(--color-ok)"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Department activity by day</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={DEPT_ACTIVITY}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                <XAxis dataKey="day" {...axis} />
                <YAxis {...axis} />
                <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "transparent" }} />
                <Legend />
                <Bar dataKey="TMS" stackId="a" fill="var(--color-tms)" />
                <Bar dataKey="TDMS" stackId="a" fill="var(--color-tdms)" />
                <Bar dataKey="SMMS" stackId="a" fill="var(--color-smms)" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
