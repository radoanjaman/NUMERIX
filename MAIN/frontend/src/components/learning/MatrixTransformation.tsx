"use client";

import React from "react";
import { Grid } from "lucide-react";

interface MatrixTransformationProps {
  matrix: number[][];
  title?: string;
  operationDescription?: string | null;
}

export function MatrixTransformation({
  matrix,
  title = "Current Augmented Matrix [A | b]",
  operationDescription,
}: MatrixTransformationProps) {
  if (!matrix || matrix.length === 0) return null;
  const numRows = matrix.length;
  const numCols = matrix[0]?.length || 0;
  const aCols = numCols - 1; // Last column is b vector

  return (
    <div className="glass-card rounded-2xl p-4 sm:p-5 border border-white/[0.12] bg-[#111820]/60 space-y-3">
      <div className="flex items-center justify-between text-xs font-semibold text-[#38D9E8]">
        <div className="flex items-center space-x-2">
          <Grid className="w-4 h-4 text-[#16B8B0]" />
          <span className="uppercase tracking-wider">{title}</span>
        </div>
        {operationDescription && (
          <span className="font-mono text-[11px] bg-white/[0.06] px-2.5 py-1 rounded-lg border border-white/[0.12] text-[#38D9E8]">
            {operationDescription}
          </span>
        )}
      </div>

      <div className="overflow-x-auto py-2">
        <div className="inline-block min-w-full align-middle">
          <table className="border-collapse font-mono text-xs text-center border-y border-white/[0.15]">
            <tbody>
              {matrix.map((row, rIdx) => (
                <tr key={rIdx} className="hover:bg-white/[0.03] transition-colors">
                  {row.map((val, cIdx) => {
                    const isAugmented = cIdx === aCols;
                    const isDiagonal = rIdx === cIdx;
                    return (
                      <td
                        key={cIdx}
                        className={`px-3.5 py-2 border-x border-white/[0.08] ${
                          isAugmented ? "border-l-2 border-l-[#FF793F]/60 font-bold bg-[#FF793F]/5 text-[#FFAD66]" : ""
                        } ${isDiagonal ? "font-bold text-[#38D9E8] bg-[#38D9E8]/10" : "text-[#B5C0CC]"}`}
                      >
                        {val !== null && val !== undefined ? (Math.abs(val) < 1e-12 ? "0" : Number(val.toFixed(4))) : "0"}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
