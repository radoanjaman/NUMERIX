"use client";

import React from "react";
import { VariableDefinition } from "@/lib/api";
import { MathView, MathText } from "@/components/math-view";

interface VariableDefinitionsProps {
  variables: VariableDefinition[];
  title?: string;
}

export function VariableDefinitions({ variables, title = "Variable & Parameter Definitions" }: VariableDefinitionsProps) {
  if (!variables || variables.length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-white/[0.12] space-y-3">
      <div className="text-xs font-semibold text-[#38D9E8] uppercase tracking-wider flex items-center justify-between">
        <span>{title}</span>
        <span className="text-[10px] text-[#7E8A98] font-mono">({variables.length} defined)</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
        {variables.map((v, i) => (
          <div
            key={i}
            className="flex items-start space-x-2.5 bg-[#080B10]/60 p-2.5 rounded-xl border border-white/[0.08] shadow-inner"
          >
            <div className="font-mono font-bold text-[#38D9E8] shrink-0 min-w-8 pt-0.5">
              <MathView math={v.symbol} />
            </div>
            <div className="space-y-0.5 flex-1 min-w-0">
              <div className="flex items-center justify-between">
                <span className="font-medium text-[#F5F7FA] truncate">{v.name}</span>
                {v.current_value !== undefined && v.current_value !== null && (
                  <span className="font-mono text-[11px] bg-white/[0.08] px-2 py-0.5 rounded-md text-[#38D9E8] ml-1 shrink-0 border border-white/[0.10]">
                    = {v.current_value}
                  </span>
                )}
              </div>
              <div className="text-[11px] text-[#7E8A98] line-clamp-2">
                <MathText text={v.description} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
