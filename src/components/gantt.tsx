import type { Block } from "@/lib/types";
import { cn } from "@/lib/utils";
import { deptBar, fmtHour } from "./ui-bits";

const HOURS = [0, 3, 6, 9, 12, 15, 18, 21, 24];

export function Gantt({
  blocks,
  onSelect,
  compact = false,
}: {
  blocks: Block[];
  onSelect?: (b: Block) => void;
  compact?: boolean;
}) {
  const rows = Array.from(new Set(blocks.map((b) => b.section)));

  return (
    <div className="w-full overflow-x-auto">
      <div className="min-w-[640px]">
        <div className="flex border-b border-border pb-1 text-[11px] text-muted-foreground">
          <div className="w-24 shrink-0" />
          <div className="relative h-4 flex-1">
            {HOURS.map((h) => (
              <span
                key={h}
                className="absolute -translate-x-1/2"
                style={{ left: `${(h / 24) * 100}%` }}
              >
                {String(h).padStart(2, "0")}
              </span>
            ))}
          </div>
        </div>

        <div className="divide-y divide-border/60">
          {rows.map((section) => (
            <div key={section} className="flex items-center">
              <div className="w-24 shrink-0 py-2 pr-2 text-xs font-medium text-muted-foreground">
                {section}
              </div>
              <div
                className={cn(
                  "relative flex-1",
                  compact ? "h-8" : "h-11",
                )}
              >
                {HOURS.map((h) => (
                  <div
                    key={h}
                    className="absolute inset-y-0 w-px bg-border/40"
                    style={{ left: `${(h / 24) * 100}%` }}
                  />
                ))}
                {blocks
                  .filter((b) => b.section === section)
                  .map((b) => (
                    <button
                      key={b.id}
                      onClick={() => onSelect?.(b)}
                      title={`${b.id} · ${b.activity}`}
                      className={cn(
                        "absolute top-1/2 flex h-6 -translate-y-1/2 items-center overflow-hidden rounded border px-1.5 text-[11px] font-medium text-foreground transition-opacity hover:opacity-90",
                        deptBar[b.dept],
                        b.status === "Rejected" && "opacity-40 line-through",
                      )}
                      style={{
                        left: `${(b.start / 24) * 100}%`,
                        width: `${((b.end - b.start) / 24) * 100}%`,
                      }}
                    >
                      <span className="truncate">
                        {compact ? b.dept : `${b.dept} · ${b.activity}`}
                      </span>
                    </button>
                  ))}
              </div>
            </div>
          ))}
          {rows.length === 0 && (
            <p className="py-6 text-center text-sm text-muted-foreground">
              No blocks match the current filters.
            </p>
          )}
        </div>

        <div className="mt-3 flex flex-wrap gap-4 text-[11px] text-muted-foreground">
          <Legend color="bg-tms" label="TMS — Engineering" />
          <Legend color="bg-tdms" label="TDMS — Traction" />
          <Legend color="bg-smms" label="SMMS — S&T" />
        </div>
      </div>
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="flex items-center gap-1.5">
      <span className={cn("size-2.5 rounded-sm", color)} />
      {label}
    </span>
  );
}

export function blockWindow(b: Block) {
  return `${fmtHour(b.start)} – ${fmtHour(b.end)}`;
}
