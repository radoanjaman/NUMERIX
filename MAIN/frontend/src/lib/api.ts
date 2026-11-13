/**
 * NUMERIX Web API Client
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface IterationItem {
  n: number;
  values: Record<string, any>;
  approximate_error?: number | null;
  extra?: Record<string, any>;
}

export interface MetricsResponse {
  iterations: number;
  execution_time_seconds: number;
  final_approximate_error?: number | null;
  final_residual?: number | null;
  final_exact_error?: number | null;
}

export interface GraphCurveData {
  x: number[];
  y: number[];
  label: string;
  type?: string;
}

export interface KnowledgeCheckQuestion {
  id: string;
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
  question_type: string;
  hint?: string | null;
}

export interface VariableDefinition {
  symbol: string;
  name: string;
  description: string;
  current_value?: string | null;
}

export interface FormulaCardModel {
  name: string;
  latex: string;
  description: string;
  variables: VariableDefinition[];
}

export interface SolutionStep {
  step_number: number;
  step_type: string;
  title: string;
  concept?: string | null;
  explanation: string;
  formula_latex?: string | null;
  substitution_latex?: string | null;
  calculation_latex?: string | null;
  result_latex?: string | null;
  decision?: string | null;
  related_iteration?: number | null;
  related_operation?: string | null;
  related_plot_data?: Record<string, any> | null;
  checkpoint_question?: KnowledgeCheckQuestion | null;
  variable_definitions: VariableDefinition[];
  matrix_snapshot?: number[][] | null;
  substeps: string[];
}

export interface FinalInterpretation {
  summary: string;
  root_or_solution: string;
  iterations_count: number;
  stopping_reason: string;
  accuracy_achieved: string;
  verification: string;
}

export interface SolutionDocument {
  method: string;
  topic: string;
  problem_statement: string;
  one_sentence_purpose?: string;
  essential_formula?: FormulaCardModel | null;
  worked_step?: SolutionStep | null;
  what_changes_next?: string;
  remaining_iterations_summary?: string;
  learning_objectives: string[];
  prerequisites: string[];
  formulas: FormulaCardModel[];
  steps: SolutionStep[];
  final_interpretation: FinalInterpretation;
  practice_questions: KnowledgeCheckQuestion[];
  detailed_theory?: string | null;
}

export interface SolverAPIResponse {
  method: string;
  problem_type: string;
  status: string;
  termination_reason: string;
  success: boolean;

  root?: number | null;
  f_root?: number | null;
  solution_vector?: number[] | null;
  ode_table?: Array<Record<string, any>> | null;

  iterations: IterationItem[];
  metrics: MetricsResponse;
  curves: GraphCurveData[];
  markers: Array<{ x: number; y: number; label: string; color?: string }>;
  warnings: string[];
  extra: Record<string, any>;
  solution_document?: SolutionDocument | null;
}

export interface MethodComparisonItem {
  method: string;
  solution_summary: string;
  iterations_or_steps: number;
  final_error_or_residual?: number | null;
  execution_time_seconds: number;
  status: string;
  raw_result: SolverAPIResponse;
}

export interface ComparisonAPIResponse {
  category: string;
  items: MethodComparisonItem[];
  curves: GraphCurveData[];
}

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || `Server error (${res.status})`);
    }
    return data as T;
  } catch (err: any) {
    if (err.message === "Failed to fetch" || err.name === "TypeError") {
      throw new Error(`Unable to connect to NUMERIX API at ${API_BASE_URL}. Ensure the backend is running.`);
    }
    throw err;
  }
}

export async function checkHealth(): Promise<{ status: string; app: string; version: string }> {
  return request("/api/health");
}

export async function getSupportedMethods(): Promise<any> {
  return request("/api/methods");
}

export async function solveRootFinding(payload: {
  method: string;
  expression: string;
  a?: number | null;
  b?: number | null;
  x0?: number | null;
  tol?: number;
  max_iter?: number;
}): Promise<SolverAPIResponse> {
  return request("/api/solve/root", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function solveLinearSystem(payload: {
  method: string;
  A: number[][];
  b: number[];
}): Promise<SolverAPIResponse> {
  return request("/api/solve/linear", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function solveODE(payload: {
  method: string;
  expression: string;
  x0: number;
  y0: number;
  h: number;
  x_end: number;
  exact_expression?: string | null;
}): Promise<SolverAPIResponse> {
  return request("/api/solve/ode", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function compareMethods(payload: {
  category: "root_finding" | "linear_systems" | "ode";
  methods: string[];
  root_input?: any;
  linear_input?: any;
  ode_input?: any;
}): Promise<ComparisonAPIResponse> {
  return request("/api/compare", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
