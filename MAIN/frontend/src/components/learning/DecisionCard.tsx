"use client";

import React from "react";
import { GitBranch } from "lucide-react";
import { MathText } from "@/components/math-view";

interface DecisionCardProps {
  decision: string;
  concept?: string | null;
}

export function DecisionCard({ decision, concept }: DecisionCardProps) {
  if (!decision) return null;

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-[#38D9E8]/30 bg-[#38D9E8]/5 space-y-2 shadow-lg">
      <div className="flex items-center space-x-2 text-xs font-bold text-[#38D9E8] uppercase tracking-wider">
        <span className="p-1.5 rounded-lg bg-[#38D9E8]/15 text-[#38D9E8] border border-[#38D9E8]/30">
          <GitBranch className="w-3.5 h-3.5" />
        </span>
        <span>Algorithmic Decision & Rationale</span>
        {concept && (
          <span className="text-[10px] text-[#B5C0CC] bg-white/[0.06] px-2.5 py-0.5 rounded-full border border-white/[0.12] font-normal ml-auto">
            {concept}
          </span>
        )}
      </div>

      <div className="text-xs sm:text-[13px] text-[#B5C0CC] leading-relaxed pl-1 pt-1">
        <MathText text={decision} />
      </div>
    </div>
  );
}
