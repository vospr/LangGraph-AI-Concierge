C
---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-02-25'
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
workflowType: 'architecture'
project_name: 'TNL-HELP'
user_name: 'Andrey'
date: '2026-02-25'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

---

## Starter Template Evaluation

### Primary Technology Domain

Python 3.11+ CLI application with LangGraph orchestration — no web server, no UI, no API deployment layer. Standard starter template landscape (Next.js, Vite, T3, etc.) does not apply.

### Starter Options Considered

**Option A: `langgraph-cli` official template**

`langgraph new --template new-langgraph-project-python ./tnl-help` — scaffolds LangGraph Server with API endpoints, threads, assistants, and `langgraph dev` deployment. Server-oriented. Pulls in `langgraph-api` dependencies unnecessary for this project. **Not the right fit.**

**Option B: Community FastAPI + LangGraph template**

`wassim249/fastapi-langgraph-agent-production-ready-template` — production-ready FastAPI + LangGraph pairing. Also API-server-oriented. **Not the right fit.**

**Option C: Custom structure from spec (Selected)**

The PRD defines the project structure explicitly. `spec/concierge-spec.md` written on Day 1 IS the starter — it defines directory layout, state schema, agent contracts, and edge conditions before any code exists. No existing starter matches this project's profile (Python CLI, multi-agent, Anthropic-only, demo-first, portfolio-argument structure).

### Selected Approach: Custom Structure from Spec

**Rationale:** Using a generic starter would introduce unnecessary files that a hiring manager must mentally subtract. The project structure is part of the architectural argument — every directory answers one question about the system.

**Initialization sequence:**

```bash
mkdir tnl-help && cd tnl-help
git init
# Commit .gitignore FIRST — before any main.py run
# Then write spec/concierge-spec.md (git timestamp proves spec-first)
git add .gitignore && git commit -m "chore: gitignore before any runtime files"
git add spec/concierge-spec.md && git commit -m "spec: concierge spec before implementation"
# Then scaffold remaining structure
```

**LangGraph Version Decision: `langgraph==1.0.x` (exact pin)**

LangGraph 1.0 (stable) shipped October 2025. Pinning to 0.2.x in February 2026 signals a developer who didn't track the framework's stable release. Core graph API patterns (`StateGraph`, `add_node`, `add_edge`, conditional edges, `TypedDict` state, `graph.invoke`) are preserved in 1.0. Breaking changes were concentrated in LangGraph Server/Platform APIs — which this project does not use. `validate_config.py` asserts `langgraph.__version__` starts with `"1."`. README states: "Built and tested with LangGraph 1.0.x."

### Defined Project Structure

```
tnl-help/
├── spec/
│   └── concierge-spec.md              # Day 1 — before any .py file. Version header + [TBD] markers.
├── docs/
│   └── adr/
│       ├── 001-context-window-ownership.md     # ≤20 lines each
│       ├── 002-multi-model-strategy.md
│       ├── 003-anthropic-only-mvp.md
│       ├── 004-file-based-memory.md
│       └── 005-langgraph-framework-selection.md
├── config/
│   └── routing_rules.yaml             # Stage 1 pre-filter rules + escalation_threshold only
├── prompts/
│   ├── dispatcher/
│   │   ├── policy.yaml                # AgentPolicy: model, prompt_version, max_tokens, confidence_threshold
│   │   └── v1.yaml                    # role, context, constraints, output_format, examples
│   ├── rag_agent/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── research_agent/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── response_synthesis/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── guardrail/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   └── followup/
│       ├── policy.yaml
│       └── v1.yaml
├── agents/                            # Agent logic — stateful, policy-aware, all reasoning here
│   ├── dispatcher.py
│   ├── rag_agent.py
│   ├── research_agent.py
│   ├── response_synthesis.py
│   ├── guardrail.py
│   ├── followup.py
│   └── booking_agent.py               # Stub — returns BookingAgentResponse Pydantic model
├── nodes/                             # LangGraph node functions — one-liner delegates ONLY
│   ├── dispatcher_node.py             # def dispatcher_node(state) -> ConciergeState: return dispatcher.run(state)
│   ├── rag_node.py
│   ├── research_node.py
│   ├── synthesis_node.py
│   ├── guardrail_node.py
│   ├── followup_node.py
│   └── booking_node.py
├── graph/
│   └── __init__.py                    # Builds + exports compiled_graph. from graph import compiled_graph.
├── memory/
│   ├── profiles/
│   │   └── alex.json                  # Version-controlled design artifact — full UserProfile schema
│   ├── sessions/                      # Runtime-generated — in .gitignore
│   │   └── .gitkeep
│   └── README.md                      # 3–5 lines on memory model
├── tests/
│   └── test_state_reset.py            # NFR10 minimum: stale-state unit test
├── main.py
├── validate_config.py
├── requirements.txt                   # All deps exact-pinned (==)
├── .env.example
├── .gitignore                         # Committed Day 1, before first main.py run
└── README.md                          # Mermaid graph + JD table on first screen + "Navigating This Repo"
```

### Architectural Decisions This Structure Makes

| Concern | Decision | Rationale |
|---------|---------|-----------|
| Language & Runtime | Python 3.11+, synchronous | No async needed for CLI; simpler stack trace on errors |
| Dependency management | `pip` + `requirements.txt`, exact pins (`==`) | Zero setup friction; demo reproducibility |
| LangGraph version | `langgraph==1.0.x` | Current stable release; core API preserved from 0.2.x |
| Agent/node split | `agents/` = logic; `nodes/` = graph interface only | Clean LangGraph seam; nodes are one-liner delegates |
| Config separation | `config/` = system behavior; `prompts/` = LLM config | Different change rates; different readers |
| ADR format | `docs/adr/` lightweight (≤20 lines each) | Industry-standard signal; minimal overhead |
| Graph assembly | `graph/__init__.py` exports `compiled_graph` | Clean import: `from graph import compiled_graph` |
| Test visibility | `tests/` top-level, explicit | No `utils/` or `helpers/` catch-alls permitted |
| Build step | None — `python main.py` is the pipeline | Zero friction for hiring manager |

### Structural Constraints

- **`nodes/*.py`** must open with a module docstring explaining the agent/node seam — not optional
- **`prompts/*/v1.yaml`** must follow 5-section schema: `role`, `context`, `constraints`, `output_format`, `examples` — trivial prompts are a signal failure
- **`config/`** is reserved for system-behavior config only — must not grow beyond 2–3 files for MVP
- **`.gitignore`** committed Day 1 before any `main.py` execution — `memory/sessions/` must never appear in git history
- **`spec/concierge-spec.md`** must include version header (`v1.0 | 2026-02-25 | Written before implementation`), 2–3 `[TBD]` markers on genuinely uncertain items, and at least one "alternatives considered" note per major decision
- **README** must include "Navigating This Repo" section with 5-step ordered reading path immediately after the Mermaid graph

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements (55 total across 8 categories):**

- **Intent Routing & Dispatch (9 FRs):** Hybrid dispatcher with rule-based pre-filter + LLM escalation, confidence scoring on every routing decision, sub-agent field reset protocol per turn, `--fast-mode` CLI override, Dispatcher as sole context owner
- **Knowledge Retrieval (8 FRs):** JSON mock KB with production swap-point comments, DuckDuckGo web search with graceful degradation, blended response with inline source attribution (RAG vs. web labeled)
- **Memory & Personalization (6 FRs):** File-based JSON profile + session R/W, proactive greeting before first user input, pre-seeded `alex` profile, fresh-session fallback without crash
- **Governance & Safety (7 FRs):** Guardrail node with confidence threshold, one-clarifying-question rule, max-clarification-before-handoff, BookingAgent stub with integration contract, out-of-domain deflection
- **Observability & Tracing (6 FRs):** Structured CLI trace on every node transition, consistent bracket-label convention `[NODE_NAME] key=value → outcome`, model name in trace output, Dispatcher routing decisions as structured parseable format
- **Configuration & Extensibility (8 FRs):** Per-agent model + prompt-version in YAML policy files, per-agent `max_tokens` enforcement, new agent via new graph node only (no Dispatcher rewrite), prompt versioning by YAML increment, `validate_config.py` pre-run check, token budget detection + summarization
- **Session & State Management (6 FRs):** `ConciergeState` TypedDict covers all handoffs, per-turn freshness guarantee, full history persisted to disk independent of context window, dual-store (in-session state + persisted file)
- **Demo Integrity & Developer Experience (5 FRs):** Single-command startup with one env var, visible reduced-capability banner, pre-validated demo script, profile reset command, actionable LLM error messages (no raw stack traces)

