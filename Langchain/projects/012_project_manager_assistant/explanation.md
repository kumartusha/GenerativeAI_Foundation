# 🤖 AI-Powered Project Manager Assistant

> An intelligent project planning agent built with **LangChain**, **LangGraph**, and **Groq LLMs** that autonomously decomposes projects, schedules tasks, allocates resources, assesses risks, and iteratively optimizes the plan — mimicking a real-world project manager's decision-making process.

---

## 📌 Project Statement

### The Problem
Project planning is one of the most **time-consuming and error-prone** activities in software development. Traditional approaches require experienced project managers to manually:
- Break down vague requirements into actionable tasks
- Map complex inter-task dependencies
- Build realistic timelines respecting those dependencies
- Match tasks to team members based on skills and availability
- Identify and mitigate risks before they derail the project

This process typically takes **days to weeks** for a medium-sized project and is heavily dependent on the PM's experience and judgment. Mistakes in early planning cascade into delays, budget overruns, and team burnout.

### The Solution
This project builds an **autonomous AI Project Manager Agent** that takes a plain-text project description and a team roster (CSV) as inputs and automatically generates a complete, optimized project plan — including task breakdown, dependency mapping, scheduling, resource allocation, risk assessment, and iterative optimization.

The agent uses a **multi-node LangGraph workflow** where each planning phase is handled by a specialized LLM-powered node, and the entire pipeline self-improves through a feedback loop.

---

## 🌍 Impact of the Solution

| Dimension | Impact |
|-----------|--------|
| **Time Savings** | Reduces planning time from days/weeks to **minutes** |
| **Consistency** | Eliminates human bias and oversight — every task is evaluated systematically |
| **Risk Reduction** | Proactive risk scoring identifies bottlenecks before execution begins |
| **Iterative Optimization** | The agent self-improves its plan across multiple iterations, something human PMs rarely have time to do |
| **Accessibility** | Makes expert-level project planning available to teams without experienced PMs |
| **Scalability** | Can handle projects of any size — from 5-task sprints to 100+ task enterprise programs |
| **Documentation** | Produces structured, traceable planning artifacts (tasks, dependencies, schedule, allocations, risks) |

### Who Benefits?
- **Startup founders** who wear the PM hat but lack formal training
- **Engineering leads** who need a quick baseline plan for sprint planning
- **Consulting firms** who produce project plans for client proposals
- **Students & educators** learning Agile/project management methodology

---

## 🏗️ Technical Architecture

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM Provider** | Groq (qwen/qwen3-32b) | Fast inference for structured output generation |
| **Orchestration** | LangGraph | Directed acyclic graph (DAG) workflow with conditional routing |
| **Framework** | LangChain | LLM abstraction, structured output parsing, prompt chaining |
| **Data Models** | Pydantic v2 | Type-safe schema enforcement for LLM outputs |
| **State Management** | TypedDict + MemorySaver | Shared state across nodes with checkpoint persistence |
| **Visualization** | Plotly Express | Interactive Gantt chart generation |
| **Data Handling** | Pandas | CSV parsing and DataFrame manipulation |
| **Configuration** | python-dotenv | Secure environment variable management |

### Modular Architecture

The project follows a **clean modular architecture** where each file has a single responsibility:

