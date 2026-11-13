"use client";

import React, { useState } from "react";
import { 
  Play, 
  AlertCircle, 
  TrendingUp, 
  Activity, 
  Grid 
} from "lucide-react";
import { MathKeyboard } from "@/components/math-keyboard";
import { InteractiveChart } from "@/components/interactive-chart";
import { compareMethods, ComparisonAPIResponse } from "@/lib/api";

export default function ComparisonPage() {
  const [category, setCategory] = useState<"root_finding" | "linear_systems" | "ode">("root_finding");

  // Root finding inputs
  const [rootExpr, setRootExpr] = useState("x**3 - x - 2");
  const [rootA, setRootA] = useState("1.0");
  const [rootB, setRootB] = useState("2.0");
  const [rootX0, setRootX0] = useState("1.5");
  const [selRootMethods, setSelRootMethods] = useState<string[]>(["bisection", "false_position", "newton_raphson"]);

  // ODE inputs
  const [odeExpr, setOdeExpr] = useState("x + y");
  const [odeX0, setOdeX0] = useState("0.0");
  const [odeY0, setOdeY0] = useState("1.0");
  const [odeH, setOdeH] = useState("0.1");
  const [odeXEnd, setOdeXEnd] = useState("0.5");
  const [selOdeMethods, setSelOdeMethods] = useState<string[]>(["euler", "modified_euler", "rk4"]);

  // Linear inputs
  const [linearMethods, setLinearMethods] = useState<string[]>(["gauss_elimination", "gauss_jordan"]);

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [compResult, setCompResult] = useState<ComparisonAPIResponse | null>(null);

  const toggleMethod = (mList: string[], setList: (l: string[]) => void, id: string) => {
    if (mList.includes(id)) {
      if (mList.length > 1) setList(mList.filter((m) => m !== id));
    } else {
      setList([...mList, id]);
    }
  };

  const handleRunComparison = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setErrorMsg(null);
    setLoading(true);

    try {
      const payload: any = { category, methods: [] };

      if (category === "root_finding") {
        payload.methods = selRootMethods;
        payload.root_input = {
          method: "bisection",
          expression: rootExpr.trim(),
          a: parseFloat(rootA),
          b: parseFloat(rootB),
          x0: parseFloat(rootX0),
          tol: 1e-6,
          max_iter: 100,
        };
      } else if (category === "ode") {
        payload.methods = selOdeMethods;
        payload.ode_input = {
          method: "euler",
          expression: odeExpr.trim(),
          x0: parseFloat(odeX0),
          y0: parseFloat(odeY0),
          h: parseFloat(odeH),
          x_end: parseFloat(odeXEnd),
        };
      } else {
        payload.methods = linearMethods;
        payload.linear_input = {
          method: "gauss_elimination",
          A: [
            [2.0, 1.0, 1.0],
            [1.0, 3.0, 1.0],
            [1.0, 1.0, 4.0],
          ],
          b: [8.0, 10.0, 15.0],
        };
      }

      const res = await compareMethods(payload);
      setCompResult(res);
    } catch (err: any) {
      setErrorMsg(err.message || "Comparison failed.");
      setCompResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 py-4">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
          Method Comparison Lab
        </h1>
        <p className="text-sm text-[#7E8A98] mt-1">
          Benchmark compatible numerical algorithms on identical mathematical problems.
        </p>
      </div>

      {/* Category Tabs */}
      <div className="flex border-b border-white/[0.08] overflow-x-auto">
        {[
          { id: "root_finding", label: "Root Finding Comparison", icon: TrendingUp },
          { id: "ode", label: "Differential Equations Comparison", icon: Activity },
          { id: "linear_systems", label: "Linear Systems Comparison", icon: Grid },
        ].map((tab) => {
          const Icon = tab.icon;
          const isSel = category === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => {
                setCategory(tab.id as any);
                setCompResult(null);
                setErrorMsg(null);
              }}
              className={`flex items-center space-x-2 py-3 px-5 text-xs sm:text-sm font-semibold border-b-2 transition-all cursor-pointer shrink-0 ${
                isSel
                  ? "border-[#38D9E8] text-[#38D9E8] bg-[#38D9E8]/10"
                  : "border-transparent text-[#7E8A98] hover:text-[#F5F7FA]"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Problem Configuration Box */}
      <div className="glass-panel p-5 sm:p-7 rounded-2xl border border-white/[0.14] shadow-2xl space-y-5 relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        <form onSubmit={handleRunComparison} className="space-y-4">
          {category === "root_finding" && (
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider block mb-2">
                  Equation: f(x) = 0
                </label>
                <input
                  type="text"
                  value={rootExpr}
                  onChange={(e) => setRootExpr(e.target.value)}
                  className="w-full glass-input px-4 py-3 rounded-xl font-mono text-sm text-[#F5F7FA]"
                  required
                />
                <div className="mt-3">
                  <MathKeyboard onInsert={(sym) => setRootExpr((p) => p + sym)} />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-xs text-[#7E8A98]">Bracket a:</label>
                  <input
                    type="number"
                    step="any"
                    value={rootA}
                    onChange={(e) => setRootA(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#7E8A98]">Bracket b:</label>
                  <input
                    type="number"
                    step="any"
                    value={rootB}
                    onChange={(e) => setRootB(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#7E8A98]">Newton Guess x₀:</label>
                  <input
                    type="number"
                    step="any"
                    value={rootX0}
                    onChange={(e) => setRootX0(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-[#B5C0CC] block mb-2">Select Solvers to Compare:</label>
                <div className="flex flex-wrap gap-2.5">
                  {[
                    { id: "bisection", label: "Bisection" },
                    { id: "false_position", label: "False Position" },
                    { id: "newton_raphson", label: "Newton-Raphson" },
                  ].map((m) => {
                    const checked = selRootMethods.includes(m.id);
                    return (
                      <button
                        key={m.id}
                        type="button"
                        onClick={() => toggleMethod(selRootMethods, setSelRootMethods, m.id)}
                        className={`px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all cursor-pointer backdrop-blur-md ${
                          checked
                            ? "bg-[#38D9E8]/20 border-[#38D9E8]/50 text-[#38D9E8] shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                            : "bg-white/[0.04] border-white/[0.08] text-[#7E8A98] hover:text-[#F5F7FA]"
                        }`}
                      >
                        {checked ? "✓ " : "+ "} {m.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {category === "ode" && (
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider block mb-2">
                  Differential Equation: dy/dx = f(x, y)
                </label>
                <input
                  type="text"
                  value={odeExpr}
                  onChange={(e) => setOdeExpr(e.target.value)}
                  className="w-full glass-input px-4 py-3 rounded-xl font-mono text-sm text-[#F5F7FA]"
                  required
                />
              </div>

              <div className="grid grid-cols-4 gap-3">
                <div>
                  <label className="text-xs text-[#7E8A98]">x₀:</label>
                  <input
                    type="number"
                    step="any"
                    value={odeX0}
                    onChange={(e) => setOdeX0(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#7E8A98]">y₀:</label>
                  <input
                    type="number"
                    step="any"
                    value={odeY0}
                    onChange={(e) => setOdeY0(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#7E8A98]">Step h:</label>
                  <input
                    type="number"
                    step="any"
                    value={odeH}
                    onChange={(e) => setOdeH(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
                <div>
                  <label className="text-xs text-[#7E8A98]">End x:</label>
                  <input
                    type="number"
                    step="any"
                    value={odeXEnd}
                    onChange={(e) => setOdeXEnd(e.target.value)}
                    className="w-full glass-input px-3 py-2 rounded-xl font-mono text-xs mt-1 text-[#F5F7FA]"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-bold text-[#B5C0CC] block mb-2">Select ODE Solvers:</label>
                <div className="flex flex-wrap gap-2.5">
                  {[
                    { id: "euler", label: "Euler Method (Order 1)" },
                    { id: "modified_euler", label: "Modified Euler (Order 2)" },
                    { id: "rk4", label: "Runge-Kutta 4 (Order 4)" },
                  ].map((m) => {
                    const checked = selOdeMethods.includes(m.id);
                    return (
                      <button
                        key={m.id}
                        type="button"
                        onClick={() => toggleMethod(selOdeMethods, setSelOdeMethods, m.id)}
                        className={`px-3.5 py-2 rounded-xl text-xs font-semibold border transition-all cursor-pointer backdrop-blur-md ${
                          checked
                            ? "bg-[#38D9E8]/20 border-[#38D9E8]/50 text-[#38D9E8] shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                            : "bg-white/[0.04] border-white/[0.08] text-[#7E8A98] hover:text-[#F5F7FA]"
                        }`}
                      >
                        {checked ? "✓ " : "+ "} {m.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {category === "linear_systems" && (
            <div className="space-y-2 text-xs text-[#B5C0CC]">
              <span className="font-semibold text-[#F5F7FA]">System to Benchmark:</span>
              <div className="p-4 bg-[#080B10]/80 rounded-xl border border-white/[0.08] font-mono shadow-inner text-[#38D9E8]">
                [ [2, 1, 1], [1, 3, 1], [1, 1, 4] ] x = [8, 10, 15]
              </div>
              <p className="text-[#7E8A98] italic mt-1">
                Compares Gaussian Elimination vs. Gauss-Jordan Elimination with partial pivoting.
              </p>
            </div>
          )}

          {/* Run Button */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="btn-glass-primary font-semibold text-xs sm:text-sm px-6 py-2.5 rounded-xl flex items-center space-x-2 cursor-pointer disabled:opacity-40"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>{loading ? "Running Benchmark…" : "Run Side-by-Side Comparison"}</span>
            </button>
          </div>
        </form>

        {errorMsg && (
          <div className="p-4 rounded-xl bg-[#FF793F]/15 border border-[#FF793F]/30 text-[#FFAD66] text-xs flex items-start space-x-2">
            <AlertCircle className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
            <span>{errorMsg}</span>
          </div>
        )}
      </div>

      {/* Comparison Results */}
      {compResult && (
        <div className="space-y-6">
          {/* Comparison Table */}
          <div className="glass-panel p-5 sm:p-6 rounded-2xl border border-white/[0.12] shadow-xl space-y-4">
            <h2 className="text-sm font-bold text-[#F5F7FA] uppercase tracking-wider">
              Benchmark Summary Results
            </h2>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-[#B5C0CC] font-sans">
                <thead className="bg-white/[0.04] text-[#F5F7FA] font-semibold border-b border-white/[0.08] uppercase tracking-wider text-[11px]">
                  <tr>
                    <th className="py-3 px-4">Method</th>
                    <th className="py-3 px-4">Solution Summary</th>
                    <th className="py-3 px-4 text-center">Iterations / Steps</th>
                    <th className="py-3 px-4">Final Error / Residual</th>
                    <th className="py-3 px-4">Execution Time</th>
                    <th className="py-3 px-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/[0.06] font-mono">
                  {compResult.items.map((item) => (
                    <tr key={item.method} className="hover:bg-white/[0.03] transition-colors">
                      <td className="py-3 px-4 font-sans font-bold text-[#F5F7FA]">
                        {item.method}
                      </td>
                      <td className="py-3 px-4 font-semibold text-[#38D9E8]">
                        {item.solution_summary}
                      </td>
                      <td className="py-3 px-4 text-center font-bold text-[#F5F7FA]">
                        {item.iterations_or_steps}
                      </td>
                      <td className="py-3 px-4 text-[#FFAD66]">
                        {item.final_error_or_residual !== null && item.final_error_or_residual !== undefined
                          ? item.final_error_or_residual.toExponential(4)
                          : "—"}
                      </td>
                      <td className="py-3 px-4 text-[#7E8A98]">
                        {(item.execution_time_seconds * 1000).toFixed(2)} ms
                      </td>
                      <td className="py-3 px-4 text-center">
                        <span className="text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                          {item.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Comparison Multi-Curve Graph (for ODEs) */}
          {compResult.curves && compResult.curves.length > 0 && (
            <InteractiveChart
              curves={compResult.curves}
              title="Method Trajectory Comparison"
              xLabel="x"
              yLabel="y(x)"
            />
          )}
        </div>
      )}
    </div>
  );
}
