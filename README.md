# NUMERIX — Interactive Mathematical Learning Platform & Numerical Solver

<p align="center">
  <strong>Understand the Mathematics. Visualize the Process. Verify the Results.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-2.0.0-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Next.js-15.5-black?logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/TailwindCSS-v4-38B2AC?logo=tailwind-css&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/KaTeX-LaTeX%20Math-3298DC" alt="KaTeX" />
  <img src="https://img.shields.io/badge/Tests-157%20Passing-brightgreen?logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/License-Educational%20%2F%20Open-blue" alt="License" />
</p>

---

## 1. What is NUMERIX?

**NUMERIX** is an interactive numerical methods workbench and mathematical learning platform built for university Numerical Methods Laboratory courses, STEM students, and self-study.

Rather than acting as a black-box calculator that merely outputs a final number, NUMERIX integrates an **Interactive Mathematical Learning Engine** directly into the numerical solver. Students can:

1. **Understand the Mathematical Concept:** View the theoretical basis and prerequisites (e.g., Intermediate Value Theorem, Taylor series linearization, Simpson's quadrature weights).
2. **Learn Governing Formulas:** Rendered in true academic **KaTeX LaTeX typography** with full variable definitions.
3. **Follow Concrete Substitutions:** Inspect exact numerical substitutions at every step.
4. **Trace Intermediate Calculations:** Follow multi-line calculations without hand-waving or fake intermediate values.
5. **Understand Algorithmic Decisions:** Understand why a subinterval was retained, why rows were swapped in partial pivoting, or why corrector slopes were averaged.
6. **Cross-Tab Synchronization:** Click **"Jump to Iteration $X$"** to navigate directly to the iteration history table with high-contrast highlighting, and return seamlessly with **"Return to Lesson"**.
7. **Verify Convergence:** Review residual norms, error bounds, and mathematical verifications.
8. **Test Understanding:** Interactive multiple-choice **Knowledge Check questions** with immediate feedback, hints, and retries.

---

## 2. Architecture Overview

```
                               ┌─────────────────────────────────────────────────────────┐
                               │           NUMERIX Next.js Web Frontend (TS)             │
                               │  - Light Glassmorphism UI (Scientific Workspace)        │
                               │  - Interactive Math Keyboard & Dynamic Matrix Editor    │
                               │  - Solution Tab: Stepper, Derivations & Knowledge Check │
                               │  - KaTeX Mathematical Typography & Interactive Charts   │
                               └────────────────────────────┬────────────────────────────┘
                                                            │ REST JSON API
                                                            ▼
┌─────────────────────────────────┐          ┌───────────────────────────────────────────┐
│  NUMERIX Desktop App (Tkinter)  │          │          FastAPI Backend Service          │
│  - Offline Dark Glass GUI       │          │  - Pydantic Request/Response Validation   │
│  - Matplotlib Canvas Plots      │          │  - Endpoints: /api/solve/root, /ode...    │
│  - Native Windowed Execution    │          │  - Dedicated /api/learning Endpoints      │
└────────────────┬────────────────┘          └─────────────────────┬─────────────────────┘
                 │                                                 │
                 └─────────────────────────┬───────────────────────┘
                                           ▼
                 ┌────────────────────────────────────────────────────────┐
                 │               NUMERIX Python Engine Core               │
                 │  - 8 Numerical Algorithms (Root, Linear, ODE)          │
                 │  - Safe SymPy Mathematical Parser (No eval/exec)       │
                 │  - Comprehensive Metrics (Errors, Residuals, Timing)   │
                 └─────────────────────────┬──────────────────────────────┘
                                           │ ProblemRequest + SolverResult
                                           ▼
                 ┌────────────────────────────────────────────────────────┐
                 │          NUMERIX Mathematical Learning Engine          │
                 │  - 8 Method-Specific Lesson Generators                 │
                 │  - Formula & Concept Registries                        │
                 │  - Deterministic Knowledge Check System                │
                 │  - Typed Pydantic Models (SolutionDocument)            │
                 └────────────────────────────────────────────────────────┘
```

---

## 3. Supported Numerical Algorithms & Learning Modules

| Module | Algorithm | Educational Derivation & Features |
|---|---|---|
| **Root Finding** | **Bisection Method** | Intermediate Value Theorem, bracket validation ($f(a) \cdot f(b) < 0$), midpoint substitution, subinterval selection, theoretical error bound $\frac{b_0 - a_0}{2^n}$, stopping criteria. |
| | **False Position (Regula Falsi)** | Secant-line interpolation vs. midpoint halving, chord formula $c = \frac{a f(b) - b f(a)}{f(b) - f(a)}$, endpoint replacement, one-sided stagnation analysis. |
| | **Newton-Raphson Method** | 1st-order Taylor linearization, symbolic differentiation via SymPy, tangent line $x$-intercept $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$, horizontal tangent guard, quadratic convergence. |
| **Linear Systems** | **Gaussian Elimination** | Augmented matrix $[A \mid b]$, partial pivoting (row swaps for column max), elimination multipliers $m_{j,i}$, row operations, back-substitution, residual norm $\|Ax - b\|_2$. |
| | **Gauss-Jordan Elimination** | Pivot normalization ($R_i \leftarrow R_i / A_{i,i}$), elimination above & below pivots, transformation to Reduced Row Echelon Form (RREF) $[I \mid x]$, direct solution extraction. |
| **Differential Equations** | **Euler's Method** | Initial Value Problem (IVP), step size $h$, tangent slope $f(x_n, y_n)$, forward Euler update $y_{n+1} = y_n + h f(x_n, y_n)$, $\mathcal{O}(h)$ truncation error. |
| | **Modified Euler (Heun)** | Two-stage predictor-corrector, trial Euler step $y^*_{n+1}$, corrector slope $f(x_{n+1}, y^*_{n+1})$, average slope $\frac{f_1 + f_2}{2}$, 2nd-order accuracy $\mathcal{O}(h^2)$. |
| | **Runge-Kutta 4th Order (RK4)**| Multi-stage slope sampling ($k_1, k_2, k_3, k_4$), Simpson's rule weighting $\frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)$, 4th-order global accuracy $\mathcal{O}(h^4)$. |

---

## 4. Quick Start (Web Application)

### Prerequisites
- **Python 3.10+** (tested on Python 3.11, 3.12, 3.14)
- **Node.js 18+** & **npm**

### 1. Launch the FastAPI Backend

```bash
# In the repository root
pip install -r MAIN/backend/requirements.txt

# Start the server (runs on port 8000)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

- **API Documentation (Swagger UI):** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc):** [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)
- **Health Check:** [`http://127.0.0.1:8000/api/health`](http://127.0.0.1:8000/api/health)

### 2. Launch the Next.js Frontend

```bash
cd MAIN/frontend
npm install
npm run dev
```

Open [`http://localhost:3000`](http://localhost:3000) in your web browser.

---

## 5. Offline Desktop Application (Tkinter)

The original standalone desktop application is preserved and available for environments without web connectivity:

```bash
cd MAIN
pip install -r requirements.txt
python main.py
```

---

## 6. Running the Automated Test Suite

NUMERIX features a comprehensive test suite covering mathematical algorithms, safe parsing, API schemas, and the learning engine:

```bash
# Set PYTHONPATH and run all 157 automated tests
$env:PYTHONPATH="E:\NUMERIX\MAIN"
python -m pytest MAIN/numerix/tests/ MAIN/backend/tests/ -v
```

**157 tests pass with 100% green status:**
- **22 Root Finding Tests:** Bisection, False Position, Newton-Raphson accuracy and convergence
- **16 Linear Systems Tests:** Gaussian Elimination, Gauss-Jordan, partial pivoting, singular matrices
- **19 Differential Equations Tests:** Euler, Modified Euler, RK4, step halving, analytical comparison
- **16 Expression Parser Tests:** Safe mathematical token validation
- **15 Adversarial Security Tests:** Blocked malicious tokens, unauthorized symbols
- **15 Solver & Comparison Engine Tests:** Multi-method comparisons, metrics verification
- **21 GUI & Integration Tests:** Unified engine execution
- **16 FastAPI REST API Tests:** Request validation and response schemas
- **17 Learning Engine & API Tests:** Solution document generation, formulas, knowledge checks, edge cases

---

## 7. Project Structure

```
NUMERIX/
├── MAIN/
│   ├── backend/                    # FastAPI REST API
│   │   ├── api/
│   │   │   ├── routes/             # Root finding, linear systems, ODE, learning routes
│   │   │   └── schemas/            # Pydantic request and response schemas
│   │   ├── tests/                  # API endpoint unit tests
│   │   ├── Dockerfile              # Container deployment
│   │   └── main.py                 # Backend application entry point
│   ├── frontend/                   # Next.js 15 + Tailwind CSS Web Client
│   │   ├── public/                 # Static assets
│   │   └── src/
│   │       ├── app/                # App Router pages (Root, Linear, ODE, Learning...)
│   │       ├── components/
│   │       │   ├── learning/       # SolutionTab, Stepper, FormulaCard, KnowledgeCheck...
│   │       │   ├── math-view.tsx   # KaTeX Mathematical Typography Renderer
│   │       │   └── interactive-chart.tsx # Plotly.js visualizer
│   │       └── lib/
│   │           └── api.ts          # Typed API client & data interfaces
│   ├── numerix/                    # Python Core Numerical & Educational Package
│   │   ├── algorithms/             # 8 Audited numerical algorithms
│   │   │   ├── linear_systems/
│   │   │   ├── ode/
│   │   │   └── root_finding/
│   │   ├── core/                   # Result models, expression parser, validators
│   │   ├── engine/                 # Solver engine & comparison engine
│   │   ├── gui/                    # Tkinter offline desktop GUI
│   │   ├── learning/               # Mathematical Learning Subsystem
│   │   │   ├── concept_registry.py # Objectives, prerequisites, convergence notes
│   │   │   ├── formula_registry.py # Governing formulas & variable definitions
│   │   │   ├── learning_engine.py  # LearningEngine orchestrator
│   │   │   ├── solution_models.py  # Typed Pydantic models (SolutionDocument, etc.)
│   │   │   ├── knowledge_checks/   # Deterministic assessment question generator
│   │   │   └── solution_generators/# 8 Method-specific lesson generators
│   │   └── tests/                  # Core numerical and learning engine tests
│   ├── docs/                       # Architectural and user reference guides
│   ├── .gitignore                  # Git exclusion rules
│   ├── README.md                   # Product documentation
│   └── requirements.txt            # Python dependencies
├── .gitignore                      # Workspace root git ignore
└── README.md                       # Workspace root documentation
```

---

## 8. Deployment

- **Backend (Render / Railway / Docker):** Deploy using `MAIN/backend/Dockerfile` or configure `render.yaml`.
- **Frontend (Vercel):** Zero-configuration Next.js deployment. Set `NEXT_PUBLIC_API_URL` to point to your live FastAPI backend URL.

---

## 9. License & Academic Integrity

NUMERIX is designed as an educational tool for university laboratory instruction, academic research, and engineering mathematics self-study. Free and open for educational use.