```
012_project_manager_assistant/
│
├── config.py              # LLM instantiation & environment setup
├── models.py              # Pydantic data models (Task, Team, Risk, etc.)
├── state.py               # AgentState TypedDict definition
├── nodes.py               # 6 LangGraph node functions (the "brain")
├── graph.py               # Graph construction, routing, compilation
├── visualization.py       # Plotly Gantt chart builder
├── main.py                # Entry point — orchestrates the full pipeline
│
├── project_description.txt  # Input: plain-text project brief
├── team.csv                 # Input: team roster with skill profiles
├── requirements.txt         # Python dependencies
├── explanation.md           # This documentation file
└── pm_assistant.ipynb       # Original notebook (preserved for reference)
```

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        INPUTS                                     │
│  ┌─────────────────────┐    ┌──────────────────────────────┐     │
│  │ project_description │    │         team.csv              │     │
│  │       .txt          │    │  Name, Profile Description    │     │
│  └────────┬────────────┘    └──────────────┬───────────────┘     │
│           │                                │                      │
│           └────────────┬───────────────────┘                      │
│                        ▼                                          │
│              ┌──────────────────┐                                 │
│              │    main.py       │    ← Entry Point                │
│              │  (Orchestrator)  │                                  │
│              └────────┬─────────┘                                 │
│                       ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                  LangGraph Workflow (graph.py)               │ │
│  │                                                              │ │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │ │
│  │  │    Task       │───▶│    Task       │───▶│    Task       │  │ │
│  │  │  Generation   │    │ Dependencies  │    │  Scheduler    │  │ │
│  │  │  (Node 1)     │    │  (Node 2)     │    │  (Node 3)     │  │ │
│  │  └──────────────┘    └──────────────┘    └──────┬───────┘  │ │
│  │                                                  │          │ │
│  │                                                  ▼          │ │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │ │
│  │  │   Insight     │◀──│    Risk       │◀──│    Task       │  │ │
│  │  │  Generator    │   │  Assessor     │    │  Allocator    │  │ │
│  │  │  (Node 6)     │   │  (Node 5)     │    │  (Node 4)     │  │ │
│  │  └──────┬───────┘    └──────┬───────┘    └──────────────┘  │ │
│  │         │                   │                               │ │
│  │         │    ┌──────────────┴──────────────┐                │ │
│  │         │    │      Conditional Router       │                │ │
│  │         │    │  (risk improved? max iter?)   │                │ │
│  │         │    └──────┬───────────┬───────────┘                │ │
│  │         │           │           │                            │ │
│  │         │     [iterate]    [terminate]                       │ │
│  │         │           │           │                            │ │
│  │         └───────────┘           ▼                            │ │
│  │                           ┌──────────┐                      │ │
│  │                           │   END     │                      │ │
│  │                           └──────────┘                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                       │                                           │
│                       ▼                                           │
│              ┌──────────────────┐                                 │
│              │ visualization.py │    ← Plotly Gantt Chart         │
│              └──────────────────┘                                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Complete Execution Workflow & File Flow

When you run `python3 main.py`, the following sequence of events occurs:

