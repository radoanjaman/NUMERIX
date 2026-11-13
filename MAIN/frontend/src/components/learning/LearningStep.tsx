"use client";

import React, { useState } from "react";
import { SolutionStep } from "@/lib/api";
import { MathText } from "@/components/math-view";
import { SubstitutionBlock } from "./SubstitutionBlock";
import { CalculationBlock } from "./CalculationBlock";
import { DecisionCard } from "./DecisionCard";
import { MatrixTransformation } from "./MatrixTransformation";
import { VariableDefinitions } from "./VariableDefinitions";
import { KnowledgeCheck } from "./KnowledgeCheck";
import { 
  ChevronDown, 
  ChevronUp, 
  ExternalLink, 
  BookOpen, 
  Calculator, 
  HelpCircle,
  Sparkles
} from "lucide-react";

interface LearningStepProps {
  step: SolutionStep;
  isActive?: boolean;
  isWorkedExample?: boolean;
  onJumpToIteration?: (iterationNumber: number) => void;
}

export function LearningStep({
  step,
  isActive = false,
  isWorkedExample = false,
  onJumpToIteration,
}: LearningStepProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [showFormula, setShowFormula] = useState(true);
  const [showCalculation, setShowCalculation] = useState(true);
  const [showDecision, setShowDecision] = useState(true);

  const getStepBadge = (type: string) => {
    switch (type) {
      case "concept":
        return { label: "Concept", bg: "bg-purple-500/15 text-purple-300 border-purple-500/30" };
      case "calculation":
        return { label: isWorkedExample ? "Worked Iteration" : "Calculation", bg: "bg-[#38D9E8]/15 text-[#38D9E8] border-[#38D9E8]/30" };
      case "matrix_operation":
        return { label: "Matrix Operation", bg: "bg-sky-500/15 text-sky-300 border-sky-500/30" };
      case "convergence":
        return { label: "Convergence", bg: "bg-[#FF793F]/15 text-[#FFAD66] border-[#FF793F]/30" };
      case "conclusion":
        return { label: "Conclusion", bg: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30" };
      default:
        return { label: type, bg: "bg-white/[0.06] text-[#B5C0CC] border-white/[0.12]" };
    }
  };

  const badge = getStepBadge(step.step_type);

  return (
    <div
      id={`lesson-step-${step.step_number}`}
      className={`glass-panel rounded-2xl border transition-all relative overflow-hidden ${
        isWorkedExample
          ? "border-[#38D9E8]/70 shadow-[0_0_30px_rgba(56,217,232,0.2)] ring-1 ring-[#38D9E8]/50 bg-[#111820]/80"
          : isActive
          ? "border-[#38D9E8]/60 shadow-[0_0_25px_rgba(56,217,232,0.15)] ring-1 ring-[#38D9E8]/40"
          : "border-white/[0.10] shadow-lg hover:border-white/[0.20]"
      }`}
    >
      {/* Top subtle reflection */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

      {/* Header */}
      <div className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/[0.08]">
        <div className="flex items-start space-x-3.5">
          <span className={`w-8 h-8 rounded-xl font-mono text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 shadow-sm ${
            isWorkedExample
              ? "bg-gradient-to-br from-[#16B8B0] to-[#38D9E8] text-[#080B10] shadow-[0_0_12px_rgba(56,217,232,0.4)]"
              : "bg-gradient-to-br from-white/[0.15] to-white/[0.05] border border-white/[0.15] text-[#F5F7FA]"
          }`}>
            {isWorkedExample ? <Sparkles className="w-4 h-4 fill-current" /> : step.step_number}
          </span>
          <div className="space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${badge.bg}`}>
                {badge.label}
              </span>
              {step.concept && (
                <span className="text-[11px] text-[#7E8A98] font-medium">
                  • <MathText text={step.concept} />
                </span>
              )}
            </div>
            <h3 className="text-sm sm:text-base font-bold text-[#F5F7FA] tracking-tight">
              <MathText text={step.title} />
            </h3>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-2 shrink-0 self-end sm:self-center">
          {step.related_iteration !== null && step.related_iteration !== undefined && onJumpToIteration && (
            <button
              type="button"
              onClick={() => onJumpToIteration(step.related_iteration!)}
              className="flex items-center space-x-1.5 text-xs text-[#38D9E8] hover:text-white bg-[#38D9E8]/10 hover:bg-[#38D9E8]/20 border border-[#38D9E8]/30 font-semibold px-3 py-1.5 rounded-xl transition-all cursor-pointer backdrop-blur-md"
              title={`Jump to Iteration ${step.related_iteration} in Table`}
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span>Jump to Iteration {step.related_iteration}</span>
            </button>
          )}

          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-xl text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.06] border border-transparent hover:border-white/[0.10] transition-colors cursor-pointer"
            aria-label={isExpanded ? "Collapse step" : "Expand step"}
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Content Body */}
      {isExpanded && (
        <div className="p-4 sm:p-5 space-y-4">
          {/* Main Conceptual Explanation */}
          {step.explanation && (
            <div className="text-xs sm:text-sm text-[#B5C0CC] leading-relaxed">
              <MathText text={step.explanation} />
            </div>
          )}

          {/* Toggle pills */}
          <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-white/[0.06]">
            {step.formula_latex && (
              <button
                type="button"
                onClick={() => setShowFormula(!showFormula)}
                className={`text-[11px] font-semibold px-2.5 py-1 rounded-lg border transition-colors cursor-pointer flex items-center space-x-1.5 ${
                  showFormula ? "bg-[#38D9E8]/15 text-[#38D9E8] border-[#38D9E8]/30" : "bg-white/[0.04] text-[#7E8A98] border-white/[0.08]"
                }`}
              >
                <BookOpen className="w-3 h-3" />
                <span>{showFormula ? "Hide Formula" : "Show Formula"}</span>
              </button>
            )}

            {(step.calculation_latex || step.result_latex || (step.substeps && step.substeps.length > 0)) && (
              <button
                type="button"
                onClick={() => setShowCalculation(!showCalculation)}
                className={`text-[11px] font-semibold px-2.5 py-1 rounded-lg border transition-colors cursor-pointer flex items-center space-x-1.5 ${
                  showCalculation ? "bg-[#16B8B0]/15 text-[#38D9E8] border-[#16B8B0]/30" : "bg-white/[0.04] text-[#7E8A98] border-white/[0.08]"
                }`}
              >
                <Calculator className="w-3 h-3" />
                <span>{showCalculation ? "Hide Calculation" : "Show Calculation"}</span>
              </button>
            )}

            {step.decision && (
              <button
                type="button"
                onClick={() => setShowDecision(!showDecision)}
                className={`text-[11px] font-semibold px-2.5 py-1 rounded-lg border transition-colors cursor-pointer flex items-center space-x-1.5 ${
                  showDecision ? "bg-[#FF793F]/15 text-[#FFAD66] border-[#FF793F]/30" : "bg-white/[0.04] text-[#7E8A98] border-white/[0.08]"
                }`}
              >
                <HelpCircle className="w-3 h-3" />
                <span>{showDecision ? "Hide Decision" : "Explain Why"}</span>
              </button>
            )}
          </div>

          {/* Formula & Substitution Card */}
          {showFormula && (step.formula_latex || step.substitution_latex) && (
            <SubstitutionBlock
              formulaLatex={step.formula_latex}
              substitutionLatex={step.substitution_latex}
            />
          )}

          {/* Matrix Transformation Snapshot for linear systems */}
          {step.matrix_snapshot && (
            <MatrixTransformation
              matrix={step.matrix_snapshot}
              operationDescription={step.related_operation}
            />
          )}

          {/* Detailed Calculations Block */}
          {showCalculation && (step.calculation_latex || step.result_latex || (step.substeps && step.substeps.length > 0)) && (
            <CalculationBlock
              calculationLatex={step.calculation_latex}
              resultLatex={step.result_latex}
              substeps={step.substeps}
            />
          )}

          {/* Decision Rationale */}
          {showDecision && step.decision && (
            <DecisionCard decision={step.decision} concept={step.concept} />
          )}

          {/* Variable definitions */}
          {step.variable_definitions && step.variable_definitions.length > 0 && (
            <VariableDefinitions variables={step.variable_definitions} />
          )}

          {/* Checkpoint Question inside this step */}
          {step.checkpoint_question && (
            <div className="pt-2">
              <KnowledgeCheck question={step.checkpoint_question} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