**Non-Functional Requirements (17 total):**

- **Performance:** Cold start < 10s; full 5-turn demo < 5 min; dispatch overhead < 2s/turn; fast-mode cold start < 5s
- **Security:** API keys from env/.env only — never in config, session, or trace files; `.env` gitignored with `.env.example` documented
- **Reliability:** No unhandled exceptions on optional component failure; retry-once on Anthropic API failure with actionable error; zero stale sub-agent data across turns (unit test validated)
- **Developer Experience:** Clone-to-running < 5 min; `validate_config.py` catches all errors before LLM call; consistent policy YAML schema (copy-paste to create new agent)
- **Documentation:** README Mermaid topology diagram; JD mapping table; ADR-001 + ADR-002 documented; `spec/concierge-spec.md` authored before implementation

**Scale & Complexity:**

- Primary domain: AI backend / agent orchestration (LangGraph), CLI demo interface
- Complexity level: Medium — novel AI technology stack; no regulatory or compliance overhead
- Estimated architectural components: 7 graph nodes (Dispatcher, RAG Agent, Research Agent, Response Synthesis, Guardrail, Follow-Up, BookingAgent stub), 2 services (Memory, TokenBudgetManager), 1 CLI adapter, 1 pre-run validator

### Technical Constraints & Dependencies

- **Runtime:** Python 3.11+, LangGraph ≥0.2, Anthropic SDK ≥0.40, Pydantic ≥2.0, duckduckgo-search ≥6.0
- **Dependency pinning:** All dependencies must be pinned to exact versions (`==`) in `requirements.txt` — not minimum versions (`>=`). Demo reliability requires reproducible installs.
- **LLM provider:** Anthropic only (MVP) — one required credential (`ANTHROPIC_API_KEY`)
- **Infrastructure:** Zero — no cloud, no vector DB, no LangSmith, no UI; runs fully local
- **Build constraint:** 1 developer, 5 days; scope locked in Day 1 spec
- **Anthropic-only for MVP:** Provider abstraction deferred post-MVP (ADR-003)

**Critical Configuration Constraints:**

- **Dispatcher 128-token output cap is load-bearing** — if misconfigured, Dispatcher generates prose instead of routing JSON, breaking the graph silently. `validate_config.py` must assert this cap explicitly.
- **Model name validation required** — `validate_config.py` must validate declared model names against an allow-list, not just check API key presence. A YAML typo silences until the first user turn.
- **Threshold naming distinction** — `escalation_threshold` (Stage 1→2 boundary in `routing_rules.yaml`) is distinct from `confidence_threshold` (Stage 2→Guardrail boundary in `AgentPolicy`). These must never be confused. `validate_config.py` must assert: `guardrail.confidence_threshold < dispatcher.confidence_threshold` (strict less-than).
- **Python version assertion at startup** — `sys.version_info >= (3, 11)` must be checked in `main.py` before any imports, with a human-readable error message.
- **API key active probe** — `validate_config.py` must make one lightweight API probe call (e.g., `anthropic.models.list()`) to verify the key is active, not just present. Catches expired keys before the demo.

### Dispatcher Hybrid Routing Architecture

The pre-filter and LLM escalation are two distinct stages with two distinct configuration files:

```
config/
  routing_rules.yaml        ← Stage 1 rules + escalation_threshold (loaded once at startup)
prompts/
  dispatcher/
    policy.yaml             ← LLM model, prompt_version, max_tokens, confidence_threshold
    v1.yaml                 ← Dispatcher prompt
```

- **Stage 1:** Load `routing_rules.yaml` → keyword match → if `confidence ≥ escalation_threshold`: route directly
- **Stage 2:** LLM classification → structured output → if `confidence ≥ confidence_threshold`: route; else → Guardrail
- Pre-filter rules are a hardcoded enumeration in `routing_rules.yaml` for MVP. Extension path = add YAML entries, not code changes (FR36).
- Demo script pre-validation for Stage 1 requires no LLM call — load `routing_rules.yaml`, assert keyword match + confidence score for each demo query.
- `routing_rules.yaml` must be self-documenting with inline comments explaining each rule.

### Cross-Cutting Concerns Identified

1. **Observability/tracing** — every graph node must emit structured CLI trace output via a centralized `trace(node_name, **fields)` function. This function maintains an explicit **allowlist** of emittable fields (`intent`, `confidence`, `route`, `model`, `session_id`) and a **denylist** of fields that must never be emitted (`current_input`, `memory_profile`, `conversation_history`, `rag_results`, `research_results`). No ad-hoc f-strings in nodes.
2. **State reset protocol** — Dispatcher must reset all sub-agent fields via `reset_turn_state(state)` helper — a single function listing all fields to reset. `validate_config.py` performs a static check asserting all optional `ConciergeState` fields appear in this helper.
3. **Graceful degradation** — every optional component (DuckDuckGo, memory profile, session file) must fail cleanly without exception; affects every agent's error boundary. Defensive access pattern for optional TypedDict fields: `(state.get("field") or [])` — never direct list operations on `None`.
4. **Demo experience at three engagement layers** — architecture must be legible at: Layer 1 (30s README scan), Layer 2 (3min source reading), Layer 3 (10min demo execution). Current architecture is designed primarily for Layer 3. Layers 1 and 2 require self-documenting source artifacts.
5. **API key safety** — `ANTHROPIC_API_KEY` must never appear in any file written during runtime. Centralized trace formatter enforces this via denylist.
6. **Configuration-driven behavior** — all per-agent settings declared in YAML; no model names or token limits hardcoded; affects AgentPolicy loading and `--fast-mode` override logic. `--fast-mode` degrades LLM-escalation routing quality (Haiku replaces Opus on Dispatcher) — acceptable for dev, not the demo path. README must make this distinction explicit.
7. **Spec-first discipline** — `spec/concierge-spec.md` must be committed before any `.py` file in `agents/`, `nodes/`, or `graph/`. Git timestamp is the enforcement mechanism. The spec must open with a datestamp and role declaration. README must link it with explicit framing.

### Architectural Gaps & Known Limitations

