"use client";

import React from "react";

interface MathKeyboardProps {
  onInsert: (symbol: string) => void;
  showY?: boolean;
}

export function MathKeyboard({ onInsert, showY = false }: MathKeyboardProps) {
  const commonKeys = [
    { label: "x²", value: "**2" },
    { label: "x³", value: "**3" },
    { label: "xⁿ", value: "**" },
    { label: "√x", value: "sqrt(" },
    { label: "sin", value: "sin(" },
    { label: "cos", value: "cos(" },
    { label: "tan", value: "tan(" },
    { label: "eˣ", value: "exp(" },
    { label: "ln", value: "log(" },
    { label: "π", value: "pi" },
    { label: "e", value: "e" },
    { label: "(", value: "(" },
    { label: ")", value: ")" },
    { label: "+", value: " + " },
    { label: "-", value: " - " },
    { label: "×", value: "*" },
    { label: "÷", value: "/" },
  ];

  return (
    <div className="w-full bg-white/[0.03] p-2.5 rounded-xl border border-white/[0.08] backdrop-blur-md flex flex-wrap gap-1.5 items-center">
      <span className="text-[10px] font-bold text-[#7E8A98] uppercase tracking-wider px-1">Math Pad:</span>
      <button
        type="button"
        onClick={() => onInsert("x")}
        className="math-key px-2.5 py-1 text-xs font-mono font-bold rounded-lg cursor-pointer"
      >
        x
      </button>
      {showY && (
        <button
          type="button"
          onClick={() => onInsert("y")}
          className="math-key px-2.5 py-1 text-xs font-mono font-bold rounded-lg cursor-pointer text-[#38D9E8]"
        >
          y
        </button>
      )}
      {commonKeys.map((k) => (
        <button
          key={k.label}
          type="button"
          onClick={() => onInsert(k.value)}
          className="math-key px-2.5 py-1 text-xs font-mono font-semibold rounded-lg cursor-pointer"
        >
          {k.label}
        </button>
      ))}
      <button
        type="button"
        onClick={() => onInsert("abs(")}
        className="math-key px-2.5 py-1 text-xs font-mono font-semibold rounded-lg cursor-pointer"
      >
        |x|
      </button>
    </div>
  );
}
