import React from "react";

interface MetricCardProps {
  label: string;
  value: string | number | null | undefined;
  subtext?: string;
  badge?: string;
  color?: "cyan" | "teal" | "orange" | "emerald" | "blue" | "rose" | "slate";
}

export function MetricCard({
  label,
  value,
  subtext,
  badge,
  color = "cyan",
}: MetricCardProps) {
  const badgeStyles: Record<string, string> = {
    cyan: "text-[#38D9E8] bg-cyan-400/10 border-cyan-400/30 shadow-[0_0_8px_rgba(56,217,232,0.15)]",
    teal: "text-[#16B8B0] bg-teal-400/10 border-teal-400/30 shadow-[0_0_8px_rgba(22,184,176,0.15)]",
    orange: "text-[#FF793F] bg-orange-500/10 border-orange-400/30 shadow-[0_0_8px_rgba(255,121,63,0.15)]",
    emerald: "text-emerald-400 bg-emerald-500/10 border-emerald-400/30",
    blue: "text-[#4B9DFF] bg-blue-500/10 border-blue-400/30",
    rose: "text-rose-400 bg-rose-500/10 border-rose-400/30",
    slate: "text-[#B5C0CC] bg-white/[0.05] border-white/[0.1]",
  };

  const badgeClass = badgeStyles[color] || badgeStyles.cyan;
  const displayVal = value !== null && value !== undefined && value !== "" ? String(value) : "—";

  return (
    <div className="glass-card p-4 rounded-2xl border border-white/[0.12] shadow-sm flex flex-col justify-between group hover:border-cyan-400/30 transition-all">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[11px] font-semibold text-[#7E8A98] uppercase tracking-wider">{label}</span>
        {badge && (
          <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border ${badgeClass}`}>
            {badge}
          </span>
        )}
      </div>
      <div className="text-xl sm:text-2xl font-mono font-extrabold text-[#F5F7FA] tracking-tight truncate group-hover:text-[#38D9E8] transition-colors">
        {displayVal}
      </div>
      {subtext && <span className="text-xs text-[#7E8A98] mt-1 truncate">{subtext}</span>}
    </div>
  );
}
