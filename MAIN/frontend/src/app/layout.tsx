import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";

export const metadata: Metadata = {
  title: "NUMERIX — Premium Glassmorphism Numerical Simulator & Learning Engine",
  description:
    "An academic numerical methods workbench with frosted glass translucent interfaces, interactive step-by-step mathematical learning, and real-time visualization.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="flex flex-col min-h-screen bg-[#080B10] text-[#F5F7FA] antialiased selection:bg-[#38D9E8]/30 selection:text-white relative">
        {/* Ambient Glassmorphism Background Layer (Teal, Cyan, Electric Blue, Torus/Orb Diffusions) */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0" aria-hidden="true">
          {/* Deep charcoal background gradient */}
          <div className="absolute inset-0 bg-gradient-to-b from-[#080B10] via-[#0B0F15] to-[#06080C]" />

          {/* Top-Left / Center: Primary Teal & Cyan Ambient Glow */}
          <div className="absolute -top-[12%] left-[12%] w-[720px] h-[720px] rounded-full bg-[#16B8B0]/18 blur-[150px] transform -translate-x-1/2" />
          <div className="absolute top-[16%] -left-[6%] w-[540px] h-[540px] rounded-full bg-[#38D9E8]/15 blur-[130px]" />

          {/* Top-Right: Deep Electric Blue Lighting */}
          <div className="absolute -top-[10%] right-[8%] w-[620px] h-[620px] rounded-full bg-[#4B9DFF]/14 blur-[150px]" />

          {/* Specular Torus / Ring Light Diffusion (Glassmorphism-scaled.jpg inspired) */}
          <div className="absolute top-[22%] right-[12%] w-[520px] h-[520px] rounded-full border-[52px] border-white/[0.045] blur-[45px]" />
          <div className="absolute top-[48%] left-[4%] w-[380px] h-[380px] rounded-full bg-gradient-to-tr from-[#16B8B0]/22 via-[#38D9E8]/12 to-white/[0.04] blur-[60px]" />

          {/* Bottom-Right: Warm Orange Accent Glow */}
          <div className="absolute bottom-[4%] -right-[6%] w-[640px] h-[640px] rounded-full bg-[#FF793F]/15 blur-[160px]" />

          {/* Bottom-Left: Subtle Warm Amber Accent */}
          <div className="absolute -bottom-[12%] left-[18%] w-[560px] h-[560px] rounded-full bg-[#FFAD66]/10 blur-[150px]" />

          {/* Micro-dot grid texture for realistic visual depth */}
          <div className="absolute inset-0 bg-[radial-gradient(#ffffff0a_1px,transparent_1px)] [background-size:28px_28px] opacity-70" />
        </div>

        {/* Foreground Content Stack */}
        <div className="relative z-10 flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
