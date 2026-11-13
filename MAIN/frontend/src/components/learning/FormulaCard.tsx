"use client";

import React, { useState } from "react";
import { FormulaCardModel } from "@/lib/api";
import { MathView, MathText } from "@/components/math-view";
import { VariableDefinitions } from "./VariableDefinitions";
import { ChevronDown, ChevronUp, FunctionSquare, Info } from "lucide-react";

interface FormulaCardProps {
  formula: FormulaCardModel;
  defaultExpanded?: boolean;
}

export function FormulaCard({ formula, defaultExpanded = false }: FormulaCardProps) {
  const [showVars, setShowVars] = useState(defaultExpanded);

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-white/[0.12] shadow-lg hover:border-white/[0.20] transition-all space-y-3 relative overflow-hidden">
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="p-1.5 rounded-lg bg-[#38D9E8]/10 text-[#38D9E8] border border-[#38D9E8]/20">
              <FunctionSquare className="w-4 h-4" />
            </span>
            <h4 className="text-sm font-bold text-[#F5F7FA] tracking-tight">{formula.name}</h4>
          </div>
          <div className="text-xs text-[#7E8A98] leading-relaxed">
            <MathText text={formula.description} />
          </div>
        </div>

        {formula.variables && formula.variables.length > 0 && (
          <button
            type="button"
            onClick={() => setShowVars(!showVars)}
            className="flex items-center space-x-1.5 text-xs text-[#B5C0CC] hover:text-[#F5F7FA] bg-white/[0.04] hover:bg-white/[0.08] px-2.5 py-1.5 rounded-xl border border-white/[0.08] transition-colors cursor-pointer shrink-0"
          >
            <Info className="w-3.5 h-3.5 text-[#38D9E8]" />
            <span>{showVars ? "Hide Vars" : "Variables"}</span>
            {showVars ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
          </button>
        )}
      </div>

      {/* Mathematical Formula Display */}
      <div className="bg-[#080B10]/80 rounded-xl p-4 text-center border border-white/[0.08] shadow-inner overflow-x-auto">
        <MathView math={formula.latex} display className="text-[#F5F7FA] text-base sm:text-lg" />
      </div>

      {/* Expandable Variable Definitions */}
      {showVars && formula.variables && formula.variables.length > 0 && (
        <div className="pt-1">
          <VariableDefinitions variables={formula.variables} title={`${formula.name} Variables`} />
        </div>
      )}
    </div>
  );
}
