"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { 
  ArrowRight, 
  TrendingUp, 
  Grid, 
  Activity, 
  Split, 
  CheckCircle2, 
  Sparkles 
} from "lucide-react";
import { MathKeyboard } from "@/components/math-keyboard";
import { MathText } from "@/components/math-view";

export default function HomePage() {
  const router = useRouter();
  const [quickExpr, setQuickExpr] = useState("x**3 - x - 2");

  const handleQuickSolve = (e: React.FormEvent) => {
    e.preventDefault();
    router.push(`/root-finding?expr=${encodeURIComponent(quickExpr)}`);
  };

  return (
    <div className="space-y-16 sm:space-y-20 py-6">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-6 pt-6 sm:pt-12 relative">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-[#38D9E8]/10 text-[#38D9E8] border border-[#38D9E8]/25 shadow-[0_0_15px_rgba(56,217,232,0.15)] backdrop-blur-md">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Interactive Mathematical Learning Engine & Numerical Simulator</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-[#F5F7FA] tracking-tight leading-[1.15]">
          Understand the Mathematics. <br />
          <span className="bg-gradient-to-r from-[#38D9E8] via-[#16B8B0] to-[#FF793F] bg-clip-text text-transparent">
            Visualize the Process.
          </span>{" "}
          Verify the Results.
        </h1>

        <p className="text-base sm:text-lg text-[#B5C0CC] max-w-2xl mx-auto leading-relaxed">
          NUMERIX is an interactive scientific computing platform.
          Inspect every iteration, explore step-by-step mathematical worked solutions, and benchmark classical algorithms in real time.
        </p>

        {/* Quick Problem Entry */}
        <div className="max-w-2xl mx-auto glass-panel p-4 sm:p-6 rounded-2xl border border-white/[0.14] shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />
          
          <form onSubmit={handleQuickSolve} className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <input
                type="text"
                value={quickExpr}
                onChange={(e) => setQuickExpr(e.target.value)}
                placeholder="Enter an equation e.g. x**3 - x - 2 = 0"
                className="w-full glass-input px-4 py-3 rounded-xl font-mono text-sm text-[#F5F7FA] placeholder-[#7E8A98]"
              />
            </div>
            <button
              type="submit"
              className="btn-glass-primary font-semibold text-sm px-6 py-3 rounded-xl flex items-center justify-center space-x-2 cursor-pointer active:scale-98"
            >
              <span>Solve Step-by-Step</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Math Pad */}
          <div className="mt-4">
            <MathKeyboard onInsert={(sym) => setQuickExpr((prev) => prev + sym)} />
          </div>
        </div>
      </section>

      {/* Module Categories Grid */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-[#F5F7FA] tracking-tight">
            Numerical Laboratory Topics
          </h2>
          <p className="text-sm text-[#7E8A98]">
            Select a module to launch its dedicated interactive solver workspace.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: Root Finding */}
          <div className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#38D9E8]/50 transition-all flex flex-col justify-between group relative overflow-hidden">
            <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />
            
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-[#38D9E8]/10 border border-[#38D9E8]/20 text-[#38D9E8] flex items-center justify-center shadow-[0_0_12px_rgba(56,217,232,0.2)]">
                <TrendingUp className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[#F5F7FA] group-hover:text-[#38D9E8] transition-colors">
                Root Finding
              </h3>
              <div className="text-sm text-[#B5C0CC] leading-relaxed">
                <MathText text="Compute approximate roots of nonlinear functions $f(x) = 0$ with bracket tracking, dynamic convergence bounds, and error charts." />
              </div>
              <ul className="text-xs text-[#7E8A98] space-y-2 font-medium">
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Bisection Method (Interval Halving)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>False Position (Regula Falsi)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Newton-Raphson (Symbolic Tangents)</span>
                </li>
              </ul>
            </div>
            <Link
              href="/root-finding"
              className="mt-6 inline-flex items-center text-sm font-semibold text-[#38D9E8] hover:text-[#16B8B0] transition-colors"
            >
              <span>Open Root Solvers</span>
              <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Card 2: Linear Systems */}
          <div className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#4B9DFF]/50 transition-all flex flex-col justify-between group relative overflow-hidden">
            <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />

            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-[#4B9DFF]/10 border border-[#4B9DFF]/20 text-[#4B9DFF] flex items-center justify-center shadow-[0_0_12px_rgba(75,157,255,0.2)]">
                <Grid className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[#F5F7FA] group-hover:text-[#4B9DFF] transition-colors">
                Linear Systems
              </h3>
              <div className="text-sm text-[#B5C0CC] leading-relaxed">
                <MathText text="Solve algebraic systems $A x = b$ using dynamic matrix grid inputs, partial pivoting row swaps, and residual vector verification." />
              </div>
              <ul className="text-xs text-[#7E8A98] space-y-2 font-medium">
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Gaussian Elimination with Partial Pivoting</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Gauss-Jordan Full Reduction (RREF)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Exact Residual Norm <MathText text="$\|Ax - b\|$" /></span>
                </li>
              </ul>
            </div>
            <Link
              href="/linear-systems"
              className="mt-6 inline-flex items-center text-sm font-semibold text-[#4B9DFF] hover:text-[#38D9E8] transition-colors"
            >
              <span>Open Matrix Solvers</span>
              <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Card 3: Differential Equations */}
          <div className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#16B8B0]/50 transition-all flex flex-col justify-between group relative overflow-hidden">
            <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />

            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-[#16B8B0]/10 border border-[#16B8B0]/20 text-[#16B8B0] flex items-center justify-center shadow-[0_0_12px_rgba(22,184,176,0.2)]">
                <Activity className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[#F5F7FA] group-hover:text-[#16B8B0] transition-colors">
                Differential Equations
              </h3>
              <div className="text-sm text-[#B5C0CC] leading-relaxed">
                <MathText text="Step through initial-value problems $dy/dx = f(x, y)$ with trajectory plots, intermediate slope stages, and analytical comparison." />
              </div>
              <ul className="text-xs text-[#7E8A98] space-y-2 font-medium">
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Euler Method (Order 1)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Modified Euler (Heun Order 2)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16B8B0]" />
                  <span>Runge-Kutta 4th Order (RK4 Order 4)</span>
                </li>
              </ul>
            </div>
            <Link
              href="/differential-equations"
              className="mt-6 inline-flex items-center text-sm font-semibold text-[#16B8B0] hover:text-[#38D9E8] transition-colors"
            >
              <span>Open ODE Solvers</span>
              <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>

      {/* Comparison & Benchmarking Highlight */}
      <section className="glass-panel p-8 sm:p-10 rounded-3xl border border-white/[0.14] flex flex-col lg:flex-row items-center justify-between gap-8 relative overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 w-80 h-80 bg-[#FF793F]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        <div className="space-y-4 max-w-2xl relative z-10">
          <div className="inline-flex items-center space-x-2 text-xs font-semibold uppercase tracking-wider text-[#FF793F]">
            <Split className="w-4 h-4" />
            <span>Interactive Benchmarking</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
            Compare Algorithms Side-by-Side on Identical Problems
          </h2>
          <p className="text-sm sm:text-base text-[#B5C0CC] leading-relaxed">
            Witness the difference in order of convergence between Bisection, False Position, and Newton-Raphson. Overlay Euler and RK4 trajectory curves directly against analytical exact solutions.
          </p>
          <div className="pt-2">
            <Link
              href="/comparison"
              className="btn-glass-primary inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl font-semibold text-sm"
            >
              <span>Launch Comparison Lab</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        <div className="w-full lg:w-80 glass-card p-5 rounded-2xl border border-white/[0.12] shadow-xl space-y-3 font-mono text-xs relative z-10">
          <div className="text-[#7E8A98] font-sans text-xs font-semibold uppercase tracking-wider">Benchmarking Overview</div>
          <div className="flex justify-between items-center py-2 border-b border-white/[0.08]">
            <span className="text-[#B5C0CC]">Newton-Raphson:</span>
            <span className="font-bold text-[#38D9E8]">5 steps (0.0012s)</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-white/[0.08]">
            <span className="text-[#B5C0CC]">False Position:</span>
            <span className="font-bold text-[#FFAD66]">14 steps (0.0034s)</span>
          </div>
          <div className="flex justify-between items-center py-2">
            <span className="text-[#B5C0CC]">Bisection Method:</span>
            <span className="font-bold text-[#7E8A98]">21 steps (0.0048s)</span>
          </div>
        </div>
      </section>
    </div>
  );
}
