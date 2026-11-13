"use client";

import React from "react";
import Image from "next/image";

interface NumerixLogoProps {
  layout?: "horizontal" | "vertical" | "symbol";
  height?: number;
  className?: string;
  useSvg?: boolean;
}

export function NumerixLogo({
  layout = "horizontal",
  height = 42,
  className = "",
  useSvg = false,
}: NumerixLogoProps) {
  if (layout === "symbol") {
    return (
      <div className={`relative inline-flex items-center justify-center ${className}`}>
        <Image
          src="/images/numerix-symbol.png"
          alt="NUMERIX Emblem"
          width={Math.round(height * (208 / 215))}
          height={height}
          priority
          className="object-contain drop-shadow-[0_2px_10px_rgba(245,158,11,0.25)]"
          style={{ height: `${height}px`, width: "auto" }}
        />
      </div>
    );
  }

  if (layout === "vertical") {
    const width = Math.round(height * (256 / 275));
    return (
      <div className={`relative inline-flex items-center justify-center ${className}`}>
        <Image
          src="/images/numerix-logo-dark.png"
          alt="NUMERIX Official Logo"
          width={width}
          height={height}
          priority
          className="object-contain drop-shadow-[0_6px_20px_rgba(0,0,0,0.45)]"
          style={{ height: `${height}px`, width: "auto" }}
        />
      </div>
    );
  }

  // Horizontal Lockup (Default for Navbar: Emblem on left, Wordmark on right)
  // Ratio: 211 / 46 ≈ 4.58
  const width = Math.round(height * 4.58);

  return (
    <div className={`relative inline-flex items-center ${className}`}>
      <Image
        src="/images/numerix-logo-horizontal-dark.png"
        alt="NUMERIX Official Logo"
        width={width}
        height={height}
        priority
        className="object-contain drop-shadow-[0_2px_12px_rgba(0,0,0,0.35)] transition-all duration-200 group-hover:drop-shadow-[0_2px_16px_rgba(56,217,232,0.3)]"
        style={{ height: `${height}px`, width: "auto" }}
      />
    </div>
  );
}
