"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  AlertTriangle, 
  Play
} from "lucide-react";
import { MathView, MathText } from "@/components/math-view";

interface TopicGuide {
  id: string;
  category: string;
  name: string;
  formula: string;
  procedure: string[];
  convergence: string;
  failureCases: string[];
  example: string;
}

const TOPICS: TopicGuide[] = [
  {
    id: "bisection",
    category: "Root Finding",
    name: "Bisection Method",
    formula: "c = \\frac{a + b}{2}, \\quad f(a) \\cdot f(b) < 0",
    procedure: [
      "1. Verify that f(a) and f(b) have opposite signs: f(a) · f(b) < 0.",
      "2. Calculate the midpoint: c = (a + b) / 2.",
      "3. Evaluate f(c). If |f(c)| < tol or (b - a)/2 < tol, stop; root ≈ c.",
      "4. If f(a) · f(c) < 0, set b = c; else set a = c.",
      "5. Repeat until the desired tolerance is met or max iterations reached.",
    ],
    convergence: "Linear convergence. Halves interval width every step (O(1/2^n)), gaining approximately 1 bit of precision per iteration.",
    failureCases: [
      "No sign change in [a, b] (e.g. roots with even multiplicity like f(x) = x²).",
      "Discontinuous functions where sign changes across an asymptote (e.g. f(x) = 1/x).",
    ],
    example: "f(x) = x³ - x - 2 = 0 on [1, 2] → root ≈ 1.52138",
  },
  {
    id: "false_position",
    category: "Root Finding",
    name: "False Position (Regula Falsi)",
    formula: "c = \\frac{a \\cdot f(b) - b \\cdot f(a)}{f(b) - f(a)}",
    procedure: [
      "1. Verify opposite signs at bracket endpoints: f(a) · f(b) < 0.",
      "2. Construct the secant line between (a, f(a)) and (b, f(b)); find x-intercept c.",
      "3. Evaluate f(c). If |root_new - root_old| < tol, terminate.",
      "4. Replace the bracket endpoint possessing the same sign as f(c).",
      "5. Repeat.",
    ],
    convergence: "Superlinear in favorable geometry, but can degenerate to linear if one bracket endpoint remains stagnant on convex functions.",
    failureCases: [
      "One-sided stagnation on functions with pronounced curvature.",
      "Identical sign endpoints (f(a) · f(b) > 0).",
    ],
    example: "f(x) = x³ - x - 2 on [1, 2] → root ≈ 1.52138",
  },
  {
    id: "newton_raphson",
    category: "Root Finding",
    name: "Newton-Raphson Method",
    formula: "x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}",
    procedure: [
      "1. Choose an initial approximation x₀ sufficiently close to the true root.",
      "2. Evaluate function value f(x_n) and symbolic derivative f'(x_n).",
      "3. Verify |f'(x_n)| > 10⁻¹⁴ to prevent division by near-zero slope.",
      "4. Compute next estimate: x_{n+1} = x_n - f(x_n) / f'(x_n).",
      "5. Stop when |x_{n+1} - x_n| < tol.",
    ],
    convergence: "Quadratic convergence (error squared each step: e_{n+1} ≈ C e_n²) for simple roots.",
    failureCases: [
      "Zero derivative: horizontal tangent causes division by zero.",
      "Inflection point cycles (oscillations between two non-root values).",
      "Divergence from poor initial guesses x₀.",
    ],
    example: "f(x) = x³ - x - 2, x₀ = 1.5 → root ≈ 1.52138",
  },
  {
    id: "gauss_elimination",
    category: "Linear Systems",
    name: "Gaussian Elimination with Partial Pivoting",
    formula: "R_j \\leftarrow R_j - \\left(\\frac{A_{j,i}}{A_{i,i}}\\right) R_i, \\quad |A_{i,i}| = \\max_{k \\ge i} |A_{k,i}|",
    procedure: [
      "1. Augmented matrix [A | b] constructed.",
      "2. Column i pivot selection: locate row k with largest absolute entry |A_{k,i}|.",
      "3. Swap row i and row k to maintain numerical stability.",
      "4. For rows j > i: eliminate subdiagonal entries using multiplier m = A_{j,i} / A_{i,i}.",
      "5. Once upper triangular form is achieved, perform back-substitution.",
    ],
    convergence: "Direct exact method (O(2/3 n³) operations).",
    failureCases: [
      "Singular or near-singular matrices with zero pivots.",
      "Ill-conditioned systems where rounding errors dominate.",
    ],
    example: "[ [2, 1, 1], [1, 3, 1], [1, 1, 4] ] x = [8, 10, 15] → x = [1.647, 1.824, 2.882]",
  },
  {
    id: "gauss_jordan",
    category: "Linear Systems",
    name: "Gauss-Jordan Elimination",
    formula: "R_i \\leftarrow \\frac{R_i}{A_{i,i}}, \\quad R_k \\leftarrow R_k - A_{k,i} R_i \\quad (\\forall k \\ne i)",
    procedure: [
      "1. Locate largest pivot in current column and swap rows.",
      "2. Normalize the pivot row so that leading coefficient A_{i,i} = 1.",
      "3. Eliminate entries in column i across all other rows (both above and below).",
      "4. Continue across all n columns until matrix reaches Reduced Row Echelon Form (RREF).",
      "5. Solution x is read directly from the right-hand column.",
    ],
    convergence: "Direct exact method (O(n³) operations).",
    failureCases: [
      "Singular or rank-deficient matrices.",
    ],
    example: "Same 3×3 system as Gauss Elimination.",
  },
  {
    id: "euler",
    category: "Differential Equations",
    name: "Euler's Forward Method",
    formula: "y_{n+1} = y_n + h \\cdot f(x_n, y_n)",
    procedure: [
      "1. Start from initial condition: (x₀, y₀).",
      "2. Calculate slope at current point: s = f(x_n, y_n).",
      "3. Advance state: y_{n+1} = y_n + h · s, x_{n+1} = x_n + h.",
      "4. Record stage and iterate until x reaches x_end.",
    ],
    convergence: "First-order accuracy (global error O(h)). Local truncation error O(h²).",
    failureCases: [
      "Stiff differential equations requiring prohibitively small step sizes h.",
      "Rapidly diverging or oscillatory systems.",
    ],
    example: "dy/dx = x + y, y(0)=1, h=0.1 over [0, 0.5]",
  },
  {
    id: "modified_euler",
    category: "Differential Equations",
    name: "Modified Euler (Heun Predictor-Corrector)",
    formula: "y^*_{n+1} = y_n + h f(x_n, y_n), \\quad y_{n+1} = y_n + \\frac{h}{2} [f(x_n, y_n) + f(x_{n+1}, y^*_{n+1})]",
    procedure: [
      "1. Predictor step: calculate initial slope f₁ = f(x_n, y_n) and predict y*_{n+1} = y_n + h · f₁.",
      "2. Evaluate predicted slope: f₂ = f(x_n + h, y*_{n+1}).",
      "3. Corrector step: average slopes: y_{n+1} = y_n + (h/2) · (f₁ + f₂).",
      "4. Advance x_{n+1} = x_n + h.",
    ],
    convergence: "Second-order accuracy (global error O(h²)).",
    failureCases: [
      "Stiff systems with extreme slope variations.",
    ],
    example: "dy/dx = x + y, y(0)=1, h=0.1",
  },
  {
    id: "rk4",
    category: "Differential Equations",
    name: "Runge-Kutta 4th Order (RK4)",
    formula: "y_{n+1} = y_n + \\frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)",
    procedure: [
      "1. k₁ = h · f(x_n, y_n) — slope at beginning of interval.",
      "2. k₂ = h · f(x_n + h/2, y_n + k₁/2) — midpoint slope using k₁.",
      "3. k₃ = h · f(x_n + h/2, y_n + k₂/2) — midpoint slope using k₂.",
      "4. k₄ = h · f(x_n + h, y_n + k₃) — endpoint slope using k₃.",
      "5. Weighted average: y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄) / 6.",
    ],
    convergence: "Fourth-order accuracy (global error O(h⁴)). High precision with moderate step sizes.",
    failureCases: [
      "Discontinuous derivatives or singularities.",
    ],
    example: "dy/dx = x + y, y(0)=1, h=0.1 → error < 10⁻⁵",
  },
];