| # | Item | Category | Severity |
|---|------|----------|----------|
| G1 | `TokenBudgetManager` is a stub in MVP. The turn count that triggers summarization is undefined. Stub comment must declare the activation threshold explicitly, or it must be defined before implementation. | Deferred Risk | High |
| G2 | Dispatcher 128-token output cap is a critical configuration constraint. Misconfiguration silently breaks graph routing. `validate_config.py` must assert this. | Configuration | High |
| G3 | SIGINT/crash during session leaves `memory/sessions/` in inconsistent state. A `signal.signal(SIGINT, handler)` flush is a demo-stability improvement not currently in FRs. | Demo Stability | Medium |
| G4 | Session files in `memory/sessions/` grow unbounded across runs — no TTL or cleanup mechanism. Known limitation for MVP; documented so future contributors don't mistake it for a bug. | Known Limitation | Low |
| G5 | `memory/profiles/alex.json` is a version-controlled test fixture and design artifact. Reset path = `git checkout -- memory/profiles/alex.json`. Must demonstrate the full `UserProfile` schema, not just the minimum needed to fire the greeting. Companion `memory/README.md` (3–5 lines) makes the memory model explicit for Layer 2 readers. | Demo Integrity | Medium |
| G6 | Opus cold-start on first routing call is the demo latency risk point. `--fast-mode` is the documented mitigation. README should give hiring managers explicit permission to use `--fast-mode` without framing it as a degraded demo. | Demo Experience | Medium |
| G7 | `validate_config.py` must validate model names against an allow-list and make one lightweight API probe call to verify the key is active. | Configuration | High |
| G8 | `--fast-mode` degrades LLM-escalation routing quality. Acceptable for development; not the demo path. README must make this distinction explicit. | Known Limitation | Medium |
| G9 | `escalation_threshold` and `confidence_threshold` are two distinct thresholds serving two distinct purposes. `validate_config.py` must assert `guardrail.confidence_threshold < dispatcher.confidence_threshold`. | Architecture | High |
| G10 | Demo script queries must be pre-validated against actual Stage 1 confidence scores to ensure routing reproducibility. Boundary queries produce non-deterministic LLM routing. Stage 1 pre-validation requires no LLM call — testable from `routing_rules.yaml` alone. | Demo Integrity | High |
| PM1 | All deps must be pinned to exact versions (`==`). `validate_config.py` must catch `AuthenticationError` with a human-readable message. Python 3.11+ must be asserted at startup. | Environment | High |
| PM2 | Memory Service paths must be resolved relative to `Path(__file__).parent`, not CWD. Silent profile miss must emit a visible warning, not fail silently. | Architecture | High |
| PM3 | Demo script must document expected routing path (not just expected response) for each query and be tested against real confidence scores before Day 5. | Demo Integrity | High |
| PM4 | `spec/concierge-spec.md` committed before implementation code. `docs/adr/` directory for ADRs. README leads with Mermaid graph + JD mapping table on first screen-height. | Documentation | High |
| PM5 | Defensive access pattern `(state.get("x") or [])` for all optional TypedDict fields. Unit test covers `None` initial state on all optional fields. | Reliability | High |
| RT1 | `reset_turn_state(state)` helper centralizes the reset block. `validate_config.py` static check asserts all optional `ConciergeState` fields appear in this helper. | Architecture | Medium |
| RT2 | Centralized `trace()` function with field allowlist/denylist. No ad-hoc trace f-strings in node implementations. | Observability | Medium |
| RT3 | One API probe call in `validate_config.py` verifies key is active before demo. | Configuration | High |
| RT4 | `BookingAgentResponse` Pydantic model (`status`, `message`, `integration_point`, `required_env_vars`) is the integration contract. Stub returns this model, not a bare string. | Architecture | Medium |
| RT5 | `spec/concierge-spec.md` committed before any implementation `.py` file. Git history is the enforcement mechanism. | Process | Medium |
| FP1 | ADR-005 must exist: LangGraph chosen for typed state + conditional edges + streaming support + direct role signal alignment. Both the technical and rhetorical justifications must be explicit. README JD mapping table maps LangGraph usage to a specific job description requirement. | Documentation | Medium |
| FP2 | Architecture must work at three engagement layers: Layer 1 (30s README), Layer 2 (3min source reading), Layer 3 (10min demo execution). Design decisions must be legible without running the code. | Architecture | High |
| FP3 | All source artifacts self-documenting for Layer 2: `routing_rules.yaml` has inline comments, `alex.json` has `_demo_notes` field, every production swap-point comment is a readable design statement. | Documentation | Medium |
| FP4 | Follow-Up Node must be justified as a demonstration of conditional graph edges (a LangGraph capability distinguishing it from linear chains) — or cut and the cut documented. Not justified as a feature alone. | Architecture | Medium |
| FP5 | `alex.json` demonstrates full `UserProfile` schema. `memory/README.md` explains the memory model in 3–5 lines. | Demo Integrity | Medium |
| FP6 | `spec/concierge-spec.md` opens with: datestamp + "written before implementation" declaration. README links it with explicit framing as the authoritative source of agent contracts. | Documentation | Medium |

---

## Core Architectural Decisions

### Already Decided (PRD + Steps 1–3)

- **Orchestration:** LangGraph 1.0.x — `StateGraph`, typed state, conditional edges
- **Language:** Python 3.11+, synchronous, no async
- **LLM provider:** Anthropic SDK only — `claude-opus-4-6` (Dispatcher), `claude-sonnet-4-6` (Research, Synthesis), `claude-haiku-4-5` (RAG, Guardrail, Follow-Up)
- **State schema:** `ConciergeState` TypedDict — defined in `spec/concierge-spec.md`
- **Agent config:** `AgentPolicy` Pydantic model per agent, loaded from `prompts/*/policy.yaml`
- **Routing:** Hybrid — `config/routing_rules.yaml` (Stage 1) + LLM classification (Stage 2)
- **Persistence:** File-based JSON — `memory/profiles/` and `memory/sessions/` — no database
- **Interface:** CLI only — `python main.py --user alex` — no web server, no deployment

### Decision 1: Error Handling Propagation

**Decision:** Catch at node boundary — not at `main.py`.

Each node function wraps its agent call in `try/except`. On failure: sets `state["error"]` to an actionable message, sets `state["human_handoff"] = True`, returns modified state. The graph routes to a terminal response node that reads the error state and emits a user-facing message. No exception escapes the graph boundary. CLI trace entry always prints (node catch ensures the `[NODE_NAME]` trace fires before the error path).

**`ConciergeState` addition:** `error: str | None` — reset to `None` by `reset_turn_state()` at turn start.

**Rationale:** FR57 (actionable errors, no stack traces) + complete CLI trace on every run. A single `main.py` catch-all breaks both requirements.

### Decision 2: Testing Strategy

**Decision:** Two-tier testing — pure unit tests + mocked integration tests. No real API calls in `pytest`.

- **Tier 1 — Pure unit tests** (`tests/test_state_reset.py` and similar): Test `reset_turn_state()`, `routing_rules.yaml` keyword matching, `AgentPolicy` loading, memory path resolution. No LLM, no mocking, pure Python.
- **Tier 2 — Mocked integration tests:** Patch `anthropic.Anthropic` via `unittest.mock.patch`. Test full dispatcher routing paths with deterministic LLM responses. One test per happy-path route minimum.

**`requirements.txt` additions:** `pytest==x.x.x` (exact pin).
**`tests/conftest.py`:** Shared mock Anthropic client fixture.

**Rationale:** NFR10 stale-state test must be pure (no LLM dependency). Integration tests verify routing contracts without incurring API costs or non-determinism.

### Decision 3: `validate_config.py` Execution Model

**Decision:** Importable module — `main.py` calls `validate_config.run_checks()` at startup.

`main.py` calls `run_checks()` before `from graph import compiled_graph`. Validation failure triggers `sys.exit(1)` with an actionable message listing every failed check. `python validate_config.py` also works standalone for explicit pre-flight use.

**Checks performed (in order):**
1. Python version ≥ 3.11
2. `ANTHROPIC_API_KEY` present in environment
3. Anthropic API reachable (lightweight probe call)
4. All `prompts/*/policy.yaml` files parse as valid `AgentPolicy`
5. All declared model names in allow-list
6. Dispatcher `max_tokens` == 128 (exact assertion)
7. `guardrail.confidence_threshold < dispatcher.confidence_threshold`
8. `config/routing_rules.yaml` parses and contains required fields
9. `langgraph.__version__` starts with `"1."`
10. `memory/profiles/alex.json` exists and parses as valid `UserProfile`

**Rationale:** Single entry point, no separate command in README quickstart, all checks run before first LLM call, ordered from cheapest to most expensive.

### Decision 4: `--fast-mode` Implementation

**Decision:** Environment variable — `os.environ["FAST_MODE"] = "1"` set by `main.py` on flag detection.

`AgentPolicy.model` is a `@property` that checks `os.environ.get("FAST_MODE")` before returning the configured model name. When set, returns `"claude-haiku-4-5"` regardless of `policy.yaml` value. `main.py` prints the session banner once: `[FAST MODE] Using claude-haiku-4-5 across all agents — not the demo path` before graph invocation.

