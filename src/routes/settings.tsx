import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { PageHeader } from "@/components/ui-bits";
import { useRealtime } from "@/hooks/use-realtime";
import { firebaseConfig, isFirebaseConfigured } from "@/lib/firebase";
import { SECTIONS } from "@/lib/mock-data";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title: "Settings — ABPS Rail Block Planning" },
      {
        name: "description",
        content:
          "Firebase realtime connection status, demo mode and AI prioritisation thresholds.",
      },
      { property: "og:title", content: "Settings — ABPS" },
      {
        property: "og:description",
        content: "Connection status, demo mode and AI thresholds.",
      },
    ],
  }),
  component: SettingsPage,
});

function SettingsPage() {
  const { state } = useRealtime("/sections", SECTIONS);
  const [demo, setDemo] = useState(true);
  const [health, setHealth] = useState([55]);
  const [urgency, setUrgency] = useState([80]);
  const [maxTrains, setMaxTrains] = useState([4]);

  return (
    <div className="max-w-3xl">
      <PageHeader title="Settings" subtitle="Data source and AI thresholds" />

      <Card className="mb-4">
        <CardHeader>
          <CardTitle className="text-base">Firebase connection</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <Row k="Status">
            <span
              className={
                state === "live" ? "text-ok" : state === "mock" ? "text-warning" : ""
              }
            >
              {state === "live"
                ? "Connected — live data"
                : state === "mock"
                  ? "Idle — serving demo data"
                  : "Connecting…"}
            </span>
          </Row>
          <Row k="Database URL">
            <span className="font-mono text-xs">{firebaseConfig.databaseURL}</span>
          </Row>
          <Row k="Project">
            <span className="font-mono text-xs">{firebaseConfig.projectId}</span>
          </Row>
          <Row k="API key">
            <span className="font-mono text-xs">
              {isFirebaseConfigured() ? "configured" : "not configured"}
            </span>
          </Row>
          <Row k="Listeners">
            <span className="font-mono text-xs">
              /sections /defects /schedule /alerts /telemetry
            </span>
          </Row>
        </CardContent>
      </Card>

      <Card className="mb-4">
        <CardHeader>
          <CardTitle className="text-base">Demo mode</CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-between">
          <div>
            <Label htmlFor="demo">Use synthetic mock dataset</Label>
            <p className="mt-1 text-xs text-muted-foreground">
              Keeps the dashboard populated when the Firebase nodes are empty.
            </p>
          </div>
          <Switch id="demo" checked={demo} onCheckedChange={setDemo} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">AI thresholds</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <SliderRow
            label="Auto block request below health score"
            value={health}
            onChange={setHealth}
            max={100}
            suffix=""
          />
          <SliderRow
            label="Critical urgency threshold"
            value={urgency}
            onChange={setUrgency}
            max={100}
            suffix=""
          />
          <SliderRow
            label="Max trains impacted per block"
            value={maxTrains}
            onChange={setMaxTrains}
            max={12}
            suffix=" trains"
          />
        </CardContent>
      </Card>
    </div>
  );
}

function Row({ k, children }: { k: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-border/60 pb-2">
      <span className="text-muted-foreground">{k}</span>
      {children}
    </div>
  );
}

function SliderRow({
  label,
  value,
  onChange,
  max,
  suffix,
}: {
  label: string;
  value: number[];
  onChange: (v: number[]) => void;
  max: number;
  suffix: string;
}) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm">
        <Label>{label}</Label>
        <span className="font-medium">
          {value[0]}
          {suffix}
        </span>
      </div>
      <Slider value={value} onValueChange={onChange} max={max} step={1} />
    </div>
  );
}
