"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Calculator, 
  Menu, 
  X, 
  Activity, 
  Layers, 
  TrendingUp, 
  Grid, 
  Split, 
  BookOpen, 
  Info
} from "lucide-react";
import { checkHealth } from "@/lib/api";
import { NumerixLogo } from "@/components/NumerixLogo";

const NAV_LINKS = [
  { href: "/", label: "Home", icon: Calculator },
  { href: "/dashboard", label: "Dashboard", icon: Layers },
  { href: "/root-finding", label: "Root Finding", icon: TrendingUp },
  { href: "/linear-systems", label: "Linear Systems", icon: Grid },
  { href: "/differential-equations", label: "Differential Equations", icon: Activity },
  { href: "/comparison", label: "Comparison", icon: Split },
  { href: "/learning", label: "Learning Center", icon: BookOpen },
  { href: "/about", label: "About", icon: Info },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    checkHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  return (
    <header className="sticky top-0 z-50 w-full glass-navbar transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand: Official NUMERIX Logo (Preserves orange symbol, dark teal cross, and NUMERIX wordmark) */}
        <Link 
          href="/" 
          className="flex items-center group py-1 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#38D9E8] rounded-xl"
          aria-label="NUMERIX Home"
        >
          <NumerixLogo layout="horizontal" height={42} className="group-hover:opacity-95 transition-opacity" />
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden lg:flex items-center space-x-1 bg-white/[0.03] p-1 rounded-2xl border border-white/[0.06] backdrop-blur-md">
          {NAV_LINKS.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? "bg-white/[0.12] text-[#38D9E8] border border-cyan-400/30 shadow-[0_0_12px_rgba(56,217,232,0.2)]"
                    : "text-[#B5C0CC] hover:text-[#F5F7FA] hover:bg-white/[0.05]"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Status Indicator & Mobile Toggle */}
        <div className="flex items-center space-x-3">
          <div className="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-white/[0.05] border border-white/[0.1] text-[#B5C0CC]">
            <span
              className={`w-2 h-2 rounded-full ${
                apiOnline === true
                  ? "bg-[#38D9E8] shadow-[0_0_8px_#38D9E8] animate-pulse"
                  : apiOnline === false
                  ? "bg-[#FF793F] shadow-[0_0_8px_#FF793F]"
                  : "bg-amber-400"
              }`}
            />
            <span className="font-mono text-[11px]">
              {apiOnline === true ? "API Online" : apiOnline === false ? "API Offline" : "Checking…"}
            </span>
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-xl text-[#B5C0CC] hover:text-white hover:bg-white/[0.08] border border-white/[0.08] focus:outline-none cursor-pointer"
            aria-label="Toggle navigation"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-white/[0.12] glass-navbar px-4 pt-3 pb-5 space-y-1">
          {NAV_LINKS.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center space-x-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-white/[0.12] text-[#38D9E8] border border-cyan-400/30"
                    : "text-[#B5C0CC] hover:bg-white/[0.06] hover:text-white"
                }`}
              >
                <Icon className="w-4 h-4 text-[#38D9E8]" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
