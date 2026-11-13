"use client";

import React, { useMemo } from "react";
import katex from "katex";

interface MathViewProps {
  math?: string;
  text?: string;
  display?: boolean;
  className?: string;
  children?: React.ReactNode;
}

/**
 * Clean up raw math strings before sending to KaTeX.
 * Strips accidental wrapping delimiters ($...$, $$...$$, \(...\), \[...\])
 * and normalizes common whitespace issues.
 */
function cleanMathString(raw: string): string {
  if (!raw) return "";
  let s = raw.trim();

  // Strip $$...$$ or \[...\]
  if (s.startsWith("$$") && s.endsWith("$$") && s.length >= 4) {
    s = s.slice(2, -2).trim();
  } else if (s.startsWith("\\[") && s.endsWith("\\]") && s.length >= 4) {
    s = s.slice(2, -2).trim();
  }
  // Strip $...$ or \(...\)
  else if (s.startsWith("$") && s.endsWith("$") && s.length >= 2) {
    s = s.slice(1, -1).trim();
  } else if (s.startsWith("\\(") && s.endsWith("\\)") && s.length >= 4) {
    s = s.slice(2, -2).trim();
  }

  return s;
}

/**
 * Render a single pure LaTeX expression using KaTeX.
 * Falls back to clean formatted text if KaTeX encounters an error.
 */
export function renderKaTeX(latex: string, displayMode: boolean = false): string {
  const clean = cleanMathString(latex);
  if (!clean) return "";

  try {
    return katex.renderToString(clean, {
      displayMode,
      throwOnError: false,
      strict: false,
      trust: false,
    });
  } catch (err) {
    console.warn("KaTeX render error on string:", clean, err);
    return `<span class="katex-fallback">${clean}</span>`;
  }
}

/**
 * Regex matching both display math ($$...$$, \[...\]) and inline math ($...$, \(...\)).
 * Captures:
 * 1: $$...$$
 * 2: \[...\]
 * 3: $...$
 * 4: \(...\)
 */
const MATH_REGEX = /(?:\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\$([^\$\n]+?)\$|\\\(([\s\S]+?)\\\))/g;

/**
 * Parses mixed text containing inline ($...$, \(...\)) and display ($$...$$, \[...\])
 * mathematical expressions and returns an array of React nodes with KaTeX rendered math.
 */
export function renderMathInText(content: string): React.ReactNode {
  if (!content) return null;
  if (typeof content !== "string") return content;

  // Quick check if string contains any potential math delimiter
  if (!content.includes("$") && !content.includes("\\(") && !content.includes("\\[")) {
    return content;
  }

  const elements: React.ReactNode[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  // Reset regex state
  MATH_REGEX.lastIndex = 0;

  while ((match = MATH_REGEX.exec(content)) !== null) {
    // Add text preceding the math match
    if (match.index > lastIndex) {
      elements.push(content.substring(lastIndex, match.index));
    }

    const isDisplay = Boolean(match[1] || match[2]);
    const mathContent = match[1] || match[2] || match[3] || match[4] || "";
    const html = renderKaTeX(mathContent, isDisplay);

    if (isDisplay) {
      elements.push(
        <span
          key={`math-disp-${match.index}`}
          className="block my-2 overflow-x-auto text-center"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      );
    } else {
      elements.push(
        <span
          key={`math-in-${match.index}`}
          className="inline-block align-baseline mx-0.5"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      );
    }

    lastIndex = match.index + match[0].length;
  }

  // Add trailing text after the last match
  if (lastIndex < content.length) {
    elements.push(content.substring(lastIndex));
  }

  return <>{elements}</>;
}

/**
 * Universal component for rendering mathematics.
 * - If `text` is provided (or children string): renders mixed text with inline/display math.
 * - If `math` is provided: renders pure formula via KaTeX in inline or display mode.
 */
export function MathView({
  math,
  text,
  display = false,
  className = "",
  children,
}: MathViewProps) {
  // Case 1: Text prop provided or string children
  const textContent = text ?? (typeof children === "string" ? children : undefined);
  if (textContent !== undefined) {
    return (
      <span className={`inline-block ${className}`}>
        {renderMathInText(textContent)}
      </span>
    );
  }

  // Case 2: Pure math prop provided
  const rawMath = math || "";
  const html = useMemo(() => {
    if (!rawMath.trim()) return "";
    return renderKaTeX(rawMath, display);
  }, [rawMath, display]);

  if (!html) return null;

  if (display) {
    return (
      <div
        className={`overflow-x-auto py-1.5 scrollbar-thin ${className}`}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  }

  return (
    <span
      className={`inline-block align-baseline ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

/**
 * Convenient shorthand component for rendering prose containing embedded LaTeX equations.
 * e.g. <MathText text="Find root of $f(x) = x^3 - 2 = 0$ on $[1, 2]$." />
 */
export function MathText({
  text,
  className = "",
  as: Component = "span",
}: {
  text: string;
  className?: string;
  as?: React.ElementType;
}) {
  if (!text) return null;

  return (
    <Component className={className}>
      {renderMathInText(text)}
    </Component>
  );
}

export default MathView;
