"use client";

import React from "react";
import { MathView, MathText } from "@/components/math-view";
import { CheckCircle2, ChevronRight, Sigma } from "lucide-react";

interface CalculationBlockProps {
  calculationLatex?: string | null;
  resultLatex?: string | null;
  substeps?: string[];
  title?: string;
}

export function CalculationBlock({
  calculationLatex,
  resultLatex,
  substeps,
  title = "Step-by-Step Numerical Calculations",
}: CalculationBlockProps) {
  if (!calculationLatex && !resultLatex && (!substeps || substeps.length === 0)) {
    return null;
  }

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-white/[0.12] space-y-3.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2 text-xs font-semibold text-[#B5C0CC] uppercase tracking-wider">
          <Sigma className="w-4 h-4 text-[#38D9E8]" />
          <span>{title}</span>
        </div>
      </div>

      {/* Main Multi-line Calculation Block */}
      {calculationLatex && (
        <div className="bg-[#080B10]/80 p-4 rounded-xl border border-white/[0.08] overflow-x-auto text-[#F5F7FA] shadow-inner">
          <MathView math={calculationLatex} display />
        </div>
      )}

      {/* Micro-substeps bullet list */}
      {substeps && substeps.length > 0 && (
        <div className="space-y-1.5 pt-1">
          {substeps.map((sub, i) => (
            <div key={i} className="flex items-center space-x-2 text-xs text-[#B5C0CC] font-mono">
              <ChevronRight className="w-3.5 h-3.5 text-[#38D9E8] shrink-0" />
              <MathText text={sub} />
            </div>
          ))}
        </div>
      )}

      {/* Evaluated Step Result Badge */}
      {resultLatex && (
        <div className="bg-emerald-500/10 p-3.5 rounded-xl border border-emerald-500/30 flex items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span className="text-xs font-bold text-emerald-300 uppercase tracking-wider">
              Step Outcome:
            </span>
          </div>
          <div className="font-mono font-bold text-[#F5F7FA] text-xs sm:text-sm overflow-x-auto">
            <MathView math={resultLatex} />
          </div>
        </div>
      )}
    </div>
  );
}