**Rationale:** Visible in process environment, debuggable without reading source, no object threading through call stack. `validate_config.py` can detect fast-mode and skip the Opus model allow-list check.

### Deferred Decisions (Post-MVP)

| Decision | Deferred Reason |
|---------|----------------|
| Provider abstraction (multi-provider) | ADR-003: Anthropic-only for MVP |
| `TokenBudgetManager` activation threshold | G1: undefined turn count — stub with comment |
| `AgentPolicy.allowed_tools` runtime enforcement | Declarative only in MVP |
| SIGINT memory flush handler | G3: nice-to-have demo stability |
| Session file TTL/cleanup | G4: known limitation, not a bug |

### Decision Impact Analysis

**Implementation Sequence (dependencies govern order):**
1. `spec/concierge-spec.md` — defines `ConciergeState` (including `error` field) + `AgentPolicy`
2. `.gitignore` + `requirements.txt` — before any runtime files
3. `validate_config.py` — before `main.py` (called from `main.py` at startup)
4. `config/routing_rules.yaml` + `prompts/*/policy.yaml` — before any agent implementation
5. `agents/` classes — before `nodes/` wrappers
6. `graph/__init__.py` — after all nodes exist
7. `main.py` — after graph is compiled
8. `tests/` — alongside agents (not after)

**Cross-Component Dependencies:**
- `reset_turn_state()` in `agents/dispatcher.py` must include `error: None` — added in Decision 1
- `validate_config.py` `run_checks()` called before `from graph import compiled_graph` — `graph/__init__.py` must be importable without side effects
- `AgentPolicy.model` property reads `os.environ["FAST_MODE"]` — env var set by `main.py` before any `AgentPolicy` instantiation
- `trace()` denylist (RT2) must include `error` field — actionable error messages are internal state, not trace output

---

## Implementation Patterns & Consistency Rules

### Tooling & Environment

**Package manager:** `uv` — mandatory.
```bash
uv venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate          # Windows
uv add langgraph anthropic pydantic duckduckgo-search python-dotenv
uv add --dev pytest pytest-asyncio ruff mypy pre-commit
```

`pyproject.toml` is the single source of truth. `uv.lock` is committed — it is the true exact-pin mechanism (exact hashes, not ranges). `requirements.txt` is generated from `pyproject.toml` for hiring manager pip convenience:
```bash
uv export --format requirements-txt > requirements.txt
```
`requirements.txt` is regenerated in the pre-commit hook — always in sync. README explains both paths: `uv sync` (recommended) and `pip install -r requirements.txt` (fallback).

**Before every commit:**
```bash
ruff format . && ruff check . --fix && mypy src/ && pytest tests/ -v
```

**`pyproject.toml` tool config:**
```toml
[tool.mypy]
python_version = "3.11"   # required for str | None union syntax
strict = true
ignore_missing_imports = true

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers --asyncio-mode=auto"
```

**mcpdoc MCP server — add to `.claude/mcp.json`:**
```json
{
  "mcpServers": {
    "langgraph-docs-mcp": {
      "command": "uvx",
      "args": [
        "--from", "mcpdoc", "mcpdoc",
        "--urls",
        "LangGraph:https://langchain-ai.github.io/langgraph/llms.txt LangChain:https://python.langchain.com/llms.txt",
        "--transport", "stdio"
      ]
    }
  }
}
```
**Rule:** For ANY LangGraph or LangChain API question, call `fetch_docs` before generating code. Also fetch: `https://langchain-ai.github.io/langgraph/concepts/multi_agent/` (multi-agent patterns) and `https://langchain-ai.github.io/langgraph/how-tos/state-reducers/` (state reducers — critical for `add_messages`).

---

### CLAUDE.md Setup

```
project root/
├── CLAUDE.md                    ← Python.md content (base Python conventions)
│                                   Last line: @docs/CLAUDE_langgraph.md
└── docs/
    └── CLAUDE_langgraph.md      ← LangGraph domain overlay
```

`CLAUDE_langgraph.md` must begin with:
```markdown
# LangGraph Domain Overlay
# Extends: CLAUDE.md (Python base)
# Rule: Where this file conflicts with CLAUDE.md, THIS FILE WINS for LangGraph code.
# LangSmith: NOT USED in this project — CLI trace via trace() is the observability layer.
```
Sections numbered `LG.1`, `LG.2`, etc. to avoid conflicts with base `CLAUDE.md` section numbers.

---

### Project Structure

```
tnl-help/
├── src/
│   └── concierge/
│       ├── __init__.py
│       ├── state.py             # ConciergeState TypedDict + update TypedDicts
│       ├── graph.py             # StateGraph assembly + compiled_graph export
│       ├── nodes.py             # All node functions (thin delegates)
│       ├── edges.py             # Conditional edge routing functions
│       ├── trace.py             # Centralized trace() function only
│       ├── agents/              # Agent logic — stateful, policy-aware
│       └── memory/              # MemoryService
├── config/
│   └── routing_rules.yaml
├── prompts/{agent}/policy.yaml + v1.yaml
├── memory/profiles/alex.json + sessions/.gitkeep + README.md
├── tests/
│   ├── unit/
│   │   ├── test_state_reset.py
│   │   ├── test_routing_rules.py
│   │   └── test_agent_policy.py
│   ├── integration/
│   │   └── test_graph_routing.py
│   └── conftest.py              # Shared fixtures incl. mock Anthropic client
├── spec/concierge-spec.md
├── docs/adr/ + CLAUDE_langgraph.md
├── main.py
├── validate_config.py
├── pyproject.toml
├── uv.lock                      # committed — exact reproducibility
├── requirements.txt             # generated, pre-commit synced
├── CLAUDE.md                    # Python.md base + @docs/CLAUDE_langgraph.md
├── .env.example
├── .gitignore
└── README.md
```

---

### Naming Patterns

| Element | Convention | Example |
|---------|-----------|---------|
| Agent classes | `PascalCase`, no suffix | `Dispatcher`, `RAGAgent` |
| Node functions | `snake_case_node` | `dispatcher_node`, `rag_node` |
| Edge functions | `snake_case_condition` | `route_condition`, `should_clarify` |
| Node update TypedDicts | `PascalCase` + `Update` | `DispatcherUpdate`, `RAGUpdate` |
| State fields | `snake_case` | `rag_results`, `human_handoff` |
| YAML keys | `snake_case` | `agent_name`, `max_tokens` |
| CLI trace labels | `[SCREAMING_SNAKE_CASE]` | `[DISPATCHER]`, `[RAG_AGENT]` |
| Test functions | `test_<what>_<condition>` | `test_state_reset_clears_rag_results` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 1` |

---

### State Design

```python
# src/concierge/state.py
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class ConciergeState(TypedDict):
    user_id: str
    session_id: str
    turn_id: int
    # ALWAYS use add_messages reducer — without it, messages overwrite on every node
    conversation_history: Annotated[list, add_messages]
    current_input: str
    current_response: str
    intent: str | None
    confidence: float | None
    route: str | None
    rag_results: list | None
    research_results: list | None
    source_attribution: list[str]
    memory_profile: dict | None
    proactive_suggestion: str | None
    guardrail_passed: bool
    clarification_needed: bool
    clarification_question: str | None
    human_handoff: bool
    error: str | None
```

**Per-node update TypedDicts** — nodes return these, not `dict` or full `ConciergeState`:
```python
class DispatcherUpdate(TypedDict, total=False):
    intent: str | None
    confidence: float | None
    route: str | None
    conversation_history: list
    error: str | None
    human_handoff: bool

class TurnResetUpdate(TypedDict):
    intent: None
    confidence: None
    route: None
    rag_results: None
    research_results: None
    source_attribution: list
    proactive_suggestion: None
    clarification_needed: bool
    clarification_question: None
    human_handoff: bool
    error: None
