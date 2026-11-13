"use client";

import React from "react";
import { FinalInterpretation as FinalInterpretationType } from "@/lib/api";
import { MathText } from "@/components/math-view";
import { CheckCircle2, ShieldCheck, Target, Award, ListChecks } from "lucide-react";

interface FinalInterpretationProps {
  interpretation: FinalInterpretationType;
  methodName: string;
}

export function FinalInterpretation({ interpretation }: FinalInterpretationProps) {
  if (!interpretation) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 sm:p-7 border border-emerald-500/30 bg-[#111820]/70 space-y-5 shadow-2xl relative overflow-hidden">
      {/* Top green/cyan reflection */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-emerald-400/40 to-transparent pointer-events-none" />
      <div className="absolute top-0 right-0 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center space-x-2 text-xs font-bold text-emerald-400 uppercase tracking-wider relative z-10">
        <span className="p-1.5 rounded-lg bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
          <Award className="w-4 h-4" />
        </span>
        <span>Final Academic Interpretation & Verification</span>
      </div>

      <div className="space-y-2 relative z-10">
        <h3 className="text-base sm:text-xl font-extrabold text-[#F5F7FA]">
          <MathText text={interpretation.root_or_solution} />
        </h3>
        <div className="text-xs sm:text-sm text-[#B5C0CC] leading-relaxed">
          <MathText text={interpretation.summary} />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 pt-2 relative z-10">
        <div className="bg-[#080B10]/70 p-3.5 rounded-xl border border-white/[0.08] shadow-inner space-y-1">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#7E8A98] uppercase tracking-wider">
            <Target className="w-3.5 h-3.5 text-[#38D9E8]" />
            <span>Convergence Reason</span>
          </div>
          <span className="font-mono text-xs font-bold text-[#F5F7FA] block pt-1">
            <MathText text={interpretation.stopping_reason} />
          </span>
        </div>

        <div className="bg-[#080B10]/70 p-3.5 rounded-xl border border-white/[0.08] shadow-inner space-y-1">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#7E8A98] uppercase tracking-wider">
            <ListChecks className="w-3.5 h-3.5 text-[#16B8B0]" />
            <span>Steps Required</span>
          </div>
          <span className="font-mono text-xs font-bold text-[#F5F7FA] block pt-1">
            {interpretation.iterations_count} iterations
          </span>
        </div>

        <div className="bg-[#080B10]/70 p-3.5 rounded-xl border border-white/[0.08] shadow-inner space-y-1">
          <div className="flex items-center space-x-1.5 text-xs font-semibold text-[#7E8A98] uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Accuracy Bound</span>
          </div>
          <span className="font-mono text-xs font-bold text-[#F5F7FA] block pt-1">
            <MathText text={interpretation.accuracy_achieved} />
          </span>
        </div>
      </div>

      {/* Verification Details */}
      {interpretation.verification && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-xs text-[#B5C0CC] flex items-start space-x-3 relative z-10">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <span className="font-bold text-emerald-300 uppercase tracking-wider text-[11px] block">
              Solution Verification:
            </span>
            <div className="leading-relaxed">
              <MathText text={interpretation.verification} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
