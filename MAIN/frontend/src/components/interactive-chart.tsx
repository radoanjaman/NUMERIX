"use client";

import React, { useState } from "react";
import { GraphCurveData } from "@/lib/api";

interface InteractiveChartProps {
  curves: GraphCurveData[];
  markers?: Array<{ x: number; y: number; label: string; color?: string }>;
  title?: string;
  xLabel?: string;
  yLabel?: string;
  height?: number;
}

/**
 * Generates nicely rounded tick values for scientific axes.
 */
function generateNiceTicks(min: number, max: number, targetCount = 5): number[] {
  if (min === max) {
    return [min - 1, min, min + 1];
  }
  const span = max - min;
  const rawStep = span / targetCount;
  const magnitude = Math.pow(10, Math.floor(Math.log10(rawStep)));
  const normalized = rawStep / magnitude;

  let step = magnitude;
  if (normalized > 5) step = 10 * magnitude;
  else if (normalized > 2) step = 5 * magnitude;
  else if (normalized > 1) step = 2 * magnitude;
  else step = magnitude;

  const start = Math.floor(min / step) * step;
  const end = Math.ceil(max / step) * step;
  const ticks: number[] = [];

  for (let val = start; val <= end + step * 0.001; val += step) {
    const clean = Math.abs(val) < 1e-12 ? 0 : Number(val.toFixed(6));
    ticks.push(clean);
  }
  return ticks.length >= 2 ? ticks : [min, (min + max) / 2, max];
}