```
mypy enforces that nodes only return fields they're allowed to change. `total=False` makes all fields optional in update TypedDicts.

---

### Node Return Pattern

```python
# src/concierge/nodes.py
def dispatcher_node(state: ConciergeState) -> DispatcherUpdate:
    """
    LangGraph node interface for the Dispatcher agent.
    Returns DispatcherUpdate — only fields this node changes.
    All routing logic lives in src/concierge/agents/dispatcher.py.
    """
    trace("DISPATCHER", status="started", turn_id=state["turn_id"])
    try:
        updates: DispatcherUpdate = dispatcher.run(state)
        trace("DISPATCHER",
              outcome=f"routed to {updates.get('route')}",
              intent=updates.get("intent"),
              confidence=updates.get("confidence"))
        return updates
    except Exception as e:
        trace("DISPATCHER", outcome="error", reason=str(e))
        return DispatcherUpdate(
            error=f"[DISPATCHER] {type(e).__name__}: {e}",
            human_handoff=True
        )
```

**FORBIDDEN patterns:**
```python
def dispatcher_node(state) -> ConciergeState: ...  # ❌ full state return
def dispatcher_node(state) -> dict: ...             # ❌ untyped dict
return state                                        # ❌ mutated full state
```

---

### Structured Output for LLM Routing

```python
# src/concierge/agents/dispatcher.py
from pydantic import BaseModel, Field

class RoutingDecision(BaseModel):
    """Structured output for Dispatcher LLM classification."""
    intent: str = Field(description="Classified intent label")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence 0-1")
    route: str = Field(description="rag|research|booking_stub|fallback")
    reasoning: str = Field(description="One-sentence routing rationale")

llm_dispatcher = ChatAnthropic(model=policy.model).with_structured_output(RoutingDecision)
```

---

### CLI Trace — Centralized Function

```python
# src/concierge/trace.py
import sys
from typing import TextIO

_ALLOWLIST = {"intent", "confidence", "route", "model", "session_id",
              "turn_id", "status", "profile", "trips"}
_DENYLIST  = {"current_input", "memory_profile", "conversation_history",
              "rag_results", "research_results", "error"}

_trace_writer: TextIO = sys.stdout  # injectable for tests

def trace(node_label: str, outcome: str | None = None, **fields) -> None:
    safe = {k: v for k, v in fields.items()
            if k in _ALLOWLIST and k not in _DENYLIST}
    parts = " ".join(f"{k}={v}" for k, v in safe.items())
    line = f"[{node_label}]"
    if parts:
        line += f" {parts}"
    if outcome:
        line += f" → {outcome}"
    _trace_writer.write(line + "\n")
    _trace_writer.flush()
