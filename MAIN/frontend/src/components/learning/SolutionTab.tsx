"use client";

import React, { useState } from "react";
import { SolutionDocument, IterationItem } from "@/lib/api";
import { MathText } from "@/components/math-view";
import { FormulaCard } from "./FormulaCard";
import { LearningStep } from "./LearningStep";
import { FinalInterpretation } from "./FinalInterpretation";
import { KnowledgeCheck } from "./KnowledgeCheck";
import { StepTable } from "@/components/step-table";
import { 
  BookOpen, 
  GraduationCap, 
  Target, 
  ChevronDown, 
  ChevronUp, 
  Sparkles,
  RefreshCw,
  Table as TableIcon,
  Layers,
  ArrowRight
} from "lucide-react";

interface SolutionTabProps {
  document: SolutionDocument;
  iterations?: IterationItem[];
  currentStep?: number;
  onStepChange?: (step: number) => void;
  onJumpToIteration?: (iterationNumber: number) => void;
}

export function SolutionTab({
  document,
  iterations,
  onJumpToIteration,
}: SolutionTabProps) {
  const [showFullHistory, setShowFullHistory] = useState(false);
  const [showTheory, setShowTheory] = useState(false);
  const [showAllSteps, setShowAllSteps] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);

  // Identify the representative worked iteration (Iteration 1 or first calculation)
  const workedStep =
    document.worked_step ||
    document.steps.find((s) => s.related_iteration === 1 && s.step_type === "calculation") ||
    document.steps.find((s) => s.step_type === "calculation" || s.step_type === "matrix_operation") ||
    document.steps[0];

  // Essential primary formula
  const essentialFormula =
    document.essential_formula ||
    (document.formulas && document.formulas.length > 0 ? document.formulas[0] : null);

  // Recurrence explanation
  const whatChangesNext =
    document.what_changes_next ||
    "The same governing formula is applied repeatedly using the latest updated values. Each iteration refines the solution until the error satisfies the tolerance.";

  // Available iterations from prop or step records
  const resolvedIterations: IterationItem[] =
    iterations && iterations.length > 0
      ? iterations
      : document.steps
          .filter((s) => s.related_iteration !== null && s.related_iteration !== undefined)
          .map((s) => ({
            n: s.related_iteration!,
            values: {
              step: s.related_iteration,
              result: s.result_latex || "",
            },
          }));

  const visibleIterations = showFullHistory
    ? resolvedIterations
    : resolvedIterations.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* 1. METHOD HEADER */}
      <div className="glass-panel rounded-2xl p-5 sm:p-6 border border-white/[0.14] shadow-2xl space-y-3 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-[#38D9E8]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        <div className="flex flex-wrap items-center justify-between gap-2.5 relative z-10">
          <div className="flex items-center space-x-2.5">
            <span className="p-2 rounded-xl bg-gradient-to-br from-[#16B8B0] to-[#38D9E8] text-[#080B10] shadow-[0_0_15px_rgba(56,217,232,0.4)]">
              <GraduationCap className="w-4 h-4 font-bold" />
            </span>
            <span className="text-xs font-bold text-[#38D9E8] uppercase tracking-wider">
              {document.topic} • Worked Numerical Example
            </span>
          </div>
          <span className="text-xs font-mono bg-white/[0.06] text-[#38D9E8] px-3 py-1 rounded-xl border border-white/[0.12] backdrop-blur-md">
            {document.method}
          </span>
        </div>

        <div className="relative z-10 space-y-1.5">
          <h2 className="text-xl sm:text-2xl font-extrabold text-[#F5F7FA] tracking-tight">
            {document.method}
          </h2>
          {document.one_sentence_purpose && (
            <div className="text-xs sm:text-sm font-medium text-[#38D9E8]">
              <MathText text={document.one_sentence_purpose} />
            </div>
          )}
          <div className="text-xs sm:text-sm text-[#B5C0CC] leading-relaxed pt-1">
            <span className="font-semibold text-[#F5F7FA]">Problem: </span>
            <MathText text={document.problem_statement} />
          </div>
        </div>
      </div>

      {/* 2. ESSENTIAL FORMULA */}
      {essentialFormula && (
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs font-bold text-[#F5F7FA] uppercase tracking-wider">
            <BookOpen className="w-4 h-4 text-[#38D9E8]" />
            <span>Essential Governing Formula</span>
          </div>
          <FormulaCard formula={essentialFormula} defaultExpanded={false} />
        </div>
      )}

      {/* 3. FIRST ITERATION — STEP-BY-STEP (WORKED REPRESENTATIVE EXAMPLE) */}
      {workedStep && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-xs font-bold text-[#38D9E8] uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-[#16B8B0]" />
              <span>Worked Representative Iteration</span>
            </div>
            <span className="text-[11px] text-[#7E8A98] font-mono">
              Complete derivation with actual calculated values
            </span>
          </div>

          <LearningStep
            step={workedStep}
            isActive={true}
            isWorkedExample={true}
            onJumpToIteration={onJumpToIteration}
          />
        </div>
      )}

      {/* 4. WHAT CHANGES IN THE NEXT ITERATIONS? */}
      <div className="glass-panel rounded-2xl p-4 sm:p-5 border border-[#38D9E8]/30 bg-[#38D9E8]/5 shadow-xl space-y-2 relative overflow-hidden">
        <div className="flex items-center space-x-2 text-xs font-bold text-[#38D9E8] uppercase tracking-wider">
          <RefreshCw className="w-4 h-4 text-[#16B8B0]" />
          <span>What Changes in Subsequent Iterations?</span>
        </div>
        <div className="text-xs sm:text-sm text-[#B5C0CC] leading-relaxed pl-1">
          <MathText text={whatChangesNext} />
        </div>
        {document.remaining_iterations_summary && (
          <div className="text-[11px] text-[#7E8A98] font-mono pl-1 pt-1 border-t border-white/[0.06]">
            <MathText text={document.remaining_iterations_summary} />
          </div>
        )}
      </div>

      {/* 5. ITERATION HISTORY (COMPACT TABLE WITH PROGRESSIVE DISCLOSURE) */}
      {resolvedIterations.length > 0 && (
        <div className="glass-panel rounded-2xl p-4 sm:p-5 border border-white/[0.12] shadow-xl space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/[0.08] pb-3">
            <div className="flex items-center space-x-2">
              <TableIcon className="w-4 h-4 text-[#38D9E8]" />
              <h3 className="text-xs font-bold text-[#F5F7FA] uppercase tracking-wider">
                Iteration History Table ({resolvedIterations.length} Total)
              </h3>
            </div>
            {resolvedIterations.length > 5 && (
              <button
                type="button"
                onClick={() => setShowFullHistory(!showFullHistory)}
                className="text-xs text-[#38D9E8] hover:text-white font-semibold transition-colors cursor-pointer flex items-center space-x-1"
              >
                <span>{showFullHistory ? "Show First 5 Only" : `Expand All (${resolvedIterations.length} Iterations)`}</span>
                {showFullHistory ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
            )}
          </div>

          <StepTable
            iterations={visibleIterations}
            method={document.method}
            highlightedIteration={1}
          />
        </div>
      )}

      {/* 6. FINAL ACADEMIC INTERPRETATION */}
      {document.final_interpretation && (
        <FinalInterpretation
          interpretation={document.final_interpretation}
          methodName={document.method}
        />
      )}

      {/* 7. PROGRESSIVE DISCLOSURE ACCORDIONS (THEORY, ALL STEPS, QUIZ) */}
      <div className="space-y-3 pt-2">
        {/* Accordion A: Detailed Theory & Prerequisites */}
        {(document.learning_objectives.length > 0 || document.prerequisites.length > 0) && (
          <div className="glass-panel rounded-2xl border border-white/[0.10] overflow-hidden shadow-md">
            <button
              type="button"
              onClick={() => setShowTheory(!showTheory)}
              className="w-full p-4 flex items-center justify-between text-left hover:bg-white/[0.03] transition-colors cursor-pointer"
            >
              <div className="flex items-center space-x-2.5">
                <Target className="w-4 h-4 text-[#7E8A98]" />
                <span className="text-xs font-bold text-[#B5C0CC] tracking-tight uppercase">
                  Optional: Learning Objectives & Prerequisites
                </span>
              </div>
              {showTheory ? <ChevronUp className="w-4 h-4 text-[#7E8A98]" /> : <ChevronDown className="w-4 h-4 text-[#7E8A98]" />}
            </button>

            {showTheory && (
              <div className="p-4 pt-0 border-t border-white/[0.06] grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                <div className="space-y-2">
                  <span className="text-xs font-bold text-[#38D9E8] uppercase tracking-wider block">
                    Learning Objectives:
                  </span>
                  <ul className="space-y-1.5 text-xs text-[#B5C0CC]">
                    {document.learning_objectives.map((obj, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-[#16B8B0] font-bold">•</span>
                        <div><MathText text={obj} /></div>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="space-y-2">
                  <span className="text-xs font-bold text-[#FFAD66] uppercase tracking-wider block">
                    Mathematical Prerequisites:
                  </span>
                  <ul className="space-y-1.5 text-xs text-[#B5C0CC]">
                    {document.prerequisites.map((req, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-[#FF793F] font-bold">•</span>
                        <div><MathText text={req} /></div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Accordion B: Full Derivation Steps Stream */}
        {document.steps.length > 1 && (
          <div className="glass-panel rounded-2xl border border-white/[0.10] overflow-hidden shadow-md">
            <button
              type="button"
              onClick={() => setShowAllSteps(!showAllSteps)}
              className="w-full p-4 flex items-center justify-between text-left hover:bg-white/[0.03] transition-colors cursor-pointer"
            >
              <div className="flex items-center space-x-2.5">
                <Layers className="w-4 h-4 text-[#7E8A98]" />
                <span className="text-xs font-bold text-[#B5C0CC] tracking-tight uppercase">
                  Optional: Inspect Full Multi-Step Derivation ({document.steps.length} Steps)
                </span>
              </div>
              {showAllSteps ? <ChevronUp className="w-4 h-4 text-[#7E8A98]" /> : <ChevronDown className="w-4 h-4 text-[#7E8A98]" />}
            </button>

            {showAllSteps && (
              <div className="p-4 pt-0 border-t border-white/[0.06] space-y-4 mt-2">
                {document.steps.map((step) => (
                  <LearningStep
                    key={step.step_number}
                    step={step}
                    isActive={false}
                    onJumpToIteration={onJumpToIteration}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Accordion C: Practice Questions */}
        {document.practice_questions && document.practice_questions.length > 0 && (
          <div className="glass-panel rounded-2xl border border-white/[0.10] overflow-hidden shadow-md">
            <button
              type="button"
              onClick={() => setShowQuiz(!showQuiz)}
              className="w-full p-4 flex items-center justify-between text-left hover:bg-white/[0.03] transition-colors cursor-pointer"
            >
              <div className="flex items-center space-x-2.5">
                <Sparkles className="w-4 h-4 text-[#FF793F]" />
                <span className="text-xs font-bold text-[#B5C0CC] tracking-tight uppercase">
                  Practice Questions: Test Your Understanding ({document.practice_questions.length} Questions)
                </span>
              </div>
              {showQuiz ? <ChevronUp className="w-4 h-4 text-[#7E8A98]" /> : <ChevronDown className="w-4 h-4 text-[#7E8A98]" />}
            </button>

            {showQuiz && (
              <div className="p-4 pt-0 border-t border-white/[0.06] space-y-4 mt-2">
                {document.practice_questions.map((q) => (
                  <KnowledgeCheck key={q.id} question={q} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