1. **Environment Setup** (`config.py`):
   - Loads `.env` file with API keys using `python-dotenv`
   - Instantiates the LLM (Groq's `qwen/qwen3-32b` by default)
   - Factory pattern supports swapping to Azure OpenAI or OpenAI

2. **Data Loading** (`main.py`):
   - Reads `project_description.txt` → plain string
   - Parses `team.csv` → `Team` Pydantic model (list of `TeamMember` objects)

3. **State Initialization** (`main.py`):
   - Creates the initial `AgentState` dictionary with:
     - `project_description`, `team` (from inputs)
     - `iteration_number=0`, `max_iteration=3`
     - Empty lists for iteration tracking: `schedule_iteration`, `task_allocations_iteration`, `risks_iteration`, `project_risk_score_iterations`

### Phase 1: Task Generation (Node 1)

**File:** `nodes.py` → `task_generation_node()`

**What happens:**
- The LLM receives the project description and is prompted to act as an **expert project manager**
- It extracts actionable, realistic tasks with estimated durations
- Any task estimated >5 days is automatically broken into independent sub-tasks
- Output is forced into a structured `TaskList` schema via `llm.with_structured_output(TaskList)`

**Technical detail:** Pydantic's `TaskList` model uses `uuid.UUID` with `default_factory=uuid.uuid4` to auto-generate unique task IDs, ensuring consistent cross-referencing across nodes.

### Phase 2: Dependency Mapping (Node 2)

**File:** `nodes.py` → `task_dependency_node()`

**What happens:**
- Takes the generated `TaskList` and identifies **blocking relationships**
- For each task, maps: "which tasks must finish before this can start?"
- Also maps the reverse: "which tasks are waiting on this one?"
- Output: `DependencyList` — a structured dependency graph

**Why this matters:** Dependencies are the foundation of realistic scheduling. Without them, the scheduler might parallelize tasks that actually require sequential execution.

### Phase 3: Task Scheduling (Node 3)

**File:** `nodes.py` → `task_scheduler_node()`

**What happens:**
- Receives tasks, dependencies, and any previous iteration insights
- Assigns `start_day` and `end_day` to each task
- Parallelizes independent tasks to minimize total project duration
- Respects all dependency constraints
- On subsequent iterations, tries to **not increase** project duration vs. previous schedules

**State mutation:** Appends the new schedule to `schedule_iteration` list for historical tracking.

### Phase 4: Task Allocation (Node 4)

**File:** `nodes.py` → `task_allocation_node()`

**What happens:**
- Matches each task to the **best-fit team member** based on:
  - Skills and expertise (e.g., frontend tasks → Alice/Frank, backend → Bob)
  - Current availability (no overlapping assignments)
  - Workload balance (prevent burnout)
- Uses previous iteration insights to improve assignments

**Constraints enforced:**
- Each team member handles only one task at a time
- Assignments respect seniority and specialization

### Phase 5: Risk Assessment (Node 5)

**File:** `nodes.py` → `risk_assessment_node()`

**What happens:**
- Analyzes each task-allocation-schedule triplet for risk factors:
  - **Task complexity** vs. assigned member's experience
  - **Buffer time** between consecutive tasks for the same person
  - **Dependency chains** — long chains amplify risk
  - **Seniority matching** — senior members get lower risk scores
- Assigns a risk score (0-10) per task
- Computes **aggregate project risk score** = sum of all task scores
- Increments `iteration_number`

**Key behavior:** If a task assignment is unchanged from a previous iteration, the risk score is retained for consistency.

### Phase 6: Conditional Routing (Router)

**File:** `graph.py` → `router()`

**Decision logic:**
```
IF iteration_number < max_iteration:
    IF ≥2 iterations completed AND latest_risk < first_risk:
        → END (plan has improved — stop optimizing)
    ELSE:
        → insight_generator (try to improve further)
ELSE:
    → END (max iterations reached — use best available plan)
```

This creates a **self-improving feedback loop** that stops when:
1. The plan's risk has measurably decreased, OR
2. The maximum iteration budget (default: 3) is exhausted

### Phase 7: Insight Generation (Node 6)

**File:** `nodes.py` → `insight_generation_node()`

**What happens:**
- Analyzes the current schedule + allocations + risk scores
- Generates **actionable improvement recommendations**:
  - Identifies bottlenecks and resource conflicts
  - Suggests task reassignments to reduce risk
  - Proposes schedule adjustments for better parallelization
- Returns free-text insights (not structured output — creative analysis)

**Feedback loop:** These insights flow back into Node 3 (Task Scheduler) and Node 4 (Task Allocator), informing the next iteration's decisions.

### Phase 8: Visualization

**File:** `visualization.py` → `build_gantt_chart()`

**What happens:**
- Extracts the final schedule and allocation from `AgentState`
- Merges them into a Pandas DataFrame
- Converts day-offset values to actual calendar dates
- Generates an interactive **Plotly Gantt chart** with:
  - Tasks on the Y-axis
  - Timeline on the X-axis
  - Color-coded by team member assignment

---

## 🛠️ Tool Calling & Structured Output

To force the Large Language Model to behave deterministically and output structured data instead of conversational text, this project uses **LangChain's Structured Output functionality**, acting as a pseudo-tool call.

1. **Pydantic Schemas (`models.py`)**: Every step has a strict Pydantic model (e.g., `TaskList`, `Schedule`, `TaskAllocation`). These define the exact keys and data types expected.
2. **JSON Mode (`nodes.py`)**: We use `llm.with_structured_output(Schema, method="json_mode")`.
3. **Explicit Prompting**: Open-source models on free tiers (like Llama 4 Scout) can sometimes fail to map internal schema definitions perfectly. To ensure robust "tool calling" execution without native function calling features, we inject explicit JSON structural examples directly into the prompt (escaped properly with `{{` and `}}` in Python f-strings).
4. **Retry Mechanism**: A custom `retry_invoke` function wraps the structured output calls. If the LLM generates invalid JSON or hallucinates keys, or if the API hits a rate limit, the wrapper catches the exception and handles backoff/retries automatically.

---

## 🔮 Future Enhancements (Real-World Production)

### 1. 🌐 Web Application Interface
Build a **Streamlit or FastAPI** frontend where users can:
- Upload project descriptions and team CSVs via drag-and-drop
- Watch the agent's progress in real-time with streaming output
- Interactively adjust the generated plan (drag tasks, reassign members)
- Export plans to **Jira, Asana, Monday.com, or MS Project**

### 2. 🧠 Multi-Agent Architecture
Replace the single-LLM approach with **specialized agents**:
- **Requirements Analyst Agent** — extracts requirements from unstructured docs
- **Scheduling Agent** — uses constraint programming (OR-Tools) for mathematically optimal schedules
- **Risk Agent** — trained on historical project failure data
- **Communication Agent** — generates stakeholder-ready reports and emails

### 3. 📊 Historical Learning & Analytics
- Store completed project plans and their actual outcomes in a database
- Train the agent on **real project velocity data** to improve estimation accuracy
- Build a **project analytics dashboard** showing estimation accuracy trends, common risk patterns, and team utilization rates

### 4. 🔗 Tool Integrations
- **Jira/Linear API integration** — auto-create tickets from the generated task list
- **Slack/Teams notifications** — send plan summaries and daily standup prompts
- **Calendar integration** — block team members' calendars based on allocations
- **Git integration** — map tasks to branches and track progress via PR/commit activity

### 5. 🎯 Advanced Risk Modeling
- Incorporate **Monte Carlo simulation** for probabilistic schedule forecasting
- Use **historical bug rates** per team member to adjust risk scores
- Factor in **leave/vacation calendars** and public holidays
- Model **scope creep probability** based on requirement ambiguity scores

### 6. 📋 Sprint-Level Planning
- Break the project plan into **sprints/iterations**
- Generate sprint backlogs with story points
- Produce **burndown chart predictions**
- Support **re-planning** when actuals deviate from estimates

### 7. 🔒 Enterprise Features
- **Role-based access control** (PM vs. Developer vs. Stakeholder views)
- **Audit trail** — log every LLM decision with reasoning for compliance
- **Cost estimation** — compute project cost based on team salaries and timeline
- **Multi-project portfolio management** — optimize resource allocation across projects

---

## 📝 Resume Summary

> **Copy-paste ready bullet points for your resume/portfolio:**

### Project Title
**AI-Powered Project Manager Assistant — Autonomous Planning Agent**

### Summary
Designed and built an **autonomous AI project planning agent** using **LangChain, LangGraph, and Groq LLMs** that takes a plain-text project description and team roster as inputs and generates a complete, optimized project plan with task decomposition, dependency mapping, resource allocation, risk assessment, and iterative self-improvement — reducing planning time from days to minutes.

### Key Bullet Points

- **Architected a 6-node LangGraph workflow** implementing a complete project management pipeline: task extraction → dependency analysis → scheduling → allocation → risk assessment → insight-driven optimization loop
- **Engineered LLM-powered structured output** using Pydantic schemas with LangChain's `with_structured_output()`, ensuring type-safe, deterministic outputs from the Groq qwen/qwen3-32b model
- **Implemented a self-improving feedback loop** with conditional routing — the agent iteratively optimizes its plan across 3 iterations, stopping early when the aggregate risk score decreases
- **Built a modular, production-ready architecture** with separated concerns: `config.py` (LLM factory), `models.py` (13 Pydantic schemas), `state.py` (shared state), `nodes.py` (6 prompt-engineered nodes), `graph.py` (DAG construction), `visualization.py` (Plotly Gantt charts)
- **Designed risk-aware resource allocation** that considers team member seniority, skill-task matching, workload balancing, and inter-task buffer times to minimize project failure probability
- **Generated interactive Plotly Gantt charts** from the optimized plan, with team-member color coding and calendar-date conversion for stakeholder presentation

### Technologies
`Python` · `LangChain` · `LangGraph` · `Groq API` · `Pydantic` · `Plotly` · `Pandas` · `Prompt Engineering` · `Structured Output` · `Stateful Agents` · `Directed Graph Workflows`

---

## 🚀 How to Run

```bash
# 1. Navigate to the project directory
cd 012_project_manager_assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with your API key
echo "GROK_API_KEY=your_groq_api_key_here" > .env

# 4. Run the assistant
python main.py
```

### Inputs
- **`project_description.txt`** — A plain-text description of your project
- **`team.csv`** — CSV with columns: `Name`, `Profile Description`

### Outputs
- Console output showing node-by-node progress
- Interactive **Plotly Gantt chart** visualization
- Complete project plan in the agent's state (tasks, schedule, allocations, risks)

---

*Built with ❤️ using LangChain + LangGraph + Groq*

---

## 💡 Key Learnings & Troubleshooting

Throughout the development and refinement of this Project Manager Assistant, we encountered and resolved several critical challenges. These learnings are essential for anyone building production-grade LLM applications on free-tier APIs:

### 1. Handling API Rate Limits Gracefully
- **Challenge:** The free-tier Groq API enforces strict Tokens-Per-Minute (TPM) and Tokens-Per-Day (TPD) limits. Models like `llama-3.3-70b-versatile` hit the rate limit instantly during the multi-node workflow due to the high context window usage in iterative planning.
- **Solution:** Switched to the `meta-llama/llama-4-scout-17b-16e-instruct` model, which offers a generous 500K TPD and 30K TPM limit. Furthermore, we implemented a custom `retry_invoke()` wrapper in `nodes.py` that catches `429 RateLimitError` exceptions, parses the "try again in X seconds" message, and dynamically sleeps before retrying. 

### 2. Pydantic Schema Validation & LLM Hallucinations
- **Challenge:** LangChain's `with_structured_output` maps LLM output to Pydantic models. However, open-source models occasionally modify keys slightly (e.g., outputting the plural `"estimated_days"` instead of the singular `"estimated_day"`), leading to `OutputParserException` failures.
- **Solution:** 
  - **Schema Alignment:** We renamed fields in `models.py` (e.g., `estimated_day` -> `estimated_days`) to align with the natural grammatical inclinations of the LLM.
  - **Explicit Structuring:** Relying purely on implicit schema passing is not enough for smaller models. We embedded strict JSON templates directly into the prompt instructions to force exact structural compliance.

### 3. Escaping Brackets in Python f-strings
- **Challenge:** When injecting explicit JSON examples into prompt templates formatted as Python f-strings (e.g., `f"""..."""`), the curly braces `{}` used for JSON objects were interpreted as variable injection placeholders by Python, causing `ValueError: Invalid format specifier`.
- **Solution:** We doubled all literal curly braces to `{{` and `}}` within the f-string prompts. This ensures Python treats them as string literals while allowing normal `{variable}` injection elsewhere in the prompt.

### 4. Bypassing Optional Tracing Overheads
- **Challenge:** The pipeline initially threw `403 Forbidden` errors related to the LangSmith API.
- **Solution:** Because we were running the pipeline locally without an active LangSmith API key or project set up, we explicitly disabled tracing in `config.py` (`os.environ["LANGCHAIN_TRACING_V2"] = "false"`), preventing unnecessary network crashes.

### 5. Managing Iteration Complexity
- **Challenge:** Running too many workflow iterations (e.g., `max_iteration=3`) multiplied token usage drastically, causing both slow execution and API throttling.
- **Solution:** Lowered the default `max_iteration` to 2. This proved sufficient for the agent to generate an initial plan and perform one solid pass of insight-driven optimization without exhausting API limits.
