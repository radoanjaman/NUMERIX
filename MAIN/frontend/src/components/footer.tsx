import React from "react";
import Link from "next/link";
import { NumerixLogo } from "@/components/NumerixLogo";

export function Footer() {
  return (
    <footer className="w-full border-t border-white/[0.12] glass-navbar mt-auto py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-[#7E8A98] gap-4">
        <div className="flex items-center space-x-3">
          <NumerixLogo layout="horizontal" height={28} />
          <span className="hidden md:inline text-white/30">|</span>
          <span className="hidden md:inline text-[#B5C0CC]">Understand the Mathematics. Visualize the Process. Verify the Results.</span>
        </div>
        <div className="flex items-center space-x-6 text-xs">
          <Link href="/about" className="hover:text-[#38D9E8] transition-colors">About</Link>
          <Link href="/learning" className="hover:text-[#38D9E8] transition-colors">Learning Center</Link>
          <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer" className="hover:text-[#38D9E8] transition-colors flex items-center space-x-1">
            <span>FastAPI Docs</span>
          </a>
          <span className="text-[#38D9E8] font-mono text-[11px] bg-white/[0.05] px-2.5 py-1 rounded-full border border-white/[0.10]">
            Numerical Engine v2.0
          </span>
        </div>
      </div>
    </footer>
  );
}
