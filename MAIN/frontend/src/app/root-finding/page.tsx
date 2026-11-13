"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { 
  Play, 
  RotateCcw, 
  AlertCircle, 
  Layers, 
  LineChart, 
  Table,
  GraduationCap,
  ArrowLeft
} from "lucide-react";
import { MathKeyboard } from "@/components/math-keyboard";
import { MetricCard } from "@/components/metric-card";
import { StepTable } from "@/components/step-table";
import { InteractiveChart } from "@/components/interactive-chart";
import { SolutionTab } from "@/components/learning";
import { MathText } from "@/components/math-view";
import { solveRootFinding, SolverAPIResponse } from "@/lib/api";

function RootFindingContent() {
  const searchParams = useSearchParams();

  // Inputs
  const [method, setMethod] = useState<"bisection" | "false_position" | "newton_raphson">("bisection");
  const [expression, setExpression] = useState("x**3 - x - 2");
  const [a, setA] = useState("1.0");
  const [b, setB] = useState("2.0");
  const [x0, setX0] = useState("1.5");
  const [tol, setTol] = useState("1e-6");
  const [maxIter, setMaxIter] = useState("100");

  // State
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<SolverAPIResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"solution" | "steps" | "plot" | "error">("solution");
  const [highlightedIteration, setHighlightedIteration] = useState<number | null>(null);
  const [lessonStep, setLessonStep] = useState(1);

  // Sync URL query params if opened from quick-starts
  useEffect(() => {
    const exprParam = searchParams.get("expr");
    if (exprParam) setExpression(exprParam);
    const aParam = searchParams.get("a");
    if (aParam) setA(aParam);
    const bParam = searchParams.get("b");
    if (bParam) setB(bParam);
    const x0Param = searchParams.get("x0");
    if (x0Param) setX0(x0Param);
  }, [searchParams]);

  const handleRun = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const res = await solveRootFinding({
        method,
        expression: expression.trim(),
        a: method !== "newton_raphson" ? parseFloat(a) : undefined,
        b: method !== "newton_raphson" ? parseFloat(b) : undefined,
        x0: method === "newton_raphson" ? parseFloat(x0) : undefined,
        tol: parseFloat(tol) || 1e-6,
        max_iter: parseInt(maxIter) || 100,
      });
      setResult(res);
      if (!res.success) {
        setErrorMsg(`Algorithm ended with status '${res.status}': ${res.termination_reason}`);
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Calculation failed.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setExpression("x**3 - x - 2");
    setA("1.0");
    setB("2.0");
    setX0("1.5");
    setTol("1e-6");
    setMaxIter("100");
    setResult(null);
    setErrorMsg(null);
  };

  return (
    <div className="space-y-6 py-4">
      {/* Page Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
          Root Finding Laboratory
        </h1>
        <div className="text-sm text-[#7E8A98] mt-1">
          <MathText text="Compute real roots of nonlinear functions $f(x) = 0$ with step-by-step mathematical convergence." />
        </div>
      </div>

      {/* Main Solver Card */}
      <div className="glass-panel p-5 sm:p-7 rounded-2xl border border-white/[0.14] shadow-2xl space-y-6 relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        {/* Method Picker Pills */}
        <div className="flex flex-wrap gap-2.5 pb-4 border-b border-white/[0.08]">
          {[
            { id: "bisection", label: "Bisection Method", desc: "Interval Halving" },
            { id: "false_position", label: "False Position", desc: "Regula Falsi" },
            { id: "newton_raphson", label: "Newton-Raphson", desc: "Tangent Iteration" },
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
                <span className={`ml-1.5 opacity-80 text-[10px] ${isSel ? "text-[#38D9E8]" : "text-[#7E8A98]"}`}>
                  • {m.desc}
                </span>
              </button>
            );
          })}
        </div>

        {/* Form */}
        <form onSubmit={handleRun} className="space-y-4">
          {/* Equation Input & Math Pad */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Mathematical Function: f(x) = 0
            </label>
            <div className="flex items-center space-x-2">
              <span className="font-mono font-semibold text-[#38D9E8] text-sm">f(x) =</span>
              <input
                type="text"
                value={expression}
                onChange={(e) => setExpression(e.target.value)}
                placeholder="e.g. x**3 - x - 2"
                required
                className="flex-1 glass-input px-4 py-3 rounded-xl font-mono text-sm text-[#F5F7FA]"
              />
            </div>
            <MathKeyboard onInsert={(sym) => setExpression((p) => p + sym)} />
          </div>

          {/* Parameters Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
            {method !== "newton_raphson" ? (
              <>
                <div>
                  <label className="text-xs font-medium text-[#7E8A98]">Lower Bound a:</label>
                  <input
                    type="number"
                    step="any"
                    value={a}
                    onChange={(e) => setA(e.target.value)}
                    required
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs font-medium text-[#7E8A98]">Upper Bound b:</label>
                  <input
                    type="number"
                    step="any"
                    value={b}
                    onChange={(e) => setB(e.target.value)}
                    required
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
              </>
            ) : (
              <div className="col-span-2">
                <label className="text-xs font-medium text-[#7E8A98]">Initial Guess x₀:</label>
                <input
                  type="number"
                  step="any"
                  value={x0}
                  onChange={(e) => setX0(e.target.value)}
                  required
                  className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                />
              </div>
            )}

            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Tolerance:</label>
              <input
                type="text"
                value={tol}
                onChange={(e) => setTol(e.target.value)}
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>

            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Max Iterations:</label>
              <input
                type="number"
                value={maxIter}
                onChange={(e) => setMaxIter(e.target.value)}
                min="1"
                max="1000"
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3 pt-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-glass-primary font-semibold text-xs sm:text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 cursor-pointer disabled:opacity-40"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{loading ? "Computing…" : "Run Calculation"}</span>
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="btn-glass-secondary font-semibold text-xs sm:text-sm px-4 py-2.5 rounded-xl flex items-center space-x-1.5 cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>
        </form>

        {/* Error notification */}
        {errorMsg && (
          <div className="p-4 rounded-xl bg-[#FF793F]/15 border border-[#FF793F]/30 text-[#FFAD66] text-xs flex items-start space-x-2.5">
            <AlertCircle className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">Solver Notice: </span>
              <span>{errorMsg}</span>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Metrics Row */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3.5">
            <MetricCard
              label="Computed Root"
              value={result.root?.toFixed(6)}
              badge={result.status}
              color={result.success ? "rose" : "slate"}
            />
            <MetricCard
              label="f(Root)"
              value={result.f_root?.toExponential(4)}
              subtext="Residual f(x*)"
            />
            <MetricCard
              label="Iterations"
              value={result.metrics.iterations}
              subtext="Total Steps"
            />
            <MetricCard
              label="Final Error"
              value={result.metrics.final_approximate_error?.toExponential(4)}
              subtext="|x_new - x_old|"
            />
            <MetricCard
              label="Execution Time"
              value={`${(result.metrics.execution_time_seconds * 1000).toFixed(2)} ms`}
              subtext="Engine Duration"
            />
          </div>

          {/* Results Display Tabs */}
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
                onClick={() => setActiveTab("steps")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "steps"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <Table className="w-3.5 h-3.5" />
                <span>2. Iteration Steps ({result.iterations.length})</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("plot")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "plot"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <LineChart className="w-3.5 h-3.5" />
                <span>3. Function & Root Plot</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("error")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "error"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>4. Convergence Error Plot</span>
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
                  setActiveTab("steps");
                }}
              />
            )}

            {activeTab === "steps" && (
              <div className="space-y-3">
                {highlightedIteration !== null && (
                  <div className="flex items-center justify-between p-3 rounded-xl bg-[#38D9E8]/10 border border-[#38D9E8]/30 text-xs text-[#F5F7FA]">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-[#38D9E8]">Focus:</span>
                      <span>Highlighting Iteration {highlightedIteration} from lesson.</span>
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

            {activeTab === "plot" && (
              <InteractiveChart
                curves={result.curves.filter((c) => !c.label.includes("Approximate Error"))}
                markers={result.markers}
                title={`Interactive Function Curve: ${expression}`}
                xLabel="x"
                yLabel="f(x)"
              />
            )}

            {activeTab === "error" && (
              <InteractiveChart
                curves={result.curves.filter((c) => c.label.includes("Approximate Error"))}
                title="Error Convergence vs. Iteration Step"
                xLabel="Iteration Number (n)"
                yLabel="Approximate Error"
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function RootFindingPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-[#7E8A98] font-mono text-sm">Loading solver workspace…</div>}>
      <RootFindingContent />
    </Suspense>
  );
}
