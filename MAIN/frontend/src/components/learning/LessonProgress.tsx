"use client";

import React from "react";
import { ChevronLeft, ChevronRight, Check } from "lucide-react";

interface LessonProgressProps {
  currentStep: number; // 1-based index
  totalSteps: number;
  onStepChange: (step: number) => void;
}

export function LessonProgress({
  currentStep,
  totalSteps,
  onStepChange,
}: LessonProgressProps) {
  const percentage = Math.round((currentStep / Math.max(totalSteps, 1)) * 100);

  return (
    <div className="glass-panel rounded-2xl p-4 sm:p-5 border border-white/[0.12] shadow-xl space-y-3.5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="space-y-0.5">
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-[#F5F7FA] uppercase tracking-wider">
              Lesson Progress: Step {currentStep} of {totalSteps}
            </span>
            <span className="text-xs font-mono font-semibold text-[#38D9E8]">
              ({percentage}%)
            </span>
          </div>
          <p className="text-[11px] text-[#7E8A98]">
            Follow the mathematical derivation sequentially or jump between worked stages.
          </p>
        </div>

        {/* Navigation Controls */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            type="button"
            disabled={currentStep <= 1}
            onClick={() => onStepChange(currentStep - 1)}
            className="flex items-center space-x-1.5 bg-white/[0.05] hover:bg-white/[0.10] disabled:opacity-30 text-[#B5C0CC] hover:text-[#F5F7FA] text-xs font-semibold px-3 py-1.5 rounded-xl border border-white/[0.10] shadow-sm transition-all cursor-pointer backdrop-blur-md"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            <span>Prev Step</span>
          </button>
          <button
            type="button"
            disabled={currentStep >= totalSteps}
            onClick={() => onStepChange(currentStep + 1)}
            className="flex items-center space-x-1.5 btn-glass-primary disabled:opacity-30 text-xs font-semibold px-3.5 py-1.5 rounded-xl shadow-sm transition-all cursor-pointer"
          >
            <span>Next Step</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-white/[0.06] rounded-full h-2 overflow-hidden border border-white/[0.08]">
        <div
          className="bg-gradient-to-r from-[#16B8B0] via-[#38D9E8] to-[#4B9DFF] h-2 rounded-full transition-all duration-300 shadow-[0_0_10px_rgba(56,217,232,0.5)]"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Step Pills Scroller */}
      {totalSteps <= 25 && (
        <div className="flex items-center space-x-2 overflow-x-auto py-1 scrollbar-thin">
          {Array.from({ length: totalSteps }, (_, i) => i + 1).map((stepNum) => {
            const isCurrent = stepNum === currentStep;
            const isPassed = stepNum < currentStep;

            return (
              <button
                key={stepNum}
                type="button"
                onClick={() => onStepChange(stepNum)}
                className={`w-7 h-7 rounded-lg text-xs font-mono font-bold flex items-center justify-center shrink-0 transition-all cursor-pointer ${
                  isCurrent
                    ? "bg-[#38D9E8] text-[#080B10] shadow-[0_0_12px_rgba(56,217,232,0.6)] scale-105"
                    : isPassed
                    ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30"
                    : "bg-white/[0.04] text-[#7E8A98] border border-white/[0.08] hover:bg-white/[0.08] hover:text-[#F5F7FA]"
                }`}
                title={`Jump to Step ${stepNum}`}
              >
                {isPassed ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : stepNum}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