```

- `outcome` is an explicit parameter — no magic keyword extraction
- `_trace_writer` injectable: `monkeypatch.setattr("src.concierge.trace._trace_writer", io.StringIO())`
- `print()` permitted ONLY in `trace.py` (via `_trace_writer.write`) and `main.py`
- Format: `[SCREAMING_SNAKE_CASE] key=value → outcome` with Unicode `→` (U+2192)

---

### `validate_config.py` — 10 Checks

Run order (cheapest → most expensive):
1. Python version ≥ 3.11 — `sys.version_info`
2. `ANTHROPIC_API_KEY` present — `os.environ` check
3. All `prompts/*/policy.yaml` parse as valid `AgentPolicy` — catch `ValidationError`, format per-field actionable messages
4. All declared model names in allow-list
5. Dispatcher `max_tokens` ≤ 256 (routing output only — not exact equality)
6. `guardrail.confidence_threshold < dispatcher.confidence_threshold` (strict less-than)
7. `config/routing_rules.yaml` parses with required fields
8. `langgraph.__version__` starts with `"1."` — prints tested version in error message
9. `memory/profiles/alex.json` parses as valid `UserProfile`
10. Anthropic API reachable — **5-second timeout**; timeout prints: `"API probe timed out — check network. Key format appears valid."`

Called from `main.py`: `validate_config.run_checks()` before `from src.concierge.graph import compiled_graph`.

---

### `reset_turn_state()` — Single Source of Truth

```python
# src/concierge/agents/dispatcher.py
def reset_turn_state(state: ConciergeState) -> TurnResetUpdate:
    """
    Returns TurnResetUpdate resetting all turn-scoped fields.
    Adding a new turn-scoped field requires updating TurnResetUpdate in state.py.
    mypy enforces completeness — no separate static check needed.
    """
    return TurnResetUpdate(
        intent=None, confidence=None, route=None,
        rag_results=None, research_results=None,
        source_attribution=[], proactive_suggestion=None,
        clarification_needed=False, clarification_question=None,
        human_handoff=False, error=None,
    )
```

---

### Defensive State Access

```python
# CORRECT
results = (state.get("rag_results") or [])
profile  = state.get("memory_profile")

# FORBIDDEN
results = state["rag_results"]        # KeyError risk
results = state.get("rag_results")    # None.append() risk
```

---

### Anchor Comments (AIDEV convention)

```python
# AIDEV-NOTE: Why this non-obvious decision was made
# AIDEV-TODO: What needs to be done before production
# AIDEV-FIXME: Known bug or broken behavior
# AIDEV-QUESTION: Uncertainty that needs human review
# AIDEV-PERF: Performance-critical section — think before changing
```

Production swap-point comments:
```python
# AIDEV-TODO: PRODUCTION SWAP POINT
# Replace MockKnowledgeBase with:
# BedrockKnowledgeBase(kb_id=os.environ["BEDROCK_KB_ID"])
```

---

### Enforcement — All Agents MUST

1. Return typed `XxxUpdate` TypedDict from nodes — never `dict` or full `ConciergeState`
2. Use `Annotated[list, add_messages]` for `conversation_history`
3. Call `trace(node_label, outcome=..., **fields)` only — never `print()` or `logging` for trace
4. Use `(state.get("field") or default)` for all optional fields
5. Load `AgentPolicy` at construction — never inside `run()`
6. Use absolute imports — `from src.concierge.state import ConciergeState`
7. Add `AIDEV-NOTE` for every non-obvious decision
8. Call `fetch_docs` on mcpdoc before any uncertain LangGraph API usage

### Anti-Patterns (Forbidden)

```python
return state                           # ❌ full state return from node
return {"intent": x}                   # ❌ untyped dict — use DispatcherUpdate(intent=x)
print("Routing to RAG")                # ❌ use trace() instead
state["rag_results"].append(r)         # ❌ use (state.get("rag_results") or [])
from .dispatcher import Dispatcher     # ❌ use absolute imports
def run(self, state):
    policy = AgentPolicy.from_yaml()   # ❌ load at __init__, not run()
```

---

## Project Structure & Boundaries

### Canonical Directory Tree (with FR→File Mapping)

```
tnl-help/
├── src/
│   └── concierge/
│       ├── __init__.py
│       ├── state.py             # ConciergeState + all XxxUpdate TypedDicts + NodeName constants
│       │                        # FR: FR01-FR09 (state schema), FR43 (turn freshness), FR44 (dual-store)
│       ├── graph.py             # StateGraph assembly; exports compiled_graph; all edges defined here
│       │                        # FR: FR01 (graph topology), FR12 (routing integration)
│       ├── nodes.py             # All node functions (thin delegates + try/except boundary)
│       │                        # FR: FR01-FR09 (node interface), FR46 (no unhandled exceptions)
│       ├── edges.py             # Conditional edge routing functions ONLY; no business logic
│       │                        # FR: FR04 (confidence routing), FR28 (guardrail edge)
│       ├── trace.py             # trace() + _trace_writer + ALLOWLIST/DENYLIST
│       │                        # FR: FR33-FR38 (observability), NFR02 (no secrets in trace)
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── dispatcher.py    # Dispatcher + reset_turn_state() + RoutingDecision
│       │   │                    # FR: FR01-FR09 (routing), FR42 (context ownership)
│       │   ├── rag_agent.py     # RAGAgent + MockKnowledgeBase + PRODUCTION SWAP POINT
│       │   │                    # FR: FR10-FR17 (knowledge retrieval)
│       │   ├── research_agent.py # ResearchAgent + DuckDuckGo + graceful degradation
│       │   │                    # FR: FR10-FR17 (web search)
│       │   ├── response_synthesis.py  # SynthesisAgent + source attribution
│       │   │                    # FR: FR17 (blended response), FR18 (attribution)
│       │   ├── guardrail.py     # GuardrailAgent + one-question rule + handoff trigger
│       │   │                    # FR: FR25-FR31 (governance)
│       │   ├── followup.py      # FollowUpAgent — demonstrates conditional edges
│       │   │                    # FR: FR32 (proactive suggestion)
│       │   ├── booking_agent.py # BookingAgentStub → BookingAgentResponse Pydantic model
│       │   │                    # FR: FR25 (booking stub), integration contract
│       │   └── memory_service.py # MemoryService + UserProfile + session R/W
│       │                        # FR: FR19-FR24 (memory), Path(__file__).parent anchoring
│       └── token_budget.py      # TokenBudgetManager stub with threshold comment
│                                # G1: activation threshold documented as [TBD]
├── config/
│   └── routing_rules.yaml       # Stage 1 keyword rules + escalation_threshold
│                                # FR: FR01 (rule-based pre-filter); inline comments mandatory
├── prompts/
│   ├── dispatcher/
│   │   ├── policy.yaml          # model, prompt_version, max_tokens (≤256), confidence_threshold
│   │   └── v1.yaml              # role, context, constraints, output_format, examples (5 sections)
│   ├── rag_agent/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── research_agent/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── response_synthesis/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── guardrail/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   └── followup/
│       ├── policy.yaml
│       └── v1.yaml
├── memory/
│   ├── profiles/
│   │   └── alex.json            # Full UserProfile schema + _demo_notes field
│   │                            # FR: FR22 (pre-seeded profile), FP5 (full schema)
│   ├── sessions/                # Runtime-generated — in .gitignore
│   │   └── .gitkeep
│   └── README.md                # 3-5 lines on memory model
├── spec/
│   └── concierge-spec.md        # Version header + [TBD] markers + alternatives considered
│                                # Committed Day 1 before any agents/ or nodes/ .py file
├── docs/
│   ├── adr/
│   │   ├── 001-context-window-ownership.md  # ≤20 lines each
│   │   ├── 002-multi-model-strategy.md
│   │   ├── 003-anthropic-only-mvp.md
│   │   ├── 004-file-based-memory.md
│   │   └── 005-langgraph-framework-selection.md
│   └── CLAUDE_langgraph.md      # LangGraph domain overlay (LG.x section numbering)
├── tests/
│   ├── unit/
│   │   ├── test_state_reset.py       # reset_turn_state() completeness (NFR10)
│   │   ├── test_routing_rules.py     # Stage 1 keyword matching + confidence scores
│   │   └── test_agent_policy.py      # AgentPolicy loading, fast_mode @property
│   ├── integration/
│   │   ├── conftest.py               # autouse mock Anthropic client fixture
│   │   └── test_graph_routing.py     # Full dispatcher routing paths, mocked LLM
│   └── conftest.py                   # Shared fixtures (state factories, tmp paths)
├── main.py                      # validate_config.run_checks() → graph invocation → REPL
├── validate_config.py           # Importable module; run_checks() exits on failure
├── pyproject.toml               # Single source of truth; pythonpath = ["src"]
├── uv.lock                      # Committed — exact reproducibility
├── requirements.txt             # Generated: uv export --format requirements-txt
├── CLAUDE.md                    # Python.md content + @docs/CLAUDE_langgraph.md
├── .claude/
│   └── mcp.json                 # mcpdoc MCP server for on-demand LangGraph docs
├── .env.example                 # ANTHROPIC_API_KEY= (no value)
├── .gitignore                   # memory/sessions/, .env, __pycache__, .venv
└── README.md                    # Mermaid graph + JD table + "Navigating This Repo"
```

### FR → File Mapping (Key Bindings)

| FR Group | FRs | Primary File(s) |
|----------|-----|----------------|
| Intent Routing | FR01-FR09 | `agents/dispatcher.py` + `edges.py` + `config/routing_rules.yaml` |
| Knowledge Retrieval | FR10-FR17 | `agents/rag_agent.py` + `agents/research_agent.py` |
| Response Synthesis | FR17-FR18 | `agents/response_synthesis.py` |
| Memory & Personalization | FR19-FR24 | `agents/memory_service.py` + `memory/profiles/alex.json` |
| Governance & Safety | FR25-FR31 | `agents/guardrail.py` + `agents/booking_agent.py` |
| Follow-Up | FR32 | `agents/followup.py` + `edges.py` (conditional edge demo) |
| Observability | FR33-FR38 | `trace.py` (centralized — all nodes call this) |
| Configuration | FR39-FR46 | `validate_config.py` + `prompts/*/policy.yaml` + `state.py` |
| Session & State | FR43-FR48 | `state.py` (TypedDict schema) + `agents/memory_service.py` |
| Demo Integrity | FR49-FR53 | `main.py` + `validate_config.py` + `README.md` |

### Architectural Boundaries

**Hard boundaries — never cross these:**

| Boundary | Rule | Enforcement |
|----------|------|-------------|
| `nodes.py` ↔ `agents/` | Nodes are one-liner delegates — no business logic in nodes | mypy: node returns `XxxUpdate`, not `dict` |
| `agents/` ↔ `state.py` | Agents read state; they return `XxxUpdate` — never mutate state directly | `total=False` TypedDicts + mypy |
| `trace.py` ↔ everywhere | Only `trace.py` writes to stdout (except `main.py` banners) | Code review + ruff rule |
| `graph.py` ↔ `agents/` | `graph.py` imports nodes, never agents directly | Import graph review |
| `config/` ↔ `prompts/` | `config/` = system behavior; `prompts/` = LLM config — no overlap | Directory ownership documented |
| `memory/sessions/` ↔ git | Session files never committed | `.gitignore` enforces; `.gitkeep` only |
| Secrets ↔ any file | API keys only from env — never written to disk by any module | `trace.py` DENYLIST; `.gitignore` |

**Soft boundaries — conventions enforced by review:**

- `edges.py` contains routing logic (if/else on state); `graph.py` wires them via `add_conditional_edges`
- `agents/` classes load `AgentPolicy` once at `__init__` — never inside `run()`
- All file paths use `Path(__file__).parent` anchoring — never `os.getcwd()`
- `spec/concierge-spec.md` remains authoritative — code must not contradict the spec silently

### Integration Points

| Integration | File | Contract | Failure Mode |
|------------|------|----------|-------------|
| Anthropic API | `agents/*.py` (all) | `ChatAnthropic(model=policy.model)` | Catch `anthropic.APIError`; set `error` field; `human_handoff=True` |
| DuckDuckGo Search | `agents/research_agent.py` | `DDGS().text(query, max_results=5)` | Catch all exceptions; return empty results with `AIDEV-NOTE` log |
| File Memory | `agents/memory_service.py` | `Path(__file__).parent / "../../memory"` | Missing profile → fresh session (warn, don't crash) |
| Stage 1 Rules | `agents/dispatcher.py` | Load `config/routing_rules.yaml` once at init | Missing file → `validate_config` catches this pre-run |
| Agent Policies | All agents | Load `prompts/{agent}/policy.yaml` at `__init__` | `ValidationError` → `validate_config` catches pre-run |
| LangGraph graph | `graph.py` → `main.py` | `compiled_graph = graph.compile()` | Import-time errors surface before first user input |

---

### Party Mode Enhancements (P1–P7)

_Seven team personas stress-tested the structure. All applied._

| ID | Persona | Concern | Applied Enhancement |
|----|---------|---------|---------------------|
| P1 | UX Designer (Sally) | Hiring manager disoriented by `src/concierge/` nesting — three directories deep before hitting code | README "Navigating This Repo" section lists exact file to read first: `src/concierge/state.py` — the entire data model in one file. Layer 2 entry point made explicit |
| P2 | QA Engineer (Quinn) | `tests/integration/conftest.py` vs `tests/conftest.py` — wrong fixture scope kills integration mocks | `tests/integration/conftest.py` gets its own `autouse` mock Anthropic fixture; `tests/conftest.py` holds only state factories and tmp path helpers (no API mocking at root level) |
| P3 | Dev (Amelia) | `nodes.py` single file grows to 7+ node functions — becomes a 200-line file fast | Each node stays in `nodes.py` for MVP (7 nodes × ~15 lines = ~105 lines, acceptable). If any node requires >30 lines (complex error routing), split to `nodes/` package. Threshold documented |
| P4 | Tech Writer (Paige) | `docs/adr/` is invisible unless README links it explicitly | README "Architecture Decisions" section lists all 5 ADRs with one-sentence summaries inline — no separate navigation required |
| P5 | PM (John) | `token_budget.py` stub with no visible activation threshold is a dead-end — hiring manager cannot tell if it's planned or forgotten | `token_budget.py` opens with: `# AIDEV-TODO: Activation threshold: summarize when turn_count > [TBD]. See spec/concierge-spec.md §TokenBudget.` — links back to the spec where the threshold decision is documented as deliberately deferred |
| P6 | Architect (Winston) | `agents/rag_agent.py` PRODUCTION SWAP POINT comment must be machine-readable, not just human-readable | Production swap point format standardized: `# AIDEV-TODO: PRODUCTION SWAP POINT — replace MockKnowledgeBase with BedrockKnowledgeBase(kb_id=os.environ["BEDROCK_KB_ID"])`. All swap points indexed in `spec/concierge-spec.md` §ProductionPath |
| P7 | Business Analyst (Mary) | `alex.json` `_demo_notes` field has no defined schema — arbitrary metadata is a smell | `UserProfile` schema includes `_demo_notes: dict[str, str]` typed field. `alex.json` populates it with keys: `preferred_name`, `demo_scenario`, `routing_showcase_queries` |

---

### Failure Mode Analysis (FM1–FM12)

_Structural failure modes identified and mitigated._

| ID | File/Component | Failure Mode | Mitigation |
|----|---------------|-------------|-----------|
| FM1 | `src/` layout | `ImportError: No module named 'concierge'` on bare `python main.py` | `pyproject.toml`: `[tool.pytest.ini_options] pythonpath = ["src"]`; `main.py` adds `sys.path.insert(0, Path(__file__).parent / "src")` before imports; README quickstart uses `python -m concierge` or documents the PYTHONPATH requirement |
| FM2 | `state.py` | Circular import: `state.py` imports from `agents/`; `agents/` imports from `state.py` | `state.py` is a pure data module — imports only `typing`, `typing_extensions`, `langgraph.graph.message`. Zero imports from `agents/` or `nodes.py` |
| FM3 | `graph.py` | `compiled_graph = graph.compile()` at module-level executes on import — causes `validate_config` to fail before checks run | `graph.py` exposes `build_graph() -> CompiledGraph` factory function. `main.py` calls `build_graph()` after `validate_config.run_checks()`. Module-level compile removed |
| FM4 | `nodes.py` | 7 nodes in one file: function names clash with agent module names (`dispatcher` the function vs `dispatcher` the import) | Import agents with module prefix: `from src.concierge.agents import dispatcher as dispatcher_agent`. Node functions named `dispatcher_node`, not `dispatcher`. Naming table in Implementation Patterns enforces this |
| FM5 | `edges.py` | Edge condition function contains business logic (confidence scoring, threshold comparison) — duplicates dispatcher | `edges.py` reads state fields only — `state["confidence"]`, `state["route"]`, `state["human_handoff"]`. All thresholds loaded from `AgentPolicy` in `agents/dispatcher.py`, not re-read in `edges.py` |
| FM6 | `agents/*.py` | `AgentPolicy` loaded inside `run()` — re-reads YAML on every turn (slow + hides parse errors until runtime) | All agents load `self.policy = AgentPolicy.from_yaml(...)` in `__init__`. `validate_config` exercises all policy loads pre-run. Anti-pattern table in Implementation Patterns flags this |
| FM7 | `memory/sessions/` | Session `.json` files committed to git on Windows (`.gitignore` uses Unix `/` prefix which git for Windows may not honor) | `.gitignore` entry: `memory/sessions/*.json` (no leading `/`). Also add: `!memory/sessions/.gitkeep`. Tested on `git status` before first commit |
| FM8 | `prompts/*/v1.yaml` | New prompt YAML omits `output_format` section — passes `AgentPolicy` validation but breaks LLM routing | `AgentPolicy` Pydantic model adds `prompt_sections: list[str]` field validated against `["role", "context", "constraints", "output_format", "examples"]` — all 5 sections required. `validate_config` check 3 enforces this |
| FM9 | `config/routing_rules.yaml` | Missing `escalation_threshold` key parses silently as `None` — Stage 1 never routes, all traffic hits LLM | `validate_config` check 7: assert `routing_rules["escalation_threshold"]` is `float` and in range `[0.0, 1.0]`. Type mismatch exits with actionable message |
| FM10 | `tests/integration/` | Developer adds real API call in integration test — CI breaks when `ANTHROPIC_API_KEY` absent | `tests/integration/conftest.py` `autouse` fixture: `monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-fake")` + patches `anthropic.Anthropic`. Real calls fail at fixture level with clear message: "Use tests/manual/ for live API tests" |
| FM11 | `docs/adr/` | ADR files exceed 20 lines when edited — lose the "lightweight signal" value | ADRs use fixed template: Status / Context (2 lines) / Decision (3 lines) / Consequences (2 lines) / Alternatives Rejected (2 lines) = 9-14 lines. Template committed to `docs/adr/TEMPLATE.md`. PR review checks line count |
| FM12 | `validate_config.py` | Wrong check order: API probe (check 10) runs before policy YAML validation (check 3) — confusing error when YAML is malformed but network is slow | Explicit ordered check list in `run_checks()`: `checks = [check_python_version, check_api_key_present, check_policies_valid, ...]`. Numbered comments match architecture doc. Early-return on each failure with count of remaining skipped checks: `"1 check failed. 9 checks skipped."` |

