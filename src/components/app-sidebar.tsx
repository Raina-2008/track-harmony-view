import { Link } from "@tanstack/react-router";
import {
  LayoutDashboard,
  CalendarRange,
  AlertTriangle,
  BarChart3,
  TrainFront,
  Settings,
  ChevronLeft,
  Radio,
} from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const NAV = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/gantt", label: "Block Planner", icon: CalendarRange },
  { to: "/defects", label: "Defects", icon: AlertTriangle },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/corridor", label: "Corridor", icon: TrainFront },
  { to: "/settings", label: "Settings", icon: Settings },
] as const;

export function AppSidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "sticky top-0 flex h-screen shrink-0 flex-col border-r border-sidebar-border bg-sidebar transition-[width] duration-200",
        collapsed ? "w-16" : "w-60",
      )}
    >
      <div className="flex items-center gap-2 px-4 py-5">
        <div className="grid size-9 shrink-0 place-items-center rounded-md bg-primary/15 text-primary">
          <Radio className="size-5" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold tracking-tight">ABPS</p>
            <p className="truncate text-[11px] text-muted-foreground">
              Rail Block Planning
            </p>
          </div>
        )}
      </div>

      <nav className="flex-1 space-y-1 px-2">
        {NAV.map(({ to, label, icon: Icon }) => (
          <Link
            key={to}
            to={to}
            activeOptions={{ exact: to === "/" }}
            activeProps={{
              className: "bg-sidebar-accent text-sidebar-accent-foreground",
            }}
            className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-sidebar-foreground/80 transition-colors hover:bg-sidebar-accent/60 hover:text-sidebar-accent-foreground"
            title={label}
          >
            <Icon className="size-4 shrink-0" />
            {!collapsed && <span className="truncate">{label}</span>}
          </Link>
        ))}
      </nav>

      <button
        onClick={() => setCollapsed((c) => !c)}
        className="m-2 flex items-center gap-2 rounded-md px-3 py-2 text-xs text-muted-foreground transition-colors hover:bg-sidebar-accent/60"
      >
        <ChevronLeft
          className={cn("size-4 transition-transform", collapsed && "rotate-180")}
        />
        {!collapsed && <span>Collapse</span>}
      </button>
    </aside>
  );
}
