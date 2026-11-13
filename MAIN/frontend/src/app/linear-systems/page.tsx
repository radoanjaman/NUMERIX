"use client";

import React, { useState } from "react";
import { 
  Play, 
  RotateCcw, 
  AlertCircle, 
  Table, 
  BarChart3,
  GraduationCap,
  ArrowLeft
} from "lucide-react";
import { MetricCard } from "@/components/metric-card";
import { StepTable } from "@/components/step-table";
import { InteractiveChart } from "@/components/interactive-chart";
import { SolutionTab } from "@/components/learning";
import { MathText } from "@/components/math-view";
import { solveLinearSystem, SolverAPIResponse } from "@/lib/api";

const DEFAULT_3X3_A = [
  [2.0, 1.0, 1.0],
  [1.0, 3.0, 1.0],
  [1.0, 1.0, 4.0],
];
const DEFAULT_3X3_B = [8.0, 10.0, 15.0];

export default function LinearSystemsPage() {
  const [method, setMethod] = useState<"gauss_elimination" | "gauss_jordan">("gauss_elimination");
  const [n, setN] = useState<number>(3);
  const [matrixA, setMatrixA] = useState<number[][]>(DEFAULT_3X3_A);
  const [vectorB, setVectorB] = useState<number[]>(DEFAULT_3X3_B);

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<SolverAPIResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"solution" | "operations" | "chart">("solution");
  const [highlightedIteration, setHighlightedIteration] = useState<number | null>(null);
  const [lessonStep, setLessonStep] = useState(1);

  const handleDimChange = (newN: number) => {
    if (newN < 2 || newN > 6) return;
    setN(newN);
    const newA: number[][] = [];
    const newB: number[] = [];
    for (let i = 0; i < newN; i++) {
      const row: number[] = [];
      for (let j = 0; j < newN; j++) {
        row.push(matrixA[i]?.[j] ?? (i === j ? 2.0 : 1.0));
      }
      newA.push(row);
      newB.push(vectorB[i] ?? (i + 1) * 5.0);
    }
    setMatrixA(newA);
    setVectorB(newB);
    setResult(null);
  };

  const updateCellA = (r: number, c: number, val: string) => {
    const parsed = parseFloat(val) || 0;
    const copy = matrixA.map((row) => [...row]);
    copy[r][c] = parsed;
    setMatrixA(copy);
  };

  const updateCellB = (r: number, val: string) => {
    const parsed = parseFloat(val) || 0;
    const copy = [...vectorB];
    copy[r] = parsed;
    setVectorB(copy);
  };

  const handleRun = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const res = await solveLinearSystem({
        method,
        A: matrixA,
        b: vectorB,
      });
      setResult(res);
      if (!res.success) {
        setErrorMsg(`Matrix solver status '${res.status}': ${res.termination_reason}`);
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to solve linear system.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setN(3);
    setMatrixA(DEFAULT_3X3_A);
    setVectorB(DEFAULT_3X3_B);
    setResult(null);
    setErrorMsg(null);
  };

  return (
    <div className="space-y-6 py-4">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
          Linear Systems Laboratory
        </h1>
        <div className="text-sm text-[#7E8A98] mt-1">
          <MathText text="Solve systems $A x = b$ with partial pivoting row operations and residual verification." />
        </div>
      </div>

      {/* Main Solver Card */}
      <div className="glass-panel p-5 sm:p-7 rounded-2xl border border-white/[0.14] shadow-2xl space-y-6 relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        {/* Method & Dimension Selector */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/[0.08]">
          <div className="flex items-center space-x-2.5">
            {[
              { id: "gauss_elimination", label: "Gaussian Elimination", desc: "Partial Pivoting" },
              { id: "gauss_jordan", label: "Gauss-Jordan", desc: "Full RREF" },
            ].map((m) => {
              const isSel = method === m.id;
              return (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setMethod(m.id as any)}
                  className={`px-4 py-2.5 rounded-xl text-xs font-semibold transition-all cursor-pointer backdrop-blur-md ${
                    isSel
                      ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/50 shadow-[0_0_15px_rgba(56,217,232,0.25)] font-bold"
                      : "bg-white/[0.04] text-[#B5C0CC] hover:bg-white/[0.08] hover:text-[#F5F7FA] border border-white/[0.08]"
                  }`}
                >
                  <span>{m.label}</span>
                  <span className={`ml-1.5 text-[10px] ${isSel ? "text-[#38D9E8]" : "text-[#7E8A98]"}`}>
                    • {m.desc}
                  </span>
                </button>
              );
            })}
          </div>

          <div className="flex items-center space-x-2.5 self-start sm:self-auto">
            <span className="text-xs font-bold text-[#7E8A98] uppercase">Dimension N:</span>
            <div className="flex items-center space-x-1.5">
              {[2, 3, 4, 5].map((dim) => (
                <button
                  key={dim}
                  type="button"
                  onClick={() => handleDimChange(dim)}
                  className={`w-8 h-8 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                    n === dim
                      ? "bg-[#38D9E8] text-[#080B10] shadow-[0_0_10px_rgba(56,217,232,0.5)]"
                      : "bg-white/[0.04] text-[#B5C0CC] hover:bg-white/[0.08] hover:text-[#F5F7FA] border border-white/[0.08]"
                  }`}
                >
                  {dim}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Matrix Grid Editor */}
        <form onSubmit={handleRun} className="space-y-6">
          <div>
            <label className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider block mb-3">
              Augmented Coefficient Matrix [ A | b ]
            </label>

            <div className="overflow-x-auto p-5 bg-[#080B10]/80 rounded-2xl border border-white/[0.10] inline-block min-w-full shadow-inner">
              <div className="grid gap-2.5 items-center" style={{ gridTemplateColumns: `repeat(${n}, minmax(68px, 85px)) 24px minmax(75px, 95px)` }}>
                {/* Headers */}
                {Array.from({ length: n }).map((_, j) => (
                  <div key={j} className="text-center font-mono font-bold text-xs text-[#7E8A98]">
                    x{j + 1}
                  </div>
                ))}
                <div className="text-center font-bold text-[#FF793F] text-sm">|</div>
                <div className="text-center font-mono font-bold text-xs text-[#38D9E8]">b</div>

                {/* Rows */}
                {Array.from({ length: n }).map((_, i) => (
                  <React.Fragment key={i}>
                    {Array.from({ length: n }).map((_, j) => (
                      <input
                        key={`${i}-${j}`}
                        type="number"
                        step="any"
                        value={matrixA[i]?.[j] ?? 0}
                        onChange={(e) => updateCellA(i, j, e.target.value)}
                        className="glass-input p-2.5 text-center rounded-xl font-mono text-xs text-[#F5F7FA] font-semibold"
                      />
                    ))}
                    <div className="text-center font-bold text-[#FF793F] text-sm">|</div>
                    <input
                      type="number"
                      step="any"
                      value={vectorB[i] ?? 0}
                      onChange={(e) => updateCellB(i, e.target.value)}
                      className="glass-input p-2.5 text-center rounded-xl font-mono text-xs text-[#FFAD66] font-bold bg-[#FF793F]/10 border border-[#FF793F]/30"
                    />
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-glass-primary font-semibold text-xs sm:text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 cursor-pointer disabled:opacity-40"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{loading ? "Solving System…" : "Solve System"}</span>
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="btn-glass-secondary font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-xl flex items-center space-x-1.5 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset to Default 3×3</span>
            </button>
          </div>
        </form>

        {errorMsg && (
          <div className="p-4 rounded-xl bg-[#FF793F]/15 border border-[#FF793F]/30 text-[#FFAD66] text-xs flex items-start space-x-2.5">
            <AlertCircle className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Matrix Notice: </span>
              <span>{errorMsg}</span>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Solution Vector Box */}
          {result.solution_vector && (
            <div className="glass-panel p-6 rounded-2xl border border-white/[0.14] shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-48 h-48 bg-[#38D9E8]/10 rounded-full blur-3xl pointer-events-none" />
              <div>
                <span className="text-xs font-bold text-[#38D9E8] uppercase tracking-wider block mb-2">
                  Computed Solution Vector x:
                </span>
                <div className="flex flex-wrap gap-2.5 text-sm sm:text-base font-mono font-bold text-[#F5F7FA]">
                  {result.solution_vector.map((xVal, idx) => (
                    <span key={idx} className="bg-white/[0.06] px-3.5 py-2 rounded-xl border border-white/[0.12] shadow-sm">
                      x{idx + 1} = {xVal.toFixed(6)}
                    </span>
                  ))}
                </div>
              </div>
              <div className="text-right text-xs font-mono text-[#7E8A98]">
                Residual: {result.metrics.final_residual?.toExponential(4) ?? "0.0"}
              </div>
            </div>
          )}

          {/* Metrics Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
            <MetricCard
              label="Solver Status"
              value={result.status}
              badge={result.success ? "Solved" : "Singular"}
              color={result.success ? "rose" : "slate"}
            />
            <MetricCard
              label="Row Operations"
              value={result.metrics.iterations}
              subtext="Elimination steps"
            />
            <MetricCard
              label="Residual Norm"
              value={result.metrics.final_residual != null ? result.metrics.final_residual.toExponential(4) : "0.0"}
              subtext="||Ax - b||"
            />
            <MetricCard
              label="Execution Time"
              value={`${(result.metrics.execution_time_seconds * 1000).toFixed(2)} ms`}
              subtext="Computation time"
            />
          </div>

          {/* Tabbed Operations / Chart View */}
          <div className="glass-panel p-5 rounded-2xl border border-white/[0.12] shadow-xl space-y-4">
            <div className="flex items-center space-x-2 border-b border-white/[0.08] pb-3 overflow-x-auto">
              <button
                type="button"
                onClick={() => setActiveTab("solution")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "solution"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <GraduationCap className="w-3.5 h-3.5" />
                <span>1. Solution</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("operations")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "operations"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <Table className="w-3.5 h-3.5" />
                <span>2. Elementary Row Operations ({result.iterations.length})</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("chart")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "chart"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                <span>3. Solution Coordinates Chart</span>
              </button>
            </div>

            {/* Tab Contents */}
            {activeTab === "solution" && result.solution_document && (
              <SolutionTab
                document={result.solution_document}
                iterations={result.iterations}
                currentStep={lessonStep}
                onStepChange={setLessonStep}
                onJumpToIteration={(iterNum) => {
                  setHighlightedIteration(iterNum);
                  setActiveTab("operations");
                }}
              />
            )}

            {activeTab === "operations" && (
              <div className="space-y-3">
                {highlightedIteration !== null && (
                  <div className="flex items-center justify-between p-3 rounded-xl bg-[#38D9E8]/10 border border-[#38D9E8]/30 text-xs text-[#F5F7FA]">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-[#38D9E8]">Focus:</span>
                      <span>Highlighting Operation {highlightedIteration} from lesson.</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setActiveTab("solution")}
                      className="flex items-center space-x-1 text-xs font-semibold bg-white/[0.08] px-3 py-1.5 rounded-lg border border-white/[0.12] text-[#38D9E8] hover:bg-white/[0.15] cursor-pointer transition-colors"
                    >
                      <ArrowLeft className="w-3 h-3" />
                      <span>Return to Lesson</span>
                    </button>
                  </div>
                )}
                <StepTable
                  iterations={result.iterations}
                  method={result.method}
                  highlightedIteration={highlightedIteration}
                />
              </div>
            )}

            {activeTab === "chart" && (
              <InteractiveChart
                curves={result.curves}
                title="Solution Vector Values (x_i)"
                xLabel="Coordinate Index i"
                yLabel="Coordinate Value x_i"
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