---

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**

All technology choices are compatible and mutually reinforcing:
- `uv` + `pyproject.toml` + `uv.lock` form a consistent dependency management chain; `requirements.txt` is a derived artifact regenerated by pre-commit hook — no manual sync required
- LangGraph 1.0.x `StateGraph` + typed `ConciergeState` + `add_messages` reducer + per-node `XxxUpdate` TypedDicts form a cohesive pattern; version chosen because core graph API was preserved from 0.2.x
- `FAST_MODE` env var set by `main.py` before any `AgentPolicy` instantiation — execution sequence confirmed; no race condition
- `build_graph()` factory pattern (FM3 mitigation) ensures `validate_config.run_checks()` completes before graph compile — startup sequence is deterministic
- `TurnResetUpdate` (non-`total=False`, all fields required) vs `XxxUpdate` (`total=False`, partial updates) — correct split; mypy enforces completeness of reset, optionality of node updates

**Pattern Consistency:**

All patterns are uniform across all 7 nodes and 7 agents:
- Node signature: `def xxx_node(state: ConciergeState) -> XxxUpdate` — no exceptions
- Agent interface: `__init__(self, policy: AgentPolicy)` + `run(self, state) -> XxxUpdate`
- Trace call: `trace("LABEL", outcome="...", **allowlisted_fields)` — no ad-hoc variants
- Error path: every node `try/except` → `XxxUpdate(error="...", human_handoff=True)`
- File path: `Path(__file__).parent` anchoring — no `os.getcwd()` anywhere

**Structure Alignment:**

- `state.py` as pure data module with zero upward imports prevents all circular dependency risks (FM2)
- `edges.py` reads state fields only; all threshold values live in `AgentPolicy` loaded by `agents/dispatcher.py` — no logic duplication (FM5)
- `graph.py` → `nodes.py` → `agents/` → `state.py` import chain is acyclic and verifiable