export default function LearningPage() {
  const [activeId, setActiveId] = useState<string>("bisection");

  const activeTopic = TOPICS.find((t) => t.id === activeId) || TOPICS[0];

  return (
    <div className="space-y-6 py-4">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
          Numerical Methods Learning Center
        </h1>
        <p className="text-sm text-[#7E8A98] mt-1">
          Mathematical reference, derivations, step-by-step procedures, and convergence analysis.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Navigation List (Left) */}
        <div className="lg:col-span-4 space-y-2.5">
          {TOPICS.map((topic) => {
            const isSel = topic.id === activeId;
            return (
              <button
                key={topic.id}
                type="button"
                onClick={() => setActiveId(topic.id)}
                className={`w-full text-left p-4 rounded-2xl border transition-all cursor-pointer backdrop-blur-md ${
                  isSel
                    ? "bg-[#38D9E8]/15 border-[#38D9E8]/60 text-[#F5F7FA] shadow-[0_0_15px_rgba(56,217,232,0.2)]"
                    : "glass-card border-white/[0.08] text-[#B5C0CC] hover:bg-white/[0.04] hover:text-[#F5F7FA]"
                }`}
              >
                <div className={`text-[10px] font-bold uppercase tracking-wider mb-0.5 ${isSel ? "text-[#38D9E8]" : "text-[#7E8A98]"}`}>
                  {topic.category}
                </div>
                <div className="font-bold text-sm text-[#F5F7FA]">{topic.name}</div>
              </button>
            );
          })}
        </div>

        {/* Content Viewer (Right) */}
        <div className="lg:col-span-8 glass-panel p-6 sm:p-8 rounded-2xl border border-white/[0.14] shadow-2xl space-y-6 relative overflow-hidden">
          <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

          <div className="border-b border-white/[0.08] pb-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-[#38D9E8] block mb-1">
                {activeTopic.category} Reference
              </span>
              <h2 className="text-2xl font-extrabold text-[#F5F7FA]">{activeTopic.name}</h2>
            </div>
            <Link
              href={
                activeTopic.category === "Root Finding"
                  ? "/root-finding"
                  : activeTopic.category === "Linear Systems"
                  ? "/linear-systems"
                  : "/differential-equations"
              }
              className="btn-glass-primary inline-flex items-center space-x-1.5 text-xs font-semibold px-4 py-2.5 rounded-xl shrink-0"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Launch Solver Lesson</span>
            </Link>
          </div>

          {/* Mathematical Formula Box */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Governing Mathematical Formula:
            </span>
            <div className="bg-[#080B10]/80 text-[#F5F7FA] p-4 rounded-xl border border-white/[0.08] shadow-inner overflow-x-auto text-center">
              <MathView math={activeTopic.formula} display className="text-[#F5F7FA] text-base sm:text-lg" />
            </div>
          </div>

          {/* Step-by-Step Procedure */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Step-by-Step Algorithm:
            </span>
            <div className="space-y-2 text-xs sm:text-sm text-[#B5C0CC]">
              {activeTopic.procedure.map((step, idx) => (
                <div key={idx} className="flex items-start space-x-2.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#38D9E8] mt-2 shrink-0 shadow-[0_0_6px_rgba(56,217,232,0.8)]" />
                  <MathText text={step} className="leading-relaxed" />
                </div>
              ))}
            </div>
          </div>

          {/* Convergence Behavior */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Convergence & Accuracy:
            </span>
            <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-xl text-xs sm:text-sm leading-relaxed">
              <MathText text={activeTopic.convergence} />
            </div>
          </div>

          {/* Common Failure Modes */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-[#B5C0CC] uppercase tracking-wider">
              Known Failure Cases:
            </span>
            <div className="p-4 bg-[#FF793F]/10 border border-[#FF793F]/30 text-[#FFAD66] rounded-xl text-xs space-y-2">
              {activeTopic.failureCases.map((fc, i) => (
                <div key={i} className="flex items-start space-x-2.5">
                  <AlertTriangle className="w-4 h-4 text-[#FF793F] shrink-0 mt-0.5" />
                  <MathText text={fc} />
                </div>
              ))}
            </div>
          </div>

          {/* Example Problem */}
          <div className="pt-3 border-t border-white/[0.08] text-xs text-[#7E8A98] font-mono">
            <span className="font-semibold text-[#B5C0CC]">Verified Textbook Example: </span>
            <MathText text={activeTopic.example} />
          </div>
        </div>
      </div>
    </div>
  );
}
