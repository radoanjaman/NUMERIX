"use client";

import React, { useState } from "react";
import { KnowledgeCheckQuestion } from "@/lib/api";
import { MathText } from "@/components/math-view";
import { 
  CheckCircle2, 
  XCircle, 
  RotateCcw, 
  Lightbulb, 
  Sparkles 
} from "lucide-react";

interface KnowledgeCheckProps {
  question: KnowledgeCheckQuestion;
  onAnswered?: (isCorrect: boolean) => void;
}

export function KnowledgeCheck({ question, onAnswered }: KnowledgeCheckProps) {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const isCorrect = selectedIdx === question.correct_index;

  const handleSubmit = () => {
    if (selectedIdx === null) return;
    setSubmitted(true);
    if (onAnswered) onAnswered(isCorrect);
  };

  const handleRetry = () => {
    setSelectedIdx(null);
    setSubmitted(false);
    setShowHint(false);
  };

  return (
    <div className="glass-card rounded-2xl p-5 sm:p-6 border border-white/[0.14] bg-[#111820]/70 space-y-4 shadow-xl relative overflow-hidden">
      {/* Top subtle reflection */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="p-1.5 rounded-lg bg-[#FF793F]/15 text-[#FFAD66] border border-[#FF793F]/30">
            <Sparkles className="w-4 h-4" />
          </span>
          <span className="text-xs font-bold text-[#FFAD66] uppercase tracking-wider">
            Knowledge Check ({question.question_type})
          </span>
        </div>
        {question.hint && (
          <button
            type="button"
            onClick={() => setShowHint(!showHint)}
            className="flex items-center space-x-1.5 text-[11px] text-[#B5C0CC] hover:text-[#F5F7FA] bg-white/[0.04] hover:bg-white/[0.08] px-2.5 py-1 rounded-lg border border-white/[0.08] transition-colors cursor-pointer"
          >
            <Lightbulb className="w-3.5 h-3.5 text-[#FFAD66]" />
            <span>{showHint ? "Hide Hint" : "Need a Hint?"}</span>
          </button>
        )}
      </div>

      {/* Hint Alert */}
      {showHint && question.hint && (
        <div className="p-3 rounded-xl bg-[#FF793F]/10 border border-[#FF793F]/25 text-xs text-[#FFAD66] flex items-start space-x-2.5">
          <Lightbulb className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
          <MathText text={question.hint} />
        </div>
      )}

      {/* Question Prompt */}
      <div className="text-sm font-semibold text-[#F5F7FA] leading-snug">
        <MathText text={question.question} />
      </div>

      {/* Options List */}
      <div className="space-y-2.5">
        {question.options.map((option, idx) => {
          let btnStyle = "border-white/[0.10] bg-white/[0.03] hover:bg-white/[0.06] text-[#B5C0CC]";
          let dotColor = "border-white/20";

          if (selectedIdx === idx) {
            btnStyle = "border-[#38D9E8]/80 bg-[#38D9E8]/15 text-[#F5F7FA] shadow-[0_0_15px_rgba(56,217,232,0.15)] ring-1 ring-[#38D9E8]";
            dotColor = "border-[#38D9E8] bg-[#38D9E8]";
          }

          if (submitted) {
            if (idx === question.correct_index) {
              btnStyle = "border-emerald-500/80 bg-emerald-500/15 text-emerald-200 font-semibold ring-1 ring-emerald-500";
              dotColor = "border-emerald-400 bg-emerald-400";
            } else if (selectedIdx === idx && !isCorrect) {
              btnStyle = "border-[#FF793F]/80 bg-[#FF793F]/15 text-[#FFAD66] font-medium ring-1 ring-[#FF793F]";
              dotColor = "border-[#FF793F] bg-[#FF793F]";
            } else {
              btnStyle = "opacity-40 border-white/[0.06] bg-transparent text-[#7E8A98]";
            }
          }

          return (
            <button
              key={idx}
              type="button"
              disabled={submitted}
              onClick={() => setSelectedIdx(idx)}
              className={`w-full text-left p-3.5 rounded-xl border transition-all text-xs flex items-center justify-between gap-3 cursor-pointer ${btnStyle}`}
            >
              <div className="flex items-center space-x-3">
                <span className={`w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${dotColor}`}>
                  {selectedIdx === idx && !submitted && (
                    <span className="w-2 h-2 rounded-full bg-[#38D9E8]" />
                  )}
                </span>
                <div>
                  <MathText text={option} />
                </div>
              </div>
              {submitted && idx === question.correct_index && (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              )}
              {submitted && selectedIdx === idx && !isCorrect && (
                <XCircle className="w-4 h-4 text-[#FF793F] shrink-0" />
              )}
            </button>
          );
        })}
      </div>

      {/* Submission Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-white/[0.08]">
        {!submitted ? (
          <button
            type="button"
            disabled={selectedIdx === null}
            onClick={handleSubmit}
            className="btn-glass-primary text-xs font-bold px-4 py-2 rounded-xl cursor-pointer disabled:opacity-40"
          >
            Check Answer
          </button>
        ) : (
          <div className="flex items-center justify-between w-full">
            <span className={`text-xs font-bold ${isCorrect ? "text-emerald-400" : "text-[#FF793F]"}`}>
              {isCorrect ? "✓ Correct! Well done." : "✗ Incorrect. Review the explanation below."}
            </span>
            <button
              type="button"
              onClick={handleRetry}
              className="flex items-center space-x-1.5 text-xs text-[#B5C0CC] hover:text-[#F5F7FA] bg-white/[0.06] hover:bg-white/[0.10] border border-white/[0.12] px-3 py-1.5 rounded-xl transition-all cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}
      </div>

      {/* Explanation when submitted */}
      {submitted && (
        <div className="p-3.5 rounded-xl bg-white/[0.04] border border-white/[0.08] text-xs text-[#B5C0CC] space-y-1">
          <span className="font-bold text-[#F5F7FA] uppercase tracking-wider text-[10px] block">
            Mathematical Explanation:
          </span>
          <div className="leading-relaxed">
            <MathText text={question.explanation} />
          </div>
        </div>
      )}
    </div>
  );
}