export function InteractiveChart({
  curves = [],
  markers = [],
  title = "Numerical Solution Visualization",
  xLabel = "x",
  yLabel = "y / f(x)",
  height = 390,
}: InteractiveChartProps) {
  const [hoveredPoint, setHoveredPoint] = useState<{ x: number; y: number; label: string } | null>(null);

  if (!curves || curves.length === 0) {
    return (
      <div
        className="glass-card rounded-2xl border border-white/[0.10] p-8 flex flex-col items-center justify-center text-[#7E8A98] text-sm"
        style={{ height }}
      >
        <div className="w-10 h-10 rounded-xl bg-white/[0.04] border border-white/[0.08] flex items-center justify-center mb-3 text-[#38D9E8]">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
          </svg>
        </div>
        <span className="font-medium text-[#F5F7FA] mb-1">No Plot Available</span>
        <span>Run a calculation to render the interactive curve and markers.</span>
      </div>
    );
  }

  // Detect whether this is a discrete bar chart
  const isBarChart = curves.some((c) => c.type === "bar");

  // Standard scientific chart layout dimensions
  const viewWidth = 760;
  const viewHeight = Math.max(380, height);

  // Exact recommended margins for four distinct regions:
  // Top: 38px (title & legend clearance)
  // Right: 30px
  // Bottom: 82px (tick labels + axis title separation)
  // Left: 72px (Y-axis tick labels + rotated Y title)
  const margin = { top: 38, right: 30, bottom: 82, left: 72 };
  const plotWidth = viewWidth - margin.left - margin.right;
  const plotHeight = viewHeight - margin.top - margin.bottom;
  const plotBottom = margin.top + plotHeight;

  // Futuristic NUMERIX glass palette: Cyan, Teal, Electric Blue, Orange, Warm Amber
  const colors = ["#38D9E8", "#16B8B0", "#4B9DFF", "#FF793F", "#FFAD66"];

  if (isBarChart) {
    // ══════════════════════════════════════════════════════════════════════════
    // MODE 1: DISCRETE CATEGORICAL BAR CHART (e.g. Linear Systems Solutions)
    // ══════════════════════════════════════════════════════════════════════════
    const primaryBarCurve = curves.find((c) => c.type === "bar") || curves[0];
    const numBars = primaryBarCurve.x.length;

    // Y Domain: Must include 0 as baseline with proportional top/bottom headroom
    const allYValues = primaryBarCurve.y;
    let rawMinY = Math.min(0, ...allYValues);
    let rawMaxY = Math.max(0, ...allYValues);

    if (rawMinY === 0 && rawMaxY === 0) {
      rawMinY = -1;
      rawMaxY = 1;
    }

    const spanY = rawMaxY - rawMinY || 1;
    const topHeadroom = spanY * 0.18;
    const bottomHeadroom = rawMinY < 0 ? spanY * 0.18 : 0;

    const yDomainMax = rawMaxY + topHeadroom;
    const yDomainMin = rawMinY - bottomHeadroom;

    const scaleY = (y: number) =>
      margin.top + (1 - (y - yDomainMin) / (yDomainMax - yDomainMin)) * plotHeight;

    const baselineY = scaleY(0);

    // Generate nice Y ticks
    const yTicks = generateNiceTicks(yDomainMin, yDomainMax, 5).filter(
      (t) => t >= yDomainMin && t <= yDomainMax
    );

    // Slot layout along X
    const slotWidth = plotWidth / numBars;
    const barWidth = Math.min(54, Math.max(26, slotWidth * 0.48));

    return (
      <div className="w-full glass-panel rounded-2xl border border-white/[0.12] p-5 shadow-2xl relative overflow-hidden">
        {/* Subtle top reflection sheen */}
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

        {/* Region 1: Chart Header & Legend */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3 pb-3 border-b border-white/[0.08]">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-[#38D9E8] shadow-[0_0_8px_rgba(56,217,232,0.8)]" />
            <h3 className="text-sm font-semibold text-[#F5F7FA] tracking-tight">{title}</h3>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-xs">
            {curves.map((c, i) => (
              <div
                key={c.label}
                className="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-white/[0.04] border border-white/[0.08]"
              >
                <span
                  className="w-2.5 h-2.5 rounded-sm inline-block shadow-sm"
                  style={{ backgroundColor: colors[i % colors.length] }}
                />
                <span className="text-[#B5C0CC] font-mono text-[11px] font-medium">{c.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Region 2, 3, 4: SVG Plot Canvas */}
        <div className="relative w-full overflow-hidden">
          <svg
            viewBox={`0 0 ${viewWidth} ${viewHeight}`}
            className="w-full h-auto select-none font-sans"
          >
            <defs>
              <linearGradient id="barTealGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38D9E8" stop-opacity="0.95" />
                <stop offset="100%" stop-color="#16B8B0" stop-opacity="0.75" />
              </linearGradient>
              <linearGradient id="barOrangeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#FF793F" stop-opacity="0.95" />
                <stop offset="100%" stop-color="#D9531E" stop-opacity="0.75" />
              </linearGradient>
              <filter id="barGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#16B8B0" flood-opacity="0.25" />
              </filter>
            </defs>

            {/* Plot Area Background Frame */}
            <rect
              x={margin.left}
              y={margin.top}
              width={plotWidth}
              height={plotHeight}
              fill="rgba(8, 12, 18, 0.45)"
              stroke="rgba(255, 255, 255, 0.08)"
              strokeWidth="1"
              rx="6"
            />

            {/* Y-Axis Horizontal Grid Lines & Ticks */}
            {yTicks.map((yt, i) => {
              const py = scaleY(yt);
              return (
                <g key={`ygrid-${i}`}>
                  <line
                    x1={margin.left}
                    y1={py}
                    x2={margin.left + plotWidth}
                    y2={py}
                    stroke={yt === 0 ? "rgba(255, 255, 255, 0.28)" : "rgba(255, 255, 255, 0.07)"}
                    strokeDasharray={yt === 0 ? undefined : "3 3"}
                    strokeWidth={yt === 0 ? "1.5" : "1"}
                  />
                  <text
                    x={margin.left - 12}
                    y={py + 3.5}
                    fill={yt === 0 ? "#F5F7FA" : "#7E8A98"}
                    fontSize="11"
                    fontWeight={yt === 0 ? "700" : "500"}
                    textAnchor="end"
                    fontFamily="monospace"
                  >
                    {yt >= 0 ? `+${yt.toFixed(2)}` : yt.toFixed(2)}
                  </text>
                </g>
              );
            })}

            {/* Baseline y = 0 Highlight (if within plot) */}
            {baselineY >= margin.top && baselineY <= plotBottom && (
              <line
                x1={margin.left}
                y1={baselineY}
                x2={margin.left + plotWidth}
                y2={baselineY}
                stroke="#38D9E8"
                strokeWidth="1.5"
                strokeOpacity="0.45"
              />
            )}

            {/* Region 2: Rendered Solution Coordinate Bars */}
            {primaryBarCurve.x.map((xv, idx) => {
              const yv = primaryBarCurve.y[idx];
              const barCenterX = margin.left + (idx + 0.5) * slotWidth;
              const barX = barCenterX - barWidth / 2;

              const pyVal = scaleY(yv);
              const isPositive = yv >= 0;

              const barTop = isPositive ? pyVal : baselineY;
              const barHeight = Math.max(3, Math.abs(baselineY - pyVal));

              const isHovered =
                hoveredPoint !== null && hoveredPoint.x === xv && hoveredPoint.y === yv;

              return (
                <g key={`bar-${idx}`}>
                  {/* Subtle vertical column guide */}
                  <line
                    x1={barCenterX}
                    y1={margin.top}
                    x2={barCenterX}
                    y2={plotBottom}
                    stroke="rgba(255, 255, 255, 0.03)"
                    strokeWidth="1"
                  />

                  {/* The Bar Element */}
                  <rect
                    x={barX}
                    y={barTop}
                    width={barWidth}
                    height={barHeight}
                    fill={isPositive ? "url(#barTealGradient)" : "url(#barOrangeGradient)"}
                    stroke={isPositive ? "rgba(56, 217, 232, 0.85)" : "rgba(255, 121, 63, 0.85)"}
                    strokeWidth={isHovered ? "2" : "1"}
                    rx="5"
                    filter="url(#barGlow)"
                    className="cursor-pointer transition-all duration-200"
                    opacity={isHovered ? 1 : 0.9}
                    onMouseEnter={() =>
                      setHoveredPoint({
                        x: xv,
                        y: yv,
                        label: `Variable x${xv}`,
                      })
                    }
                    onMouseLeave={() => setHoveredPoint(null)}
                  />

                  {/* Value Annotation (Directly above/below the bar with zero overlap) */}
                  <text
                    x={barCenterX}
                    y={isPositive ? barTop - 8 : barTop + barHeight + 14}
                    fill={isPositive ? "#38D9E8" : "#FF793F"}
                    fontSize="11"
                    fontWeight="700"
                    fontFamily="monospace"
                    textAnchor="middle"
                  >
                    {yv >= 0 ? `+${yv.toFixed(3)}` : yv.toFixed(3)}
                  </text>

                  {/* Region 3: X-Axis Tick Mark (Below Plot Frame) */}
                  <line
                    x1={barCenterX}
                    y1={plotBottom}
                    x2={barCenterX}
                    y2={plotBottom + 6}
                    stroke="rgba(255, 255, 255, 0.35)"
                    strokeWidth="1.5"
                  />

                  {/* Region 3: X-Axis Tick Label (Centered beneath each corresponding bar) */}
                  <text
                    x={barCenterX}
                    y={plotBottom + 24}
                    fill="#F5F7FA"
                    fontSize="12"
                    fontWeight="600"
                    textAnchor="middle"
                    fontFamily="monospace"
                  >
                    x<tspan fontSize="10" dy="2">{xv}</tspan>
                  </text>

                  <text
                    x={barCenterX}
                    y={plotBottom + 40}
                    fill="#7E8A98"
                    fontSize="9.5"
                    fontFamily="monospace"
                    textAnchor="middle"
                  >
                    (idx {xv})
                  </text>
                </g>
              );
            })}

            {/* Region 4: X-Axis Title (Sufficient separation below tick labels) */}
            <text
              x={margin.left + plotWidth / 2}
              y={plotBottom + 64}
              fill="#B5C0CC"
              fontSize="12"
              fontWeight="700"
              letterSpacing="0.5"
              textAnchor="middle"
            >
              {xLabel}
            </text>

            {/* Y-Axis Title (Rotated on the Left) */}
            <text
              x={22}
              y={margin.top + plotHeight / 2}
              fill="#B5C0CC"
              fontSize="12"
              fontWeight="700"
              letterSpacing="0.5"
              textAnchor="middle"
              transform={`rotate(-90 22 ${margin.top + plotHeight / 2})`}
            >
              {yLabel}
            </text>
          </svg>

          {/* Interactive Tooltip on Hover */}
          {hoveredPoint && (
            <div className="absolute top-3 right-5 bg-[#080B10]/95 backdrop-blur-md text-[#F5F7FA] text-xs font-mono px-3.5 py-2 rounded-xl shadow-2xl border border-white/20 pointer-events-none flex items-center space-x-2">
              <span className="text-[#38D9E8] font-bold">{hoveredPoint.label}:</span>
              <span>value = {hoveredPoint.y.toFixed(6)}</span>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ══════════════════════════════════════════════════════════════════════════
  // MODE 2: CONTINUOUS SCIENTIFIC CURVE / LINE CHART (Root Finding & ODEs)
  // ══════════════════════════════════════════════════════════════════════════
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;

  for (const c of curves) {
    for (let i = 0; i < c.x.length; i++) {
      const xv = c.x[i];
      const yv = c.y[i];
      if (xv < minX) minX = xv;
      if (xv > maxX) maxX = xv;
      if (yv < minY) minY = yv;
      if (yv > maxY) maxY = yv;
    }
  }

  for (const m of markers) {
    if (m.x < minX) minX = m.x;
    if (m.x > maxX) maxX = m.x;
    if (m.y < minY) minY = m.y;
    if (m.y > maxY) maxY = m.y;
  }

  if (!isFinite(minX) || !isFinite(maxX) || minX === maxX) {
    minX = -5;
    maxX = 5;
  }
  if (!isFinite(minY) || !isFinite(maxY) || minY === maxY) {
    minY = -5;
    maxY = 5;
  }

  // Generous padding for clean domain bounds
  const padX = (maxX - minX) * 0.08 || 0.5;
  const padY = (maxY - minY) * 0.12 || 0.5;
  const x0 = minX - padX;
  const x1 = maxX + padX;
  const y0 = minY - padY;
  const y1 = maxY + padY;

  const scaleX = (x: number) => margin.left + ((x - x0) / (x1 - x0)) * plotWidth;
  const scaleY = (y: number) => margin.top + (1 - (y - y0) / (y1 - y0)) * plotHeight;

  // Generate 5-6 nice ticks
  const xTicks = generateNiceTicks(x0, x1, 5).filter((t) => t >= x0 && t <= x1);
  const yTicks = generateNiceTicks(y0, y1, 5).filter((t) => t >= y0 && t <= y1);

  return (
    <div className="w-full glass-panel rounded-2xl border border-white/[0.12] p-5 shadow-2xl relative overflow-hidden">
      {/* Subtle top reflection sheen */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />

      {/* Region 1: Chart Title & Legend */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3 pb-3 border-b border-white/[0.08]">
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-[#38D9E8] shadow-[0_0_8px_rgba(56,217,232,0.8)]" />
          <h3 className="text-sm font-semibold text-[#F5F7FA] tracking-tight">{title}</h3>
        </div>
        <div className="flex flex-wrap items-center gap-3 text-xs">
          {curves.map((c, i) => (
            <div
              key={c.label}
              className="flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-white/[0.04] border border-white/[0.08]"
            >
              <span
                className="w-2.5 h-1 rounded-full inline-block shadow-sm"
                style={{ backgroundColor: colors[i % colors.length] }}
              />
              <span className="text-[#B5C0CC] font-mono text-[11px] font-medium">{c.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Region 2, 3, 4: SVG Canvas */}
      <div className="relative w-full overflow-hidden">
        <svg
          viewBox={`0 0 ${viewWidth} ${viewHeight}`}
          className="w-full h-auto select-none font-sans"
        >
          {/* Plot Area Frame */}
          <rect
            x={margin.left}
            y={margin.top}
            width={plotWidth}
            height={plotHeight}
            fill="rgba(8, 12, 18, 0.45)"
            stroke="rgba(255, 255, 255, 0.08)"
            strokeWidth="1"
            rx="6"
          />

          {/* X-Axis Vertical Grid Lines & Ticks */}
          {xTicks.map((xt, i) => {
            const px = scaleX(xt);
            return (
              <g key={`xtick-${i}`}>
                <line
                  x1={px}
                  y1={margin.top}
                  x2={px}
                  y2={plotBottom}
                  stroke="rgba(255, 255, 255, 0.06)"
                  strokeDasharray="3 3"
                  strokeWidth="1"
                />
                {/* Region 3: X-Axis Tick Mark */}
                <line
                  x1={px}
                  y1={plotBottom}
                  x2={px}
                  y2={plotBottom + 6}
                  stroke="rgba(255, 255, 255, 0.3)"
                  strokeWidth="1.2"
                />
                {/* Region 3: X-Axis Tick Label */}
                <text
                  x={px}
                  y={plotBottom + 22}
                  fill="#7E8A98"
                  fontSize="11"
                  textAnchor="middle"
                  fontFamily="monospace"
                >
                  {xt.toFixed(2)}
                </text>
              </g>
            );
          })}

          {/* Y-Axis Horizontal Grid Lines & Ticks */}
          {yTicks.map((yt, i) => {
            const py = scaleY(yt);
            return (
              <g key={`ytick-${i}`}>
                <line
                  x1={margin.left}
                  y1={py}
                  x2={margin.left + plotWidth}
                  y2={py}
                  stroke={yt === 0 ? "rgba(255, 255, 255, 0.25)" : "rgba(255, 255, 255, 0.06)"}
                  strokeDasharray={yt === 0 ? undefined : "3 3"}
                  strokeWidth={yt === 0 ? "1.5" : "1"}
                />
                <text
                  x={margin.left - 12}
                  y={py + 3.5}
                  fill={yt === 0 ? "#F5F7FA" : "#7E8A98"}
                  fontSize="11"
                  fontWeight={yt === 0 ? "700" : "500"}
                  textAnchor="end"
                  fontFamily="monospace"
                >
                  {yt.toFixed(2)}
                </text>
              </g>
            );
          })}

          {/* Region 4: X-Axis Title (Sufficient separation below tick labels) */}
          <text
            x={margin.left + plotWidth / 2}
            y={plotBottom + 58}
            fill="#B5C0CC"
            fontSize="12"
            fontWeight="700"
            letterSpacing="0.5"
            textAnchor="middle"
          >
            {xLabel}
          </text>

          {/* Y-Axis Title (Rotated on the Left) */}
          <text
            x={22}
            y={margin.top + plotHeight / 2}
            fill="#B5C0CC"
            fontSize="12"
            fontWeight="700"
            letterSpacing="0.5"
            textAnchor="middle"
            transform={`rotate(-90 22 ${margin.top + plotHeight / 2})`}
          >
            {yLabel}
          </text>

          {/* Continuous Curves & Polylines */}
          {curves.map((c, i) => {
            const strokeColor = colors[i % colors.length];
            const isZeroLine = c.label.includes("y = 0");

            const points = c.x
              .map((xv, idx) => {
                const yv = c.y[idx];
                return `${scaleX(xv)},${scaleY(yv)}`;
              })
              .join(" ");

            return (
              <g key={c.label}>
                <polyline
                  fill="none"
                  stroke={isZeroLine ? "rgba(255, 255, 255, 0.25)" : strokeColor}
                  strokeWidth={isZeroLine ? "1.2" : "2.4"}
                  strokeDasharray={isZeroLine ? "4 4" : undefined}
                  points={points}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {/* Data point dots */}
                {c.x.length <= 40 &&
                  !isZeroLine &&
                  c.x.map((xv, idx) => (
                    <circle
                      key={idx}
                      cx={scaleX(xv)}
                      cy={scaleY(c.y[idx])}
                      r="4"
                      fill={strokeColor}
                      stroke="#080B10"
                      strokeWidth="1.5"
                      className="cursor-pointer hover:r-6 transition-all"
                      onMouseEnter={() =>
                        setHoveredPoint({ x: xv, y: c.y[idx], label: c.label })
                      }
                      onMouseLeave={() => setHoveredPoint(null)}
                    />
                  ))}
              </g>
            );
          })}

          {/* Markers (Roots / Pivots / Critical States) */}
          {markers.map((m, i) => {
            const mx = scaleX(m.x);
            const my = scaleY(m.y);
            return (
              <g key={`marker-${i}`}>
                <circle
                  cx={mx}
                  cy={my}
                  r="7"
                  fill="#FF793F"
                  stroke="#FFFFFF"
                  strokeWidth="2"
                  className="animate-pulse shadow-lg"
                />
                <rect
                  x={mx + 8}
                  y={my - 22}
                  width="100"
                  height="22"
                  rx="6"
                  fill="#080B10"
                  fillOpacity="0.85"
                  stroke="rgba(255, 255, 255, 0.18)"
                  strokeWidth="1"
                />
                <text
                  x={mx + 14}
                  y={my - 7}
                  fill="#FF793F"
                  fontSize="10"
                  fontWeight="600"
                  fontFamily="monospace"
                >
                  {m.label}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Tooltip on Hover */}
        {hoveredPoint && (
          <div className="absolute top-3 right-5 bg-[#080B10]/95 backdrop-blur-md text-[#F5F7FA] text-xs font-mono px-3.5 py-2 rounded-xl shadow-2xl border border-white/20 pointer-events-none flex items-center space-x-2">
            <span className="text-[#38D9E8] font-bold">{hoveredPoint.label}:</span>
            <span>
              x = {hoveredPoint.x.toFixed(4)}, y = {hoveredPoint.y.toFixed(4)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
