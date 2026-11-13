"use client";

import React from "react";
import Link from "next/link";
import { 
  TrendingUp, 
  Grid, 
  Activity, 
  Split, 
  BookOpen, 
  ArrowRight, 
  Play, 
  Sparkles 
} from "lucide-react";
import { MathText } from "@/components/math-view";

const PRESETS = [
  {
    title: "Standard Cubic Root",
    category: "Root Finding",
    detail: "f(x) = x³ - x - 2 on [1, 2]",
    href: "/root-finding?expr=x**3+-+x+-+2&a=1&b=2&x0=1.5",
  },
  {
    title: "Kepler Transcendental Equation",
    category: "Root Finding",
    detail: "f(x) = x - 0.2*sin(x) - 0.5",
    href: "/root-finding?expr=x+-+0.2*sin(x)+-+0.5&a=0&b=2&x0=0.5",
  },
  {
    title: "3×3 Well-Conditioned Linear System",
    category: "Linear Systems",
    detail: "2x₁ + x₂ + x₃ = 8, x₁ + 3x₂ + x₃ = 10, x₁ + x₂ + 4x₃ = 15",
    href: "/linear-systems",
  },
  {
    title: "Classic Initial Value Problem (IVP)",
    category: "Differential Equations",
    detail: "dy/dx = x + y with y(0) = 1, h = 0.1, x_end = 0.5",
    href: "/differential-equations",
  },
  {
    title: "Convergence Order Comparison",
    category: "Comparison",
    detail: "Compare Bisection vs False Position vs Newton-Raphson",
    href: "/comparison",
  },
];

export default function DashboardPage() {
  return (
    <div className="space-y-8 py-4">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/[0.08] pb-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#F5F7FA] tracking-tight">
            Dashboard
          </h1>
          <p className="text-sm text-[#7E8A98] mt-1">
            Overview of laboratory computation modules and quick-start numerical presets.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            href="/comparison"
            className="btn-glass-primary inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold"
          >
            <Split className="w-3.5 h-3.5" />
            <span>Comparison Lab</span>
          </Link>
          <Link
            href="/learning"
            className="btn-glass-secondary inline-flex items-center space-x-2 px-4 py-2 rounded-xl text-xs font-semibold"
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Learning Center</span>
          </Link>
        </div>
      </div>

      {/* Primary Workspaces Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Workspace 1: Root Finding */}
        <Link
          href="/root-finding"
          className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#38D9E8]/50 transition-all group flex flex-col justify-between relative overflow-hidden"
        >
          <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />
          <div>
            <div className="w-12 h-12 rounded-xl bg-[#38D9E8]/10 border border-[#38D9E8]/20 text-[#38D9E8] flex items-center justify-center mb-4 shadow-[0_0_12px_rgba(56,217,232,0.2)]">
              <TrendingUp className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-[#F5F7FA] group-hover:text-[#38D9E8] transition-colors">
              Root Finding Solvers
            </h3>
            <div className="text-xs text-[#B5C0CC] mt-2 leading-relaxed">
              <MathText text="Find scalar solutions for $f(x) = 0$. Inspect bracket contraction or tangent derivative updates step-by-step." />
            </div>
          </div>
          <div className="mt-6 flex items-center justify-between text-xs font-medium text-[#7E8A98] pt-3 border-t border-white/[0.08]">
            <span>3 Algorithms Available</span>
            <ArrowRight className="w-4 h-4 text-[#38D9E8] group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        {/* Workspace 2: Linear Systems */}
        <Link
          href="/linear-systems"
          className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#4B9DFF]/50 transition-all group flex flex-col justify-between relative overflow-hidden"
        >
          <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />
          <div>
            <div className="w-12 h-12 rounded-xl bg-[#4B9DFF]/10 border border-[#4B9DFF]/20 text-[#4B9DFF] flex items-center justify-center mb-4 shadow-[0_0_12px_rgba(75,157,255,0.2)]">
              <Grid className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-[#F5F7FA] group-hover:text-[#4B9DFF] transition-colors">
              Linear Systems Solvers
            </h3>
            <div className="text-xs text-[#B5C0CC] mt-2 leading-relaxed">
              <MathText text="Solve $A x = b$ using dynamic interactive grid inputs. View pivot row swaps and elementary elimination matrices." />
            </div>
          </div>
          <div className="mt-6 flex items-center justify-between text-xs font-medium text-[#7E8A98] pt-3 border-t border-white/[0.08]">
            <span>2 Algorithms (Pivoting)</span>
            <ArrowRight className="w-4 h-4 text-[#4B9DFF] group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>

        {/* Workspace 3: ODEs */}
        <Link
          href="/differential-equations"
          className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl hover:border-[#16B8B0]/50 transition-all group flex flex-col justify-between relative overflow-hidden"
        >
          <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />
          <div>
            <div className="w-12 h-12 rounded-xl bg-[#16B8B0]/10 border border-[#16B8B0]/20 text-[#16B8B0] flex items-center justify-center mb-4 shadow-[0_0_12px_rgba(22,184,176,0.2)]">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-[#F5F7FA] group-hover:text-[#16B8B0] transition-colors">
              Differential Equations (ODEs)
            </h3>
            <div className="text-xs text-[#B5C0CC] mt-2 leading-relaxed">
              <MathText text="Step through IVPs $dy/dx = f(x, y)$. Track slope stages $k_1, k_2, k_3, k_4$ and compare against exact solutions." />
            </div>
          </div>
          <div className="mt-6 flex items-center justify-between text-xs font-medium text-[#7E8A98] pt-3 border-t border-white/[0.08]">
            <span>Euler, Heun, RK4</span>
            <ArrowRight className="w-4 h-4 text-[#16B8B0] group-hover:translate-x-1 transition-transform" />
          </div>
        </Link>
      </div>

      {/* Preset Problem Library */}
      <div className="glass-panel p-6 sm:p-7 rounded-2xl border border-white/[0.12] shadow-xl space-y-4 relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/15 to-transparent pointer-events-none" />
        
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <h2 className="text-base font-bold text-[#F5F7FA] flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-[#38D9E8]" />
              <span>Standard Laboratory Presets</span>
            </h2>
            <p className="text-xs text-[#7E8A98]">
              Pre-configured textbook examples ready to run in one click.
            </p>
          </div>
        </div>

        <div className="divide-y divide-white/[0.06]">
          {PRESETS.map((preset) => (
            <div
              key={preset.title}
              className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-white/[0.03] px-3 rounded-xl transition-colors"
            >
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-semibold text-[#F5F7FA]">{preset.title}</span>
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-white/[0.06] text-[#38D9E8] border border-white/[0.10]">
                    {preset.category}
                  </span>
                </div>
                <div className="font-mono text-xs text-[#7E8A98] mt-1">{preset.detail}</div>
              </div>
              <Link
                href={preset.href}
                className="inline-flex items-center space-x-1.5 text-xs font-semibold text-[#38D9E8] hover:text-white bg-[#38D9E8]/10 hover:bg-[#38D9E8]/20 px-3 py-1.5 rounded-xl border border-[#38D9E8]/30 transition-all self-start sm:self-auto cursor-pointer"
              >
                <span>Load in Solver</span>
                <Play className="w-3 h-3 fill-current" />
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
