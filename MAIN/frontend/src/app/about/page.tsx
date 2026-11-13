import React from "react";
import Link from "next/link";
import { 
  Layers, 
  Cpu, 
  ShieldCheck, 
  Globe, 
  Sparkles 
} from "lucide-react";
import { NumerixLogo } from "@/components/NumerixLogo";

export default function AboutPage() {
  return (
    <div className="space-y-8 max-w-4xl mx-auto py-6">
      {/* Title with Official Logo */}
      <div className="text-center space-y-4">
        <div className="flex justify-center">
          <div className="p-4 rounded-2xl glass-card inline-flex items-center justify-center">
            <NumerixLogo layout="vertical" height={96} />
          </div>
        </div>
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-[#38D9E8]/10 text-[#38D9E8] border border-[#38D9E8]/25 shadow-[0_0_15px_rgba(56,217,232,0.15)] backdrop-blur-md">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Official NUMERIX Platform</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#F5F7FA] tracking-tight">
          Numerical Simulation &amp; Learning Architecture
        </h1>
        <p className="text-base font-semibold bg-gradient-to-r from-[#38D9E8] via-[#16B8B0] to-[#FF793F] bg-clip-text text-transparent">
          Understand the Mathematics. Visualize the Process. Verify the Results.
        </p>
      </div>

      {/* Main Glass Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-white/[0.14] shadow-2xl space-y-6 text-sm text-[#B5C0CC] leading-relaxed relative overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        <div>
          <h2 className="text-lg font-bold text-[#F5F7FA] mb-2">Project Vision</h2>
          <p>
            NUMERIX is an interactive numerical methods workbench designed for university students, educators, and engineers.
            Instead of providing a black-box calculator, NUMERIX exposes every intermediate step of classical numerical algorithms,
            allowing students to inspect bracket intervals, tangent approximations, pivot row operations, and slope evaluations in real time.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="glass-card p-4 sm:p-5 rounded-xl border border-white/[0.10]">
            <h3 className="font-bold text-[#F5F7FA] flex items-center space-x-2 mb-1.5">
              <Globe className="w-4 h-4 text-[#38D9E8]" />
              <span>Public & Anonymous Access</span>
            </h3>
            <p className="text-xs text-[#7E8A98] leading-relaxed">
              No account creation, email sign-up, or login required. Open directly in any modern desktop, tablet, or mobile browser.
            </p>
          </div>

          <div className="glass-card p-4 sm:p-5 rounded-xl border border-white/[0.10]">
            <h3 className="font-bold text-[#F5F7FA] flex items-center space-x-2 mb-1.5">
              <Cpu className="w-4 h-4 text-[#4B9DFF]" />
              <span>Native Python Numerical Core</span>
            </h3>
            <p className="text-xs text-[#7E8A98] leading-relaxed">
              Calculations are executed on an optimized FastAPI Python backend using SymPy symbolic parsing and NumPy linear algebra.
            </p>
          </div>

          <div className="glass-card p-4 sm:p-5 rounded-xl border border-white/[0.10]">
            <h3 className="font-bold text-[#F5F7FA] flex items-center space-x-2 mb-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Rigorous Test Suite</span>
            </h3>
            <p className="text-xs text-[#7E8A98] leading-relaxed">
              Verified by 157 automated tests covering convergence tolerances, singular matrices, zero derivatives, educational models, and adversarial parser injection attacks.
            </p>
          </div>

          <div className="glass-card p-4 sm:p-5 rounded-xl border border-white/[0.10]">
            <h3 className="font-bold text-[#F5F7FA] flex items-center space-x-2 mb-1.5">
              <Layers className="w-4 h-4 text-[#FF793F]" />
              <span>Authentic Glassmorphism System</span>
            </h3>
            <p className="text-xs text-[#7E8A98] leading-relaxed">
              Featuring dark translucent frosted glass surfaces, deep ambient teal and orange lighting, subtle 1px white reflective borders, and high-contrast mathematical typography.
            </p>
          </div>
        </div>

        {/* Algorithm Catalog */}
        <div className="border-t border-white/[0.08] pt-6 space-y-3">
          <h2 className="text-lg font-bold text-[#F5F7FA]">Supported Algorithms</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-xs font-medium">
            <div className="p-4 bg-[#080B10]/80 rounded-xl border border-white/[0.08] space-y-1.5">
              <span className="font-bold text-[#38D9E8] block uppercase tracking-wider text-[11px]">Root Finding</span>
              <div className="text-[#B5C0CC]">• Bisection Method</div>
              <div className="text-[#B5C0CC]">• False Position (Regula Falsi)</div>
              <div className="text-[#B5C0CC]">• Newton-Raphson Method</div>
            </div>
            <div className="p-4 bg-[#080B10]/80 rounded-xl border border-white/[0.08] space-y-1.5">
              <span className="font-bold text-[#4B9DFF] block uppercase tracking-wider text-[11px]">Linear Systems</span>
              <div className="text-[#B5C0CC]">• Gaussian Elimination (Pivoting)</div>
              <div className="text-[#B5C0CC]">• Gauss-Jordan (RREF)</div>
              <div className="text-[#B5C0CC]">• Residual Norm Verification</div>
            </div>
            <div className="p-4 bg-[#080B10]/80 rounded-xl border border-white/[0.08] space-y-1.5">
              <span className="font-bold text-[#16B8B0] block uppercase tracking-wider text-[11px]">Differential Equations</span>
              <div className="text-[#B5C0CC]">• Euler Method (Order 1)</div>
              <div className="text-[#B5C0CC]">• Modified Euler (Heun Order 2)</div>
              <div className="text-[#B5C0CC]">• Runge-Kutta 4 (RK4 Order 4)</div>
            </div>
          </div>
        </div>

        <div className="border-t border-white/[0.08] pt-4 flex items-center justify-between text-xs text-[#7E8A98]">
          <span>NUMERIX Mathematical Learning Platform</span>
          <Link href="/dashboard" className="text-[#38D9E8] font-semibold hover:text-white transition-colors">
            Launch Dashboard →
          </Link>
        </div>
      </div>
    </div>
  );
}
