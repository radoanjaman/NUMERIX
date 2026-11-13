"use client";

import React, { useState } from "react";
import { 
  Play, 
  RotateCcw, 
  AlertCircle, 
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
import { solveODE, SolverAPIResponse } from "@/lib/api";

export default function DifferentialEquationsPage() {
  const [method, setMethod] = useState<"euler" | "modified_euler" | "rk4">("rk4");
  const [expression, setExpression] = useState("x + y");
  const [x0, setX0] = useState("0.0");
  const [y0, setY0] = useState("1.0");
  const [h, setH] = useState("0.1");
  const [xEnd, setXEnd] = useState("0.5");
  const [exactExpr, setExactExpr] = useState("2*exp(x) - x - 1");

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<SolverAPIResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"solution" | "plot" | "table">("solution");
  const [highlightedIteration, setHighlightedIteration] = useState<number | null>(null);
  const [lessonStep, setLessonStep] = useState(1);

  const handleRun = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const res = await solveODE({
        method,
        expression: expression.trim(),
        x0: parseFloat(x0),
        y0: parseFloat(y0),
        h: parseFloat(h),
        x_end: parseFloat(xEnd),
        exact_expression: exactExpr.trim() || null,
      });
      setResult(res);
      if (!res.success) {
        setErrorMsg(`ODE solver status '${res.status}': ${res.termination_reason}`);
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to solve ODE.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setExpression("x + y");
    setX0("0.0");
    setY0("1.0");
    setH("0.1");
    setXEnd("0.5");
    setExactExpr("2*exp(x) - x - 1");
    setResult(null);
    setErrorMsg(null);
  };

  const finalY = result?.ode_table && result.ode_table.length > 0 
    ? result.ode_table[result.ode_table.length - 1]?.y 
    : null;

  return (
    <div className="space-y-6 py-4">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
          Differential Equations Laboratory
        </h1>
        <div className="text-sm text-[#7E8A98] mt-1">
          <MathText text="Integrate initial-value problems $dy/dx = f(x, y)$ with trajectory overlays and step-by-step stage evaluations." />
        </div>
      </div>

      {/* Main Solver Card */}
      <div className="glass-panel p-5 sm:p-7 rounded-2xl border border-white/[0.14] shadow-2xl space-y-6 relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        {/* Method Picker */}
        <div className="flex flex-wrap gap-2.5 pb-4 border-b border-white/[0.08]">
          {[
            { id: "euler", label: "Euler Method", desc: "Order 1 (O(h))" },
            { id: "modified_euler", label: "Modified Euler (Heun)", desc: "Order 2 (O(h²))" },
            { id: "rk4", label: "Runge-Kutta 4 (RK4)", desc: "Order 4 (O(h⁴))" },
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

        {/* Input Form */}
        <form onSubmit={handleRun} className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Differential Equation: dy/dx = f(x, y)
            </label>
            <div className="flex items-center space-x-2">
              <span className="font-mono font-semibold text-[#38D9E8] text-sm">dy/dx =</span>
              <input
                type="text"
                value={expression}
                onChange={(e) => setExpression(e.target.value)}
                placeholder="e.g. x + y"
                required
                className="flex-1 glass-input px-4 py-3 rounded-xl font-mono text-sm text-[#F5F7FA]"
              />
            </div>
            <MathKeyboard onInsert={(sym) => setExpression((p) => p + sym)} showY={true} />
          </div>

          {/* Initial Value Problem parameters */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Initial x₀:</label>
              <input
                type="number"
                step="any"
                value={x0}
                onChange={(e) => setX0(e.target.value)}
                required
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Initial y₀ = y(x₀):</label>
              <input
                type="number"
                step="any"
                value={y0}
                onChange={(e) => setY0(e.target.value)}
                required
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Step Size h:</label>
              <input
                type="number"
                step="any"
                value={h}
                onChange={(e) => setH(e.target.value)}
                required
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-[#7E8A98]">Final x (x_end):</label>
              <input
                type="number"
                step="any"
                value={xEnd}
                onChange={(e) => setXEnd(e.target.value)}
                required
                className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
              />
            </div>
          </div>

          {/* Optional exact solution */}
          <div className="pt-1">
            <label className="text-xs font-medium text-[#7E8A98]">
              Optional Exact Solution y(x) for Error Overlay:
            </label>
            <input
              type="text"
              value={exactExpr}
              onChange={(e) => setExactExpr(e.target.value)}
              placeholder="e.g. 2*exp(x) - x - 1"
              className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3 pt-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-glass-primary font-semibold text-xs sm:text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 cursor-pointer disabled:opacity-40"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{loading ? "Integrating ODE…" : "Run Simulation"}</span>
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

        {errorMsg && (
          <div className="p-4 rounded-xl bg-[#FF793F]/15 border border-[#FF793F]/30 text-[#FFAD66] text-xs flex items-start space-x-2.5">
            <AlertCircle className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
            <div>
              <span className="font-bold">ODE Notice: </span>
              <span>{errorMsg}</span>
            </div>
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Metrics Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
            <MetricCard
              label="Final y(x_end)"
              value={finalY !== null ? finalY.toFixed(6) : "—"}
              badge={result.method}
              color="rose"
            />
            <MetricCard
              label="Integration Steps"
              value={result.metrics.iterations}
              subtext="Total step count"
            />
            <MetricCard
              label="Exact Solution Error"
              value={result.metrics.final_exact_error != null ? result.metrics.final_exact_error.toExponential(4) : "—"}
              subtext="|y_num - y_exact|"
            />
            <MetricCard
              label="Execution Time"
              value={`${(result.metrics.execution_time_seconds * 1000).toFixed(2)} ms`}
              subtext="Engine speed"
            />
          </div>

          {/* Tabbed Results */}
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
                onClick={() => setActiveTab("plot")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "plot"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <LineChart className="w-3.5 h-3.5" />
                <span>2. Numerical Trajectory Plot</span>
              </button>
              <button
                type="button"
                onClick={() => setActiveTab("table")}
                className={`flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer shrink-0 ${
                  activeTab === "table"
                    ? "bg-[#38D9E8]/20 text-[#38D9E8] border border-[#38D9E8]/40 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#7E8A98] hover:text-[#F5F7FA] hover:bg-white/[0.04]"
                }`}
              >
                <Table className="w-3.5 h-3.5" />
                <span>3. Stage Evaluation Table ({result.iterations.length})</span>
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
                  setActiveTab("table");
                }}
              />
            )}

            {activeTab === "plot" && (
              <InteractiveChart
                curves={result.curves}
                title={`Trajectory: dy/dx = ${expression}`}
                xLabel="x (Independent Variable)"
                yLabel="y(x) (State Variable)"
              />
            )}

            {activeTab === "table" && (
              <div className="space-y-3">
                {highlightedIteration !== null && (
                  <div className="flex items-center justify-between p-3 rounded-xl bg-[#38D9E8]/10 border border-[#38D9E8]/30 text-xs text-[#F5F7FA]">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-[#38D9E8]">Focus:</span>
                      <span>Highlighting Step {highlightedIteration} from lesson.</span>
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
          </div>
        </div>
      )}
    </div>
  );
}