---

### Requirements Coverage Validation ✅

**Functional Requirements Coverage (55 FRs across 8 categories):**

All FR categories have direct file ownership, integration contract, and failure mitigation documented. FR→file mapping in Project Structure section provides one-to-one traceability. Every agent's agent file is mapped to its FR group. No FR category is orphaned.

**Non-Functional Requirements Coverage (17 NFRs):**

| NFR Area | Coverage |
|----------|----------|
| Performance (cold start, dispatch latency) | `FAST_MODE`, API probe 5s timeout, no module-level compile |
| Security (API key handling) | `trace.py` DENYLIST, `.gitignore`, `validate_config` check 2 |
| Reliability (no unhandled exceptions, stale state) | Node `try/except` boundary, `TurnResetUpdate`, mypy enforcement |
| Developer Experience (clone-to-run, pre-flight) | `uv sync`, `validate_config.run_checks()`, README quickstart |
| Documentation (README, spec, ADRs) | Mermaid graph, JD table, 5 ADRs ≤20 lines, spec-first git discipline |

---

### Implementation Readiness Validation ✅

**Decision Completeness:**
All 4 core decisions documented with rationale, code examples, and impact analysis. 5 deferred decisions documented with explicit reasons — no silent gaps. LangGraph 1.0.x pinned with version assertion in `validate_config`.

**Structure Completeness:**
Canonical directory tree is complete with FR annotations on every file. All 7 node functions defined. All integration points have contracts and failure modes. `NodeName` constants class prevents routing string mismatches.

**Pattern Completeness:**
Mandatory rules (8), FORBIDDEN patterns (7), anti-patterns (6), AIDEV anchor conventions, defensive state access, production swap-point format — all specified. An AI agent reading this document has no ambiguous decision points for MVP implementation.

---

### Gap Analysis Results

**Critical Gaps: None**

All G1–G10, PM1–PM5, RT1–RT5, FP1–FP6, CR1–CR12, P1–P7, FM1–FM12 addressed and incorporated.

**Important Gaps — RESOLVED 2026-02-25:**

| # | Gap | Resolution |
|---|-----|-----------|
| VG1 | Follow-Up edge condition unspecified | ✅ Defined in `spec/concierge-spec.md` §FollowUpCondition: `confidence ≥ 0.8 AND clarification_needed == False AND turn_id > 1 AND not human_handoff AND route in ("rag", "research")`. `edges.should_run_followup()` is the canonical implementation location. |
| VG2 | Demo script queries not documented | ✅ Defined in `memory/profiles/alex.json` `_demo_notes.routing_showcase_queries`: 5 queries with expected stage, route, intent, min confidence, trace format, and what each demonstrates. `tests/unit/test_routing_rules.py` has a concrete assertion pattern in §DemoScript. |

**Nice-to-Have (optional, post-MVP):**

| # | Gap |
|---|-----|
| NTH1 | `docs/adr/TEMPLATE.md` referenced in FM11 but not in tree — add it |
| NTH2 | `.pre-commit-config.yaml` not in tree — add after initial scaffold |
| NTH3 | `spec/concierge-spec.md` §ProductionPath swap-point index (P6) — add before demo day |

---

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed (55 FRs, 17 NFRs, 8 cross-cutting concerns)
- [x] Scale and complexity assessed (medium complexity, 7 nodes, 5-day solo build)
- [x] Technical constraints identified (Python 3.11+, LangGraph 1.0.x, Anthropic-only, CLI-only)
- [x] Cross-cutting concerns mapped (observability, state reset, graceful degradation, API safety, spec-first discipline)

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions and rationale (4 decisions)
- [x] Technology stack fully specified (uv, ruff, mypy, pytest, LangGraph 1.0.x, Anthropic SDK)
- [x] Integration patterns defined (Anthropic API, DuckDuckGo, file memory, YAML configs)
- [x] Performance considerations addressed (FAST_MODE, cold start, probe timeout)

**✅ Implementation Patterns**
- [x] Naming conventions established (8 categories, node/agent/edge/update/trace labels)
- [x] Structure patterns defined (src/ layout, test tiers, config/prompts split)
- [x] Communication patterns specified (typed TypedDicts, RoutingDecision structured output)
- [x] Process patterns documented (error handling, state reset, policy loading, tracing)

**✅ Project Structure**
- [x] Complete directory tree defined with FR annotations on every file
- [x] Component boundaries established (hard and soft boundary tables)
- [x] Integration points mapped with contracts and failure modes
- [x] FR→file mapping complete (8 FR groups, all 55 FRs traceable)

**⚠️ 2 Important Gaps** — VG1 (FollowUp edge condition) and VG2 (demo queries) — resolve in `spec/concierge-spec.md` Day 1

---

### Architecture Readiness Assessment

**Overall Status: READY FOR IMPLEMENTATION**

**Confidence Level: High** — Seven full validation rounds (Steps 1-6 advanced elicitation, party mode, failure analysis) have driven the gap count from 10 critical architectural unknowns (G1-G10) to 2 spec-level details that belong in `concierge-spec.md`, not in the architecture document.

**Key Strengths:**
1. **Hiring manager legibility** — three-layer engagement (30s / 3min / 10min) designed into every artifact; JD mapping table, Mermaid graph, and "Navigating This Repo" section address Layer 1 before a single line of code is written
2. **LangGraph pattern correctness** — `XxxUpdate` TypedDicts, `add_messages` reducer, `build_graph()` factory, `with_structured_output()` for routing — all verified against `CLAUDE_langgraph.md` standards
3. **Demo reliability engineering** — `validate_config.py` 10-check pre-flight, FAST_MODE documented as dev path (not demo path), Stage 1 query pre-validation testable without LLM
4. **Fail-safe architecture** — every node catches exceptions; every optional component degrades gracefully; `trace.py` fires even on error path; memory miss never crashes
5. **Spec-first discipline enforced** — git commit order is the enforcement mechanism; `spec/concierge-spec.md` is the authoritative contract referenced by README, ADR-005, and all AIDEV-NOTE anchors

**Areas for Future Enhancement (post-MVP):**
- Provider abstraction layer (ADR-003: Anthropic-only is MVP-locked)
- `TokenBudgetManager` activation threshold (G1: deliberately deferred)
- SIGINT memory flush handler (G3: demo stability nice-to-have)
- Session file TTL/cleanup (G4: known limitation, documented)
- `AgentPolicy.allowed_tools` runtime enforcement (declarative only in MVP)

---

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented — deviations require ADR update
- Use `XxxUpdate` TypedDicts for all node returns — never `dict` or full `ConciergeState`
- Run `validate_config.run_checks()` mentally before every implementation step — if an implementation would break a check, fix the check too
- Refer to this document for all architectural questions; refer to `spec/concierge-spec.md` for contract-level details

**First Implementation Priority (Day 1 sequence):**
```bash
# 1. Init repo + gitignore
git init && git add .gitignore && git commit -m "chore: gitignore before any runtime files"

# 2. Write spec FIRST — before any .py in agents/, nodes/, graph/
# spec/concierge-spec.md: include VG1 (FollowUp condition) + VG2 (demo queries) + §ProductionPath
git add spec/concierge-spec.md && git commit -m "spec: concierge spec before implementation"

# 3. Scaffold: pyproject.toml → uv sync → CLAUDE.md + .claude/mcp.json
# 4. state.py (ConciergeState + all XxxUpdate TypedDicts + NodeName)
# 5. validate_config.py (10 checks — runs standalone before graph exists)
# 6. config/routing_rules.yaml + prompts/*/policy.yaml (all 6 agents)
# 7. agents/ (dispatcher first — includes reset_turn_state + RoutingDecision)
# 8. nodes.py (after all agents exist)
# 9. edges.py (after spec §FollowUpCondition is written)
# 10. graph.py (build_graph() factory — after all nodes + edges)
# 11. main.py (validate_config → build_graph → REPL loop)
# 12. tests/ (alongside agents — not after)
```
