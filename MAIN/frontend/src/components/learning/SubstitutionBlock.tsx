"use client";

import React from "react";
import { MathView } from "@/components/math-view";
import { Calculator } from "lucide-react";

interface SubstitutionBlockProps {
  formulaLatex?: string | null;
  substitutionLatex?: string | null;
  title?: string;
}

export function SubstitutionBlock({
  formulaLatex,
  substitutionLatex,
  title = "Formula & Concrete Substitution",
}: SubstitutionBlockProps) {
  if (!formulaLatex && !substitutionLatex) return null;

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-white/[0.12] bg-[#111820]/50 space-y-3">
      <div className="flex items-center space-x-2 text-xs font-semibold text-[#38D9E8] uppercase tracking-wider">
        <Calculator className="w-4 h-4 text-[#16B8B0]" />
        <span>{title}</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 items-stretch">
        {formulaLatex && (
          <div className="bg-[#080B10]/70 p-3.5 rounded-xl border border-white/[0.08] shadow-inner space-y-1.5 flex flex-col justify-between">
            <span className="text-[10px] font-bold text-[#7E8A98] uppercase tracking-wider block">
              Governing Formula:
            </span>
            <div className="overflow-x-auto py-2 text-[#F5F7FA]">
              <MathView math={formulaLatex} display />
            </div>
          </div>
        )}

        {substitutionLatex && (
          <div className="bg-[#080B10]/70 p-3.5 rounded-xl border border-[#38D9E8]/30 shadow-inner space-y-1.5 flex flex-col justify-between">
            <span className="text-[10px] font-bold text-[#38D9E8] uppercase tracking-wider block">
              Substituted Values:
            </span>
            <div className="overflow-x-auto py-2 text-[#38D9E8] font-semibold">
              <MathView math={substitutionLatex} display />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
