"use client";

import React, { useState } from "react";
import { IterationItem } from "@/lib/api";
import { MathText } from "@/components/math-view";
import { ChevronDown, ChevronRight, Sparkles } from "lucide-react";

interface StepTableProps {
  iterations: IterationItem[];
  method: string;
  highlightedIteration?: number | null;
}

export function StepTable({ iterations, method, highlightedIteration }: StepTableProps) {
  const [expandedRow, setExpandedRow] = useState<number | null>(null);

  React.useEffect(() => {
    if (highlightedIteration !== null && highlightedIteration !== undefined) {
      const el = window.document.getElementById(`iteration-row-${highlightedIteration}`);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  }, [highlightedIteration]);

  if (!iterations || iterations.length === 0) {
    return (
      <div className="p-8 text-center text-[#7E8A98] text-sm italic glass-card rounded-2xl border border-white/[0.08]">
        No iteration steps recorded. Run a calculation to view the step-by-step process.
      </div>
    );
  }

  const sampleValues = iterations[0]?.values || {};
  const valueKeys = Object.keys(sampleValues);
  const totalIterations = iterations.length;

  return (
    <div className="w-full glass-card-static rounded-2xl border border-white/[0.12] overflow-hidden shadow-lg backdrop-blur-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-[#F5F7FA] font-mono">
          <thead className="bg-white/[0.06] text-[#B5C0CC] font-semibold border-b border-white/[0.1] uppercase tracking-wider text-[11px] backdrop-blur-md">
            <tr>
              <th className="py-3 px-4 w-16 text-center">#</th>
              {valueKeys.map((k) => (
                <th key={k} className="py-3 px-4">{k}</th>
              ))}
              <th className="py-3 px-4 text-[#38D9E8]">Error / Residual</th>
              <th className="py-3 px-4 text-right">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.06]">
            {iterations.map((it, idx) => {
              const isExpanded = expandedRow === it.n;
              const isHighlighted = highlightedIteration === it.n;
              const isFirst = it.n === 1;
              const isLast = idx === totalIterations - 1 && totalIterations > 1;

              return (
                <React.Fragment key={it.n}>
                  <tr
                    id={`iteration-row-${it.n}`}
                    className={`transition-colors ${
                      isHighlighted
                        ? "bg-[#38D9E8]/20 font-bold ring-1 ring-[#38D9E8] shadow-[0_0_15px_rgba(56,217,232,0.25)]"
                        : isFirst
                        ? "bg-[#38D9E8]/5 hover:bg-[#38D9E8]/10"
                        : isLast
                        ? "bg-emerald-500/10 hover:bg-emerald-500/15"
                        : "hover:bg-white/[0.03]"
                    }`}
                  >
                    <td className={`py-2.5 px-4 text-center font-bold ${
                      isHighlighted
                        ? "bg-[#38D9E8]/30 text-white"
                        : isFirst
                        ? "text-[#38D9E8]"
                        : isLast
                        ? "text-emerald-400"
                        : "text-[#7E8A98]"
                    }`}>
                      <div className="flex items-center justify-center space-x-1">
                        <span>{it.n}</span>
                        {isFirst && (
                          <span className="text-[9px] font-sans px-1.5 py-0.2 rounded bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/30">
                            Worked
                          </span>
                        )}
                        {isLast && (
                          <span className="text-[9px] font-sans px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            Final
                          </span>
                        )}
                      </div>
                    </td>
                    {valueKeys.map((k) => {
                      const v = it.values[k];
                      return (
                        <td key={k} className="py-2.5 px-4 truncate max-w-xs text-[#F5F7FA]">
                          {typeof v === "number" ? v.toFixed(6) : <MathText text={String(v ?? "—")} />}
                        </td>
                      );
                    })}
                    <td className="py-2.5 px-4 font-semibold text-[#38D9E8]">
                      {it.approximate_error !== null && it.approximate_error !== undefined
                        ? it.approximate_error.toExponential(4)
                        : "—"}
                    </td>
                    <td className="py-2.5 px-4 text-right">
                      {it.extra && Object.keys(it.extra).length > 0 ? (
                        <button
                          type="button"
                          onClick={() => setExpandedRow(isExpanded ? null : it.n)}
                          className="inline-flex items-center text-[#38D9E8] hover:text-white font-sans font-medium px-2 py-1 rounded-lg hover:bg-white/[0.08] transition-colors cursor-pointer"
                        >
                          {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                        </button>
                      ) : null}
                    </td>
                  </tr>
                  {isExpanded && it.extra && (
                    <tr className="bg-black/40 font-sans text-xs text-[#B5C0CC]">
                      <td colSpan={valueKeys.length + 3} className="p-4 border-t border-white/[0.08]">
                        <div className="font-semibold text-[#F5F7FA] mb-1.5 flex items-center space-x-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-[#38D9E8]" />
                          <span>Step {it.n} Derivation Details:</span>
                        </div>
                        {it.extra.description && (
                          <div className="font-mono text-[#38D9E8] bg-black/60 p-2.5 rounded-xl border border-white/[0.1] mb-2 shadow-inner">
                            <MathText text={it.extra.description} />
                          </div>
                        )}
                        {it.extra.operation && (
                          <div className="font-mono text-[#FFAD66] bg-[#FF793F]/10 p-2 rounded-lg border border-[#FF793F]/20 mb-2">
                            <MathText text={it.extra.operation} />
                          </div>
                        )}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 font-mono text-[11px]">
                          {it.extra && Object.keys(it.extra)
                            .filter((ek) => ek !== "description" && ek !== "operation")
                            .map((ek) => (
                              <div key={ek} className="bg-white/[0.03] p-1.5 rounded-lg border border-white/[0.06]">
                                <span className="text-[#7E8A98]">{ek}: </span>
                                <span className="text-[#F5F7FA] font-bold">
                                  <MathText text={String(it.extra?.[ek] ?? "")} />
                                </span>
                              </div>
                            ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
