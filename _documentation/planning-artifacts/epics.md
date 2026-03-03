---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
elicitationRounds:
  - Cross-Functional War Room (critical path, milestones, nice-to-cut)
  - Red Team vs Blue Team (edge cases, non-determinism, error handling)
  - Tree of Thoughts (Stage 1/2/Guardrail flow clarity)
  - Architecture Decision Records (formalized ADRs 001-004)
---

# TNL-HELP - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for TNL-HELP, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Intent Routing & Dispatch**

- FR1: System can accept a natural language message and initiate the agent routing lifecycle
- FR2: Dispatcher can classify high-confidence intents without invoking an LLM
- FR3: Dispatcher can escalate ambiguous intents through a secondary classification step
- FR4: Dispatcher can emit a structured routing decision including intent label and confidence score on every message
- FR5: Dispatcher can route messages to the appropriate agent based on intent classification result
- FR6: System can ensure sub-agent outputs from previous turns do not affect current turn processing
- FR7: System can accept a `--fast-mode` CLI flag that overrides all agent models to a lightweight model for development testing
- FR8: Dispatcher can maintain the full conversation history as the sole context owner across an entire session
- FR51: Dispatcher can route messages to specialist agents for response generation — it does not generate user-facing responses directly

**Knowledge Retrieval**

- FR9: RAG Agent can retrieve relevant entries from a structured JSON file serving as the knowledge base
- FR10: Research Agent can perform web search using DuckDuckGo given a user query
- FR11: System can degrade gracefully to KB-only responses when web search is unavailable, labeled with `[WEB SEARCH UNAVAILABLE]`
- FR12: Response Synthesis can merge RAG Agent and Research Agent results into a single blended response
- FR13: Response Synthesis can attribute sources inline in the final response, distinguishing internal KB from web search results
- FR14: Research Agent can operate without access to the full session conversation history
- FR15: Knowledge base can expose production swap-point comments identifying the replacement path to a hosted vector database
- FR54: System can label inline source attributions with consistent tags distinguishing internal KB results from web search results

**Memory & Personalization**

- FR16: Memory Service can load a user profile from a local JSON file at session start
- FR17: Memory Service can write session data to a local JSON file at session end
- FR18: System can generate a single proactive memory-driven greeting at session start, before any user input, when a profile exists
- FR19: System ships with a pre-seeded demo user profile (`alex`) containing past trips, preferences, and a cached research session
- FR20: User can inspect the demo persona's memory state as a readable local JSON file during the demo
- FR21: System can start a fresh session without personalization when no profile file exists, without crashing

**Governance & Safety**

- FR22: Guardrail can detect when response confidence is below the agent's configured `confidence_threshold` and emit one clarifying question per turn
- FR23: Guardrail can classify queries as out-of-domain and return a labeled deflection response
- FR24: System can route to a human handoff message when confidence remains below threshold after the maximum number of clarification attempts
- FR25: BookingAgent stub can return a labeled message indicating the integration point for a real booking service, and expose an integration contract in code
- FR26: System can enforce a configurable maximum number of clarification attempts per session before triggering human handoff
- FR27: System can ensure internal memory management messages are never exposed in user-facing responses
- FR28: Follow-Up Node can conditionally inject a proactive suggestion after a Research Agent response, based on a configured graph edge condition

**Observability & Tracing**

- FR29: System can print a labeled trace entry for every graph node transition during execution
- FR30: System can print Dispatcher routing decisions with intent classification, confidence score, and destination agent
- FR31: System can print Memory Service load and write events with profile metadata at session boundaries
- FR48: Dispatcher can emit routing decisions in a consistent structured format parseable by the CLI trace printer
- FR50: System can format all trace output using a consistent bracket-label convention: `[NODE_NAME] key=value → outcome`
- FR53: System can include the active model name in CLI trace output for each agent invocation

**Configuration & Extensibility**

- FR34: Each agent can declare its LLM model and prompt version in a versioned YAML policy file without requiring code changes
- FR35: System can enforce per-agent token output limits declared in `AgentPolicy` before each LLM call
- FR36: Developer can add a new agent capability by wiring a new graph node without modifying the Dispatcher's core classification logic
- FR37: Developer can change an agent's prompt by incrementing its version in the YAML without touching graph code
- FR38: System can validate all policy YAML configurations and API credentials via a standalone pre-run script before the main application starts
- FR39: System can detect when conversation context approaches the model's token limit
- FR40: System can compress oldest conversation turns to preserve recent context when approaching token limits
- FR46: System can assign a different LLM model to each agent based on its declared policy configuration

**Session & State Management**

- FR41: System can maintain a typed state schema covering all agent handoffs within a session
- FR42: System can ensure agents always operate on data from the current conversation turn
- FR43: System can persist the full conversation history to a local session file regardless of LLM context window constraints
- FR45: System can write session data to disk when the user exits, preserving continuity for the next session
- FR49: User can inspect session history files in a labeled directory without additional tooling
- FR52: System can maintain conversation history in two distinct stores — in-session state for active routing and a persisted file for cross-session continuity

**Demo Integrity & Developer Experience**

- FR44: System can run end-to-end from a single terminal command with one required environment variable (`ANTHROPIC_API_KEY`)
- FR47: System can notify the user when operating in reduced-capability mode via a visible session banner
- FR55: System ships with a documented demo script containing pre-validated queries with known expected routing outcomes
- FR56: System can restore the demo user profile to its pre-seeded state via a documented reset command
- FR57: System can surface actionable error messages when LLM API calls fail, without exposing raw stack traces

### NonFunctional Requirements

**Performance**

- NFR1: Cold start to first agent response (including profile load + first Dispatcher LLM call) completes within 10 seconds
- NFR2: A full demo script execution (5 user turns, 4 distinct agent routes) completes in under 5 minutes total
- NFR3: Dispatch loop overhead (state reset + routing decision emission) adds less than 2 seconds per turn, excluding LLM API latency
- NFR4: In `--fast-mode` with Haiku, cold start to first response completes within 5 seconds

**Security**

- NFR5: API keys are loaded from environment variables or `.env` file only — never written to config files, session files, or trace output
- NFR6: No credentials, API keys, or user identifiers are written to any file the system creates during normal operation
- NFR7: `.env` is listed in `.gitignore` and absent from all commits; `.env.example` documents required variables without values

**Reliability**

- NFR8: System must not raise an unhandled exception when any optional component (DuckDuckGo, memory profile, session file) is unavailable
- NFR9: If an Anthropic API call fails, system retries once and surfaces an actionable error message — does not silently drop the user's turn or hang
- NFR10: A two-turn conversation that switches agent routes between turns must produce correct, non-stale output on 100% of runs — validated by unit test

**Developer Experience**

- NFR11: A developer can go from `git clone` to a running first session in under 5 minutes
- NFR12: `validate_config.py` surfaces all configuration errors before any LLM call is made, each with a specific fix instruction
- NFR13: All agent policy YAML files follow a consistent schema — a new contributor can create a valid policy file by copying an existing one

**Documentation**

- NFR14: README contains a Mermaid agent topology diagram showing the full graph structure
- NFR15: README contains a table mapping every major architectural decision to a specific job description requirement
- NFR16: ADR-001 (context window ownership) and ADR-002 (multi-model strategy) are documented in the repo
- NFR17: `spec/concierge-spec.md` exists and is written before any implementation begins

### Additional Requirements

**From Architecture — Starter Template & Structure**

- No starter template; custom project structure from `spec/concierge-spec.md` defines directory layout before any code
- LangGraph version pinned to `langgraph==1.0.x` (stable); `validate_config.py` asserts version starts with `"1."`
- All dependencies exact-pinned (`==`) in `requirements.txt` — not minimum versions
- `.gitignore` committed Day 1 before any `main.py` execution; `memory/sessions/` must never appear in git history
- `spec/concierge-spec.md` committed before any `.py` file in `agents/`, `nodes/`, or `graph/` — Git timestamp is enforcement

**From Architecture — Core Architecture Constraints**

- Dispatcher hybrid routing uses two distinct config files: `config/routing_rules.yaml` (Stage 1 rules + `escalation_threshold`) and `prompts/dispatcher/policy.yaml` (Stage 2 LLM + `confidence_threshold`)
- `validate_config.py` must assert `guardrail.confidence_threshold < dispatcher.confidence_threshold` (strict less-than)
- Dispatcher `max_tokens == 128` enforced as exact assertion in `validate_config.py` (load-bearing; misconfiguration breaks routing silently)
- Error handling: catch at node boundary, not in `main.py`; `state["error"]` field reset by `reset_turn_state()` each turn; no exception escapes graph boundary
- `reset_turn_state(state)` helper centralizes all sub-agent field resets; `validate_config.py` static check asserts all optional `ConciergeState` fields appear in this helper
- Centralized `trace()` function with explicit field allowlist (`intent`, `confidence`, `route`, `model`, `session_id`) and denylist (`current_input`, `memory_profile`, `conversation_history`, `rag_results`, `research_results`) — no ad-hoc f-strings in nodes

**From Architecture — Configuration & Validation**

- `validate_config.py` runs as importable module: `main.py` calls `validate_config.run_checks()` before `from graph import compiled_graph`; 10 ordered checks from Python version through `alex.json` validity
- `--fast-mode` implemented via environment variable: `os.environ["FAST_MODE"] = "1"` set by `main.py`; `AgentPolicy.model` is a `@property` reading this env var
- Python 3.11+ asserted via `sys.version_info >= (3, 11)` in `main.py` before any imports
- One Anthropic API probe call in `validate_config.py` verifies key is active before demo

**From Architecture — Testing**

- Two-tier testing: pure unit tests (no LLM, no mocking) + mocked integration tests (`unittest.mock.patch` on `anthropic.Anthropic`)
- `tests/conftest.py` with shared mock Anthropic client fixture
- `pytest` exact-pinned in `requirements.txt`

**From Architecture — Design Artifacts**

- `BookingAgentResponse` Pydantic model with fields `status`, `message`, `integration_point`, `required_env_vars` — stub returns this model, not a bare string
- `alex.json` demonstrates full `UserProfile` schema with `_demo_notes` field; `memory/README.md` explains memory model in 3–5 lines
- Memory Service paths resolved relative to `Path(__file__).parent`, not CWD; silent profile miss emits visible warning
- Architecture must work at three engagement layers: Layer 1 (30s README scan), Layer 2 (3min source reading), Layer 3 (10min demo execution)
- `routing_rules.yaml` must be self-documenting with inline comments explaining each rule
- All production swap-point comments are readable design statements

### FR Coverage Map

- FR1: Epic 2 — Dispatcher accepts natural language, starts routing lifecycle
- FR2: Epic 3 — Rule-based pre-filter (no LLM) classifies high-confidence intents
- FR3: Epic 3 — LLM escalation for ambiguous intents
- FR4: Epic 3 — Structured routing decision emitted on every message
- FR5: Epic 3 — Route to correct agent based on classification
- FR6: Epic 3 — `reset_turn_state()` helper; sub-agent fields reset each turn
- FR7: Epic 2 — `--fast-mode` CLI flag + `FAST_MODE` env var; `AgentPolicy.model` property
- FR8: Epic 3 — Dispatcher owns full conversation history across session
- FR9: Epic 5 — RAG Agent retrieves from JSON KB
- FR10: Epic 5 — Research Agent DuckDuckGo web search
- FR11: Epic 5 — Graceful degradation to KB-only with `[WEB SEARCH UNAVAILABLE]` label
- FR12: Epic 5 — Response Synthesis blends RAG + Research results
- FR13: Epic 5 — Inline source attribution distinguishing KB from web
- FR14: Epic 5 — Research Agent operates on scoped context only (no full session history)
- FR15: Epic 5 — Production swap-point comments in KB identifying Bedrock replacement path
- FR16: Epic 4 — Memory Service loads user profile from local JSON at session start
- FR17: Epic 4 — Memory Service writes session data to local JSON at session end
- FR18: Epic 4 — Proactive memory-driven greeting fires before first user input
- FR19: Epic 4 — Pre-seeded `alex` demo profile ships with repo
- FR20: Epic 4 — Demo persona memory state inspectable as readable JSON mid-demo
- FR21: Epic 4 — Fresh session fallback (no personalization, no crash) when profile missing
- FR22: Epic 6 — Guardrail: confidence below threshold → one clarifying question per turn
- FR23: Epic 6 — Guardrail: out-of-domain deflection with labeled response
- FR24: Epic 6 — Human handoff after max clarification attempts exceeded
- FR25: Epic 6 — BookingAgent stub returns `BookingAgentResponse` Pydantic model with integration contract
- FR26: Epic 6 — Max clarification attempts per session configurable and enforced
- FR27: Epic 6 — `system_summary` messages filtered from user-facing responses
- FR28: Epic 6 — Follow-Up Node: conditional edge after Research Agent, proactive suggestion
- FR29: Epic 3 — CLI trace entry printed for every graph node transition
- FR30: Epic 3 — Dispatcher routing decisions printed with intent, confidence, destination
- FR31: Epic 4 — Memory Service load/write events printed with profile metadata
- FR34: Epic 1 — Per-agent YAML policy schema defined; all 6 agents have `policy.yaml` + `v1.yaml`
- FR35: Epic 5 — Per-agent `max_tokens` enforced before each LLM call
- FR36: Epic 7 — New agent = new node + new YAML; no Dispatcher rewrite required (validated by test)
- FR37: Epic 7 — Prompt versioning via YAML version bump; no code change required
- FR38: Epic 1 — `validate_config.py` pre-run script with all 10 ordered checks
- FR39: Epic 7 — `TokenBudgetManager` detects when context approaches token limit
- FR40: Epic 7 — `TokenBudgetManager` stub compresses oldest turns; activation threshold documented in comment
- FR41: Epic 1 — `ConciergeState` TypedDict defined in `spec/concierge-spec.md`
- FR42: Epic 3 — Agents always operate on current-turn data (enforced by reset protocol)
- FR43: Epic 4 — Full conversation history persisted to local session file
- FR44: Epic 2 — Single-command startup: `python main.py --user alex` with one required env var
- FR45: Epic 4 — Session data written to disk on user exit
- FR46: Epic 2 — Per-agent model assigned from `AgentPolicy` loaded from `policy.yaml`
- FR47: Epic 2 — Reduced-capability mode banner printed when `--fast-mode` active
- FR48: Epic 3 — Dispatcher routing decisions in consistent structured format parseable by CLI trace
- FR49: Epic 4 — Session history files in labeled `memory/sessions/` directory, inspectable without tooling
- FR50: Epic 3 — Consistent `[NODE_NAME] key=value → outcome` bracket-label trace format
- FR51: Epic 3 — Dispatcher routes to specialist agents; does not generate user-facing responses directly
- FR52: Epic 4 — Dual-store: in-session `ConciergeState` for routing + persisted file for cross-session
- FR53: Epic 3 — Active model name included in CLI trace output for each agent invocation
- FR54: Epic 5 — Consistent inline source attribution tags: `[RAG]` vs `[Web]`
- FR55: Epic 7 — Demo script with pre-validated queries and expected routing paths
- FR56: Epic 7 — Profile reset command documented (`git checkout -- memory/profiles/alex.json`)
- FR57: Epic 2 — Actionable error messages on LLM API failure; no raw stack traces exposed

## Critical Path & Risk Mitigation

### Critical Path Stories (Must Complete by EOD Day 2–3)

These 4 stories form the foundation; any slip cascades to dependent work:

1. **Story 2.1** — `graph/__init__.py` State Initialization (Foundation for graph wiring)
2. **Story 3.1** — `reset_turn_state()` Helper + Unit Test (Cross-cutting; impacts all agents)
3. **Story 3.2** — Centralized `trace()` Function (Cross-cutting; every node depends on it)
4. **Story 5.1** — Mock JSON Knowledge Base (Blocks RAG Agent, Research Agent)

**Mitigation:** If any critical path story slips, immediately escalate; these block Day 3 agent implementation.

### Key Milestones

- **EOD Day 2:** Stories 2.1, 3.1, 3.2 complete. Graph compiles, stubs wire, trace function validated.
- **EOD Day 3:** Story 5.1 + all agents live. **Run demo script queries (Story 7.3 validation) to verify routing works before Day 5 polish.**
- **EOD Day 4:** All governance, memory, retrieval, safety logic complete. Follow-Up node (Story 6.5) — optional, cut if timeline pressure.
- **EOD Day 5:** Demo polish, docs, final validation.

### Nice-to-Cut Story

**Story 6.5** (Follow-Up Node with Conditional Edge) — Demonstrates LangGraph architectural sophistication but is not load-bearing for MVP. If Day 4 runs over, this is the first cut without breaking the core demo. MVP is complete without it.

### Cross-Cutting Risk

**Story 3.2** (Centralized `trace()` Function) — Every node calls this function. If the signature or allowlist/denylist logic is wrong, refactoring cascades across 7 agents on Day 4. **Test Story 3.2 acceptance criteria exhaustively; don't defer to Day 4 integration.**

---

## Architecture Decision Records (ADRs)

### ADR-001: Hybrid Dispatcher (Rule-Based Stage 1 + LLM Stage 2)

**Decision:** Two-stage dispatcher: Stage 1 keyword-matches against `routing_rules.yaml` for deterministic routing; Stage 2 escalates ambiguous queries to LLM.

**Trade-off:** Deterministic speed + demo reliability vs. LLM nuance for edge cases.

**Rationale:**
- Stage 1 (Story 3.3) routes "book a flight" in <100ms (deterministic).
- Stage 2 (Story 3.4) handles "something about Southeast Asia" via LLM (intelligent).
- Guardrail (Story 6.1) catches Stage 1 false positives via clarifying question.
- Context preservation (Story 3.7) ensures multi-turn resilience.

**Implication:** `config/routing_rules.yaml` must be maintained; post-MVP: add Stage 1 confidence learning.

---

### ADR-002: File-Based Memory (JSON) vs. Database

**Decision:** Profiles and sessions stored as local JSON files (`memory/profiles/{user_id}.json`, `memory/sessions/{session_id}.json`).

**Trade-off:** Simplicity + zero infrastructure + transparency vs. scalability and transaction guarantees.

**Rationale:**
- MVP constraint: single developer, no cloud setup (Story 1.1).
- Hiring manager can inspect `memory/profiles/alex.json` mid-demo (Story 4.2 transparency).
- JSON load/save is ~10 lines of Python (Story 4.1).
- Known limitation documented; production swap-point: Bedrock Knowledge Base (Story 5.1 code comment).

**Implication:** `memory/sessions/` unbounded growth (known limitation); reset via `git checkout` (Story 7.6).

---

### ADR-003: Per-Agent `max_tokens` (AgentPolicy) vs. Global Budget

**Decision:** Each agent declares its own `max_tokens` in `AgentPolicy`: Dispatcher=128, RAG=512, Research=1024, Guardrail=256.

**Trade-off:** Complexity vs. resource efficiency + extensibility.

**Rationale:**
- **Load-bearing:** Dispatcher's 128-token cap is critical (Story 3.5). Misconfiguration breaks routing silently.
- **Extensibility:** New agent (Story 7.4) adds policy YAML; no code changes (FR36).
- **Validation:** `validate_config.py` asserts Dispatcher == 128 before first LLM call (Story 1.4).
- **Right-sized:** Research gets 1024 (complex synthesis), Guardrail gets 256 (pass/fail).

**Implication:** `AgentPolicy` becomes the extension interface; post-MVP tokenizer tuning is per-agent.

---

### ADR-004: Dual-Store Architecture (In-Session + Persisted File)

**Decision:** `conversation_history` in `ConciergeState` (LLM context managed by TokenBudgetManager); full history written to `memory/sessions/{session_id}.json` on exit.

**Trade-off:** Complexity vs. crash-resilience + cross-session continuity.

**Rationale:**
- **Reliability:** Session file (Story 4.3) survives process crashes; full history never lost.
- **Context Window:** TokenBudgetManager (Story 7.2) bounds in-session history to fit Opus context (200k tokens).
- **Cross-session:** New session reads previous session file for context (Alex's cached research).
- **Simplicity:** Dispatcher doesn't handle file I/O; Memory Service (Story 4.3) abstracts it.

**Implication:** Session files in `.gitignore`; graceful degradation if write fails (Story 4.6, NFR8).

---

## Epic List

### Epic 1: Project Foundation — "Any Developer Can Understand the Architecture Without Running It"
A hiring manager can clone the repo, read `spec/concierge-spec.md`, scan the README Mermaid graph, and understand the full system architecture before running a single command. `validate_config.py` catches all environment issues before the first LLM call.
**FRs covered:** FR34, FR38, FR41, FR44 (partial)
**NFRs covered:** NFR5, NFR6, NFR7, NFR11, NFR12, NFR13, NFR14, NFR15, NFR16, NFR17

### Epic 2: LangGraph Skeleton & CLI Entry Point — "The Graph Compiles and Starts"
Running `python main.py --user alex` starts without error: graph compiles, entry point is fully wired, `--fast-mode` works, and the fast-mode banner prints. All node delegates exist as one-liner stubs with docstrings.
**FRs covered:** FR7, FR44, FR46, FR47, FR57 (partial)
**NFRs covered:** NFR4, NFR11

### Epic 3: Dispatcher Intelligence & CLI Observability — "Every Routing Decision Prints to the CLI"
Every routing decision prints `[DISPATCHER] intent=X confidence=0.84 → ResearchAgent`. Hybrid routing (Stage 1 rule-based + Stage 2 LLM escalation) is live. `reset_turn_state()` and `trace()` are implemented and unit-tested. Stale-state bug is impossible.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR8, FR29, FR30, FR42, FR48, FR50, FR51, FR53
**NFRs covered:** NFR1, NFR3, NFR8 (partial), NFR9, NFR10

### Epic 4: Memory & Proactive Personalization — "Alex is Greeted Before He Types"
The proactive memory-driven greeting fires before the first user input, proving the JD "proactive outcome completion" requirement in 5 seconds. Memory state is inspectable as a readable JSON file mid-demo.
**FRs covered:** FR16, FR17, FR18, FR19, FR20, FR21, FR31, FR43, FR45, FR49, FR52
**NFRs covered:** NFR8 (complete)

### Epic 5: Knowledge Retrieval & Blended Response — "Two Sources, One Cited Answer"
A user asking about travel destinations receives a blended response attributing results from internal KB (`[RAG]`) and live web search (`[Web]`). Web search failure degrades gracefully to KB-only with a visible label.
**FRs covered:** FR9, FR10, FR11, FR12, FR13, FR14, FR15, FR35, FR54
**NFRs covered:** NFR2

### Epic 6: Governance, Safety & Graph Edges — "The System Knows What It Can't Do"
The system handles ambiguous queries, out-of-scope requests, and booking inquiries gracefully. The Follow-Up Node demonstrates a conditional graph edge. The BookingAgent stub communicates engineering judgment via its Pydantic integration contract.
**FRs covered:** FR22, FR23, FR24, FR25, FR26, FR27, FR28
**NFRs covered:** (none new)

### Epic 7: The Repo Is the Argument — "The Demo Runs Perfectly Every Time"
A hiring manager can run the full pre-validated demo script with confidence. Every Layer 1 (30s README scan) and Layer 2 (3min source reading) artifact is polished. Extensibility is validated by a mocked integration test. `TokenBudgetManager` stub signals production readiness.
**FRs covered:** FR36, FR37, FR39, FR40, FR55, FR56
**NFRs covered:** (none new)

---

## Epic 1: Project Foundation — "Any Developer Can Understand the Architecture Without Running It"

**Goal:** A hiring manager can clone the repo, read `spec/concierge-spec.md`, scan the README Mermaid graph, and understand the full system architecture before running a single command.

**FRs covered:** FR34, FR38, FR41, FR44 (partial)
**NFRs covered:** NFR5, NFR6, NFR7, NFR11, NFR12, NFR13, NFR14, NFR15, NFR16, NFR17

### Story 1.1: Initialize Repo with Git Discipline and Dependency Manifest

As a **developer**, I want the repo initialized with `.gitignore` committed as the first commit and all dependencies exact-pinned in `requirements.txt`, so that sensitive files never appear in git history and the demo is reproducible on any machine.

**Acceptance Criteria:**

- **Given** a fresh `git clone`, **When** I run `git log --oneline`, **Then** the first commit is `.gitignore` with no `.py` files in `agents/`, `nodes/`, or `graph/` present
- **Given** `requirements.txt`, **When** I inspect it, **Then** all dependencies use `==` (not `>=`) and include `langgraph`, `anthropic`, `pydantic`, `duckduckgo-search`, and `pytest`
- **Given** `memory/sessions/` directory, **When** I check `.gitignore`, **Then** `memory/sessions/` is listed and only `.gitkeep` is tracked
- **Given** `.env.example`, **When** I read it, **Then** it documents `ANTHROPIC_API_KEY` without a value and no `.env` file exists in the repo

### Story 1.2: Author `spec/concierge-spec.md` with Full State and Policy Contracts

As a **hiring manager / developer**, I want `spec/concierge-spec.md` committed before any agent implementation files, so that the Git timestamp proves spec-first engineering discipline and the spec serves as the authoritative source of all agent contracts.

**Acceptance Criteria:**

- **Given** `git log --oneline`, **When** I compare timestamps, **Then** `spec/concierge-spec.md` is committed before any `.py` file in `agents/`, `nodes/`, or `graph/`
- **Given** `spec/concierge-spec.md`, **When** I open it, **Then** the first line contains a datestamp and the declaration "written before implementation"
- **Given** the spec file, **When** I read it, **Then** it contains the complete `ConciergeState` TypedDict with all fields (including `error: str | None`), the `AgentPolicy` Pydantic model with all fields, the full graph edge list, and at least one "alternatives considered" note per major decision
- **Given** the spec file, **When** I search for `[TBD]`, **Then** at least 2 markers exist on genuinely uncertain items
- **Given** `README.md`, **When** I read it, **Then** it links `spec/concierge-spec.md` with explicit framing as the authoritative source of agent contracts

### Story 1.3: Scaffold All Prompt YAML Files and Routing Config

As a **developer**, I want all agent `policy.yaml` and `v1.yaml` files scaffolded with the standard 5-section schema and `config/routing_rules.yaml` created with inline comments, so that any contributor can understand every agent's configuration without reading Python source code.

**Acceptance Criteria:**

- **Given** `prompts/` directory, **When** I list it, **Then** 6 subdirectories exist: `dispatcher/`, `rag_agent/`, `research_agent/`, `response_synthesis/`, `guardrail/`, `followup/` — each containing `policy.yaml` and `v1.yaml`
- **Given** any `policy.yaml`, **When** I parse it as `AgentPolicy`, **Then** it contains valid values for `agent_name`, `model`, `prompt_version`, `max_tokens`, `confidence_threshold`, `max_clarifications`, `allowed_tools`
- **Given** any `v1.yaml`, **When** I read it, **Then** it contains all 5 sections: `role`, `context`, `constraints`, `output_format`, `examples` — none empty
- **Given** `prompts/dispatcher/policy.yaml`, **When** I read `max_tokens`, **Then** the value is exactly `128`
- **Given** `config/routing_rules.yaml`, **When** I read it, **Then** every rule has an inline comment explaining its intent, and it contains `escalation_threshold` distinct from any per-agent `confidence_threshold`

### Story 1.4: Implement `validate_config.py` with All 10 Pre-Flight Checks

As a **developer**, I want `validate_config.py` to catch every environment and configuration error before the first LLM call, so that demo setup is self-guiding and never fails silently at runtime.

**Acceptance Criteria:**

- **Given** `validate_config.py`, **When** I call `validate_config.run_checks()` from `main.py`, **Then** all 10 checks run in order before `from graph import compiled_graph`
- **Given** Python < 3.11, **When** `run_checks()` runs, **Then** it exits with a human-readable error before any imports
- **Given** missing or expired `ANTHROPIC_API_KEY`, **When** `run_checks()` runs, **Then** it exits with a specific fix instruction naming the variable
- **Given** a `policy.yaml` with `max_tokens != 128` on the Dispatcher, **When** `run_checks()` runs, **Then** it fails with an explicit message: "Dispatcher max_tokens must be exactly 128"
- **Given** `guardrail.confidence_threshold >= dispatcher.confidence_threshold`, **When** `run_checks()` runs, **Then** it fails with a message explaining the required ordering
- **Given** `python validate_config.py` run standalone, **When** all checks pass, **Then** it prints `[CONFIG OK]` and exits 0
- **Given** multiple failing checks, **When** `run_checks()` runs, **Then** all failures are listed before `sys.exit(1)` — not just the first

### Story 1.5: Create README, ADRs, and `alex.json` as Hiring-Manager-Facing Design Artifacts

As a **hiring manager**, I want the README to lead with a Mermaid agent topology diagram and a JD mapping table, and `memory/profiles/alex.json` to demonstrate the full `UserProfile` schema, so that I can evaluate the architectural judgment in 30 seconds without running any code.

**Acceptance Criteria:**

- **Given** `README.md`, **When** I view the first screen-height, **Then** a Mermaid agent topology diagram and the JD mapping table are both visible before any scrolling
- **Given** the README JD mapping table, **When** I read it, **Then** ≥7 of the 9 MVP items are mapped to specific job description bullets
- **Given** `README.md`, **When** I search for "Navigating This Repo", **Then** a section exists with a 5-step ordered reading path immediately after the Mermaid graph
- **Given** `docs/adr/` directory, **When** I list it, **Then** ADR-001 through ADR-005 exist, each ≤20 lines, each with decision context, options considered, and rationale
- **Given** `memory/profiles/alex.json`, **When** I parse it, **Then** it demonstrates the full `UserProfile` schema including past trips, preferences, a cached research session, and a `_demo_notes` field
- **Given** `memory/README.md`, **When** I read it, **Then** it explains the memory model (profile vs. session, read vs. write) in 3–5 lines

---

## Epic 2: LangGraph Skeleton & CLI Entry Point — "The Graph Compiles and Starts"

**Goal:** Running `python main.py --user alex` starts without error: graph compiles, entry point is fully wired, `--fast-mode` works, and the fast-mode banner prints. All node delegates exist as one-liner stubs with docstrings.

**FRs covered:** FR7, FR44, FR46, FR47, FR57 (partial)
**NFRs covered:** NFR4, NFR11

### Story 2.1: Create `graph/__init__.py` State Initialization and Graph Compilation

As a **developer**, I want `graph/__init__.py` to initialize `ConciergeState` with all default values and compile the graph with all edges, so that the graph is a single importable unit that can be invoked without side effects.

**Acceptance Criteria:**

- **Given** `ConciergeState`, **When** initialized, **Then** all optional fields (e.g., `rag_results`, `error`, `proactive_suggestion`) default to `None` or `[]`
- **Given** `graph/__init__.py`, **When** imported, **Then** `compiled_graph` is returned as the compiled, runnable graph
- **Given** the compiled graph, **When** I inspect it, **Then** all 7 nodes are present and all expected edges (including conditional edges) are wired
- **Given** the graph, **When** I call `compiled_graph.invoke(state)`, **Then** the invocation produces a modified `state` dict with no side effects to the original

### Story 2.2: Build LangGraph StateGraph with All 7 Nodes Wired as Stubs

As a **developer**, I want all 7 LangGraph nodes wired as one-liner stubs that delegate to agent classes, so that the graph compiles and runs end-to-end even before agent logic is implemented.

**Acceptance Criteria:**

- **Given** `graph/__init__.py` from Story 2.1, **When** I wire all 7 nodes, **Then** `compiled_graph` exports without errors
- **Given** `compiled_graph`, **When** I call `compiled_graph.invoke(state)`, **Then** it routes through all 7 nodes in sequence (Dispatcher → RAG/Research/Booking → Guardrail → Response Synthesis → Follow-Up)
- **Given** `nodes/*.py`, **When** I read each file, **Then** it contains a module docstring explaining the agent/node seam and a one-liner function delegating to the corresponding agent class
- **Given** the graph invocation, **When** no error occurs, **Then** `state` is returned unchanged (all agents return state unmodified while stubbed)
- **Given** `state["turn_id"]`, **When** agents are invoked, **Then** all agents receive the same turn_id value without modification

### Story 2.3: Implement `main.py` with Python Version Check and Argument Parsing

As a **developer**, I want `main.py` to assert Python 3.11+, parse `--user` and `--fast-mode` flags, and call `validate_config.run_checks()` before graph import, so that the entry point is self-guiding and catches errors early.

**Acceptance Criteria:**

- **Given** Python < 3.11, **When** I run `python main.py`, **Then** an error prints before any imports: "Python 3.11+ required"
- **Given** `main.py`, **When** I run `python main.py --help`, **Then** output documents `--user` (required) and `--fast-mode` (optional) flags
- **Given** `--user alex`, **When** `main.py` runs, **Then** `state["user_id"] = "alex"` is set before graph invocation
- **Given** `main.py`, **When** `validate_config.run_checks()` is called, **Then** it completes before `from graph import compiled_graph`
- **Given** validation failure, **When** `main.py` runs, **Then** the error from `validate_config` is printed and `sys.exit(1)` is called
- **Given** validation success, **When** `main.py` runs normally, **Then** no visible output until user input is expected

### Story 2.4: Implement `--fast-mode` via Environment Variable and `AgentPolicy.model` Property

As a **developer**, I want `--fast-mode` to set `os.environ["FAST_MODE"] = "1"` and `AgentPolicy.model` to check this env var before returning the configured model, so that lightweight testing is available without code changes.

**Acceptance Criteria:**

- **Given** `python main.py --user alex --fast-mode`, **When** the flag is parsed, **Then** `os.environ["FAST_MODE"]` is set to `"1"` before any `AgentPolicy` instantiation
- **Given** `AgentPolicy.model` as a property, **When** `FAST_MODE` env var is set, **Then** it returns `"claude-haiku-4-5"` regardless of the configured model in `policy.yaml`
- **Given** `AgentPolicy.model` property, **When** `FAST_MODE` is not set, **Then** it returns the value from `policy.yaml` unchanged
- **Given** `--fast-mode` active, **When** the session starts, **Then** a banner prints: `[FAST MODE] Using claude-haiku-4-5 across all agents — not the demo path`
- **Given** `validate_config.py`, **When** `FAST_MODE` env var is set, **Then** the Opus model allow-list check is skipped

---

## Epic 3: Dispatcher Intelligence & CLI Observability — "Every Routing Decision Prints to the CLI"

**Goal:** Every routing decision prints `[DISPATCHER] intent=X confidence=0.84 → ResearchAgent`. Hybrid routing (Stage 1 rule-based + Stage 2 LLM escalation) is live. `reset_turn_state()` and `trace()` are implemented and unit-tested. Stale-state bug is impossible.

**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR8, FR29, FR30, FR42, FR48, FR50, FR51, FR53
**NFRs covered:** NFR1, NFR3, NFR8 (partial), NFR9, NFR10

### Story 3.1: Implement `reset_turn_state()` Helper and Stale-State Unit Test

As a **developer**, I want `reset_turn_state(state)` to explicitly reset all sub-agent fields to `None`/`[]` at turn start, and want a unit test proving that stale data never bleeds across turns, so that the stale-state bug is architecturally impossible.

**Acceptance Criteria:**

- **Given** `agents/dispatcher.py`, **When** I read `reset_turn_state()`, **Then** it resets these fields: `rag_results`, `research_results`, `source_attribution`, `clarification_question`, `proactive_suggestion`, `error`, `human_handoff`, `guardrail_passed`, and all per-turn routing fields
- **Given** `validate_config.py`, **When** I run the static check, **Then** it asserts that every optional `ConciergeState` field appears in `reset_turn_state()`
- **Given** `tests/test_state_reset.py`, **When** I run it, **Then** a test verifies: Turn 1 sets `rag_results = [KB Entry]`, Turn 2 calls `reset_turn_state()`, Turn 2 route check sees `rag_results = None` (no bleed)
- **Given** the stale-state test, **When** it runs, **Then** it passes on 100% of executions (no non-determinism)
- **And** `tests/conftest.py` provides a fixture for a fresh `ConciergeState` dict with all optional fields initialized to `None`

### Story 3.2: Implement Centralized `trace()` Function with Field Allowlist/Denylist

As a **developer**, I want a centralized `trace(node_name, **kwargs)` function that enforces an allowlist of emittable fields and rejects any field containing sensitive data, so that CLI trace output is safe and consistent across all nodes.

**Acceptance Criteria:**

- **Given** the `trace()` function, **When** called with `trace("dispatcher", intent="travel", confidence=0.87)`, **Then** it prints `[dispatcher] intent=travel confidence=0.87`
- **Given** the `trace()` function, **When** called with a denylist field like `trace("dispatcher", current_input="secret")`, **Then** it raises a `ValueError` with message "current_input is not emittable"
- **Given** the denylist, **When** I inspect it, **Then** it includes: `current_input`, `memory_profile`, `conversation_history`, `rag_results`, `research_results`, any field containing API keys
- **Given** the allowlist, **When** I inspect it, **Then** it includes: `intent`, `confidence`, `route`, `model`, `session_id`, `turn_id`, and outcome-oriented fields
- **Given** `nodes/*.py`, **When** I search for trace calls, **Then** every node calls `trace()` exactly once at start, never with ad-hoc f-strings
- **And** `tests/test_trace.py` validates that denylist fields raise `ValueError` on any trace attempt

### Story 3.3: Implement Stage 1 Rule-Based Pre-Filter Routing

As a **developer**, I want the Dispatcher's Stage 1 to load `routing_rules.yaml`, keyword-match user input, and route directly if confidence ≥ `escalation_threshold`, so that deterministic intents don't waste LLM budget.

**Acceptance Criteria:**

- **Given** `routing_rules.yaml`, **When** loaded at startup, **Then** it parses as a valid rule list with fields: `intent`, `keywords`, `confidence`
- **Given** user input "I want to book a flight", **When** Stage 1 checks rules, **Then** keyword "book" matches `booking_intent` rule with confidence 0.95
- **Given** confidence 0.95 and `escalation_threshold=0.70`, **When** Stage 1 runs, **Then** it returns `route="booking_agent"` without invoking an LLM
- **Given** user input "something else", **When** no rule keyword matches, **Then** confidence is 0 and routing escalates to Stage 2 (LLM)
- **Given** Stage 1 routing, **When** it routes directly, **Then** `trace("dispatcher", intent=X, confidence=0.95, stage="pre_filter")` is called (no LLM marker printed)
- **And** `config/routing_rules.yaml` contains inline comments explaining every rule's purpose

### Story 3.4: Implement Stage 2 LLM-Based Escalation and Intent Classification

As a **developer**, I want the Dispatcher's Stage 2 to invoke Claude for ambiguous intents, parse structured routing output (intent + confidence), and decide whether to route or escalate to Guardrail, so that hybrid routing works.

**Acceptance Criteria:**

- **Given** user input with low confidence from Stage 1, **When** Stage 2 runs, **Then** `anthropic.Anthropic().messages.create()` is called with the configured Dispatcher model
- **Given** the Dispatcher prompt, **When** I read `prompts/dispatcher/v1.yaml`, **Then** it contains explicit instruction: return JSON with `intent` and `confidence` fields only
- **Given** LLM response `{"intent": "destination_research", "confidence": 0.84}`, **When** parsed, **Then** `state["intent"]` and `state["confidence"]` are set
- **Given** confidence 0.84 and `confidence_threshold=0.75`, **When** Stage 2 completes, **Then** `route="research_agent"` is set
- **Given** confidence 0.61 (below threshold), **When** Stage 2 completes, **Then** `route="guardrail"` is set (triggers clarifying question)
- **Given** Stage 2 routing, **When** it completes, **Then** `trace("dispatcher", intent=X, confidence=Y, stage="llm_escalation")` is called

### Story 3.5: Orchestrate Full Dispatcher: Both Stages, Routing Decision, History Management

As a **developer**, I want the Dispatcher to own the full conversation history, call both Stage 1 and Stage 2 in sequence, emit a structured routing decision, and never generate user-facing responses, so that the routing intelligence is the architectural centerpiece.

**Acceptance Criteria:**

- **Given** `agents/dispatcher.py`, **When** `dispatcher.run(state)` is called, **Then** it: (1) calls `reset_turn_state(state)`, (2) appends user input to `conversation_history`, (3) tries Stage 1, (4) escalates to Stage 2 if needed, (5) sets `state["route"]` and `state["current_response"] = None`
- **Given** a multi-turn conversation, **When** the Dispatcher checks `conversation_history`, **Then** it contains all previous turns verbatim (full session history owned by Dispatcher, not sub-agents)
- **Given** `state["route"]` set to a valid agent name, **When** the graph routes, **Then** the corresponding agent node is invoked
- **Given** the Dispatcher, **When** it completes, **Then** `state["current_response"]` remains `None` (Dispatcher never generates user-facing responses)
- **Given** the Dispatcher at the end of a turn, **When** I check trace output, **Then** exactly one `[dispatcher]` trace line was printed with `intent`, `confidence`, and `route` fields
- **Given** Stage 1 confidence ≥ `escalation_threshold` (0.70), **When** Dispatcher runs, **Then** it routes directly to the matched agent and skips Stage 2 LLM call
- **Given** Stage 1 confidence < `escalation_threshold`, **When** Dispatcher escalates to Stage 2, **Then** Stage 2 LLM result is evaluated; if Stage 2 confidence ≥ `confidence_threshold` (0.75), route to agent; else route to Guardrail for clarification
- **And** the Dispatcher respects `max_tokens=128` constraint (output capped to routing decision only)

### Story 3.6: Implement Error Handling at Node Boundary with Actionable Messages

As a **developer**, I want every node to catch LLM API errors, set `state["error"]` to an actionable message, set `state["human_handoff"] = True`, and return state without raising exceptions, so that the demo never crashes and the user always gets a helpful message.

**Acceptance Criteria:**

- **Given** an Anthropic API timeout in the Dispatcher, **When** the node catches it, **Then** `state["error"] = "LLM connection timeout. Please try again."` (no raw stack trace)
- **Given** a missing or invalid API key, **When** caught, **Then** `state["error"]` contains the exact fix: "ANTHROPIC_API_KEY not set or invalid"
- **Given** any node catching an exception, **When** it returns, **Then** the graph edge routing is NOT interrupted — the graph continues and the terminal response node reads `state["error"]` to emit the message to the user
- **Given** the error path, **When** trace is printed, **Then** the catching node still prints its `[NODE_NAME]` trace entry before exiting (trace completeness guaranteed)
- **Given** `state["human_handoff"] = True`, **When** the graph reaches the terminal response node, **Then** the user-facing message ends with "A human travel specialist can help — please wait"

### Story 3.7: Implement Per-Turn Data Guarantee and Conversation History Ownership

As a **developer**, I want the Dispatcher to guarantee that all agents in a turn operate on current-turn data (no stale sub-agent results from prior turns), and that the full conversation history is persisted independently of LLM context windows, so that session continuity is reliable.

**Acceptance Criteria:**

- **Given** Turn 2 of a conversation, **When** the Dispatcher calls `reset_turn_state()`, **Then** all sub-agent fields from Turn 1 are reset to `None`
- **Given** Turn 2 routing to RAG Agent, **When** RAG Agent receives state, **Then** `state["rag_results"] = None` (guaranteed fresh, not Turn 1 stale data)
- **Given** `state["conversation_history"]`, **When** I inspect it at the end of Turn N, **Then** it contains all N turns verbatim (complete session history independent of LLM context window)
- **Given** the Dispatcher managing history, **When** it receives a new user message in Turn N+1, **Then** the message is appended to `conversation_history` before any routing decision is made
- **And** NFR3 is met: dispatch loop overhead (reset + routing decision emission) is < 2s per turn, excluding LLM API latency

---

## Epic 4: Memory & Proactive Personalization — "Alex is Greeted Before He Types"

**Goal:** The proactive memory-driven greeting fires before the first user input, proving the JD "proactive outcome completion" requirement in 5 seconds. Memory state is inspectable as a readable JSON file mid-demo.

**FRs covered:** FR16, FR17, FR18, FR19, FR20, FR21, FR31, FR43, FR45, FR49, FR52
**NFRs covered:** NFR8 (complete)

### Story 4.1: Implement Memory Service Profile Loader at Session Start

As a **developer**, I want the Memory Service to load a user profile from `memory/profiles/{user_id}.json` at session start using paths resolved relative to `Path(__file__).parent`, so that user context is available before any agent logic runs.

**Acceptance Criteria:**

- **Given** `memory/profiles/alex.json` exists, **When** the session starts with `--user alex`, **Then** `state["memory_profile"]` is populated with the full profile (not `None`)
- **Given** the Memory Service, **When** it loads the profile, **Then** it uses `Path(__file__).parent` to resolve paths (not CWD), working correctly even if `python main.py` is run from a different directory
- **Given** a profile missing, **When** the session starts, **Then** `state["memory_profile"] = None` (no crash, no exception)
- **Given** a profile missing, **When** it occurs, **Then** a visible warning is emitted: `[MEMORY] Profile for {user_id} not found — starting fresh session`
- **Given** `memory/profiles/alex.json`, **When** I parse it, **Then** it contains fields: `user_id`, `past_trips`, `preferences`, `cached_research_session`, `last_seen`

### Story 4.2: Implement Proactive Memory-Driven Greeting Before First User Input

As a **developer**, I want the system to generate and print a proactive greeting from the loaded profile before the user types anything, so that the hiring manager sees the "proactive outcome completion" JD requirement fire automatically in the first 5 seconds.

**Acceptance Criteria:**

- **Given** a loaded profile for Alex with past trips including "Bali" and "Tokyo", **When** the session starts, **Then** a greeting is printed BEFORE any user input prompt: `Welcome back, Alex. Based on your March trip to Bali, you might be interested in upcoming deals to Southeast Asia.`
- **Given** the proactive greeting, **When** it fires, **Then** it's printed immediately after the session banner (if `--fast-mode` applies)
- **Given** no profile loaded (Story 4.1 error case), **When** the session starts, **Then** NO proactive greeting is printed — the visible warning from Story 4.1 fires instead, and the user is simply prompted for input (no silent failure)
- **Given** the greeting text, **When** I inspect it, **Then** it references actual profile data (past trip names, dates) — not generic placeholder text
- **Given** the greeting, **When** it's generated, **Then** `trace("memory", event="greeting_fired", user_id="alex")` is called

### Story 4.3: Implement Session File Write at Session Exit

As a **developer**, I want the Memory Service to write the full conversation state to `memory/sessions/{session_id}.json` when the user exits, so that session continuity is preserved across runs.

**Acceptance Criteria:**

- **Given** a completed session, **When** the user exits (CTRL+C or natural end), **Then** `memory/sessions/{session_id}/state.json` is written
- **Given** the session file, **When** I parse it, **Then** it contains: `session_id`, `user_id`, `timestamp_start`, `timestamp_end`, `conversation_history` (all turns), `turn_count`
- **Given** a new session for the same user, **When** it starts, **Then** the greeting can reference `cached_research_session` from the previous session written to `memory/sessions/`
- **Given** the session directory, **When** I list `memory/sessions/`, **Then** each session has a unique `session_id` subdirectory with readable JSON
- **Given** memory paths, **When** resolved, **Then** `Path(__file__).parent` is used (not CWD), working from any directory
- **And** `validate_config.py` asserts that `memory/sessions/` is listed in `.gitignore` (no session files committed)

### Story 4.4: Implement Fresh Session Fallback (No Profile, No Crash)

As a **developer**, I want the system to gracefully handle missing profiles without crashing, emitting a visible warning and continuing with a fresh session, so that the demo is resilient.

**Acceptance Criteria:**

- **Given** `--user unknown_user` with no profile file, **When** the session starts, **Then** the Memory Service catches the missing file and sets `state["memory_profile"] = None`
- **Given** the missing profile, **When** it occurs, **Then** a warning is printed: `[MEMORY] Profile for unknown_user not found — starting fresh session`
- **Given** no profile loaded, **When** the session proceeds, **Then** the user is prompted for input and the system works normally (no personalization, but fully functional)
- **Given** a malformed JSON file in `memory/profiles/`, **When** it's loaded, **Then** it's caught as a `JSONDecodeError`, a warning is printed, and `state["memory_profile"] = None`
- **And** no exception escapes to `main.py` — all errors are caught and handled at the Memory Service boundary

### Story 4.5: Implement Memory Service Trace Output with Profile Metadata

As a **developer**, I want the Memory Service to emit structured trace entries when loading and writing profiles, so that session boundaries are observable in the CLI output.

**Acceptance Criteria:**

- **Given** profile load at session start, **When** it occurs, **Then** `trace("memory", event="profile_loaded", user_id="alex", past_trips_count=2)` is called
- **Given** session write at exit, **When** it occurs, **Then** `trace("memory", event="session_written", session_id=X, turn_count=N)` is called
- **Given** profile not found, **When** it occurs, **Then** `trace("memory", event="profile_not_found", user_id=X)` is called
- **Given** trace output, **When** I inspect it, **Then** it follows the `[memory]` bracket-label convention with outcome-oriented fields (no sensitive data leaked)

### Story 4.6: Implement Dual-Store Architecture (In-Session State + Persisted File)

As a **developer**, I want conversation history to be stored in two places (in-session `ConciergeState` for active routing + persisted `memory/sessions/{session_id}.json` for cross-session continuity), so that session context is never lost even if the process crashes.

**Acceptance Criteria:**

- **Given** active session, **When** I inspect `state["conversation_history"]`, **Then** it contains all turns in memory for LLM context window management
- **Given** session write, **When** it occurs at exit, **Then** the full `conversation_history` is appended to `memory/sessions/{session_id}.json`
- **Given** a new session for the same user, **When** it starts, **Then** the greeting can read `memory/sessions/{previous_session_id}/state.json` to access `cached_research_session` or other context
- **Given** `state["conversation_history"]` vs. the persisted file, **When** I compare them, **Then** the persisted file is the authoritative long-term record independent of in-memory state
- **Given** NFR8 graceful degradation, **When** session write fails (disk full, permissions), **Then** `state["human_handoff"] = True` and the user is notified: "Session could not be saved — a human can assist"
- **And** the in-session routing continues (degradation, not crash)

---

## Epic 5: Knowledge Retrieval & Blended Response — "Two Sources, One Cited Answer"

**Goal:** A user asking about travel destinations receives a blended response attributing results from internal KB (`[RAG]`) and live web search (`[Web]`). Web search failure degrades gracefully to KB-only with a visible label.

**FRs covered:** FR9, FR10, FR11, FR12, FR13, FR14, FR15, FR35, FR54
**NFRs covered:** NFR2

### Story 5.1: Create Mock JSON Knowledge Base with Production Swap-Point Comments

As a **developer**, I want a mock JSON Knowledge Base containing 5–10 travel destinations with production swap-point comments, so that RAG Agent has structured data to retrieve from and future developers see exactly where to swap in AWS Bedrock.

**Acceptance Criteria:**

- **Given** `agents/kb/knowledge_base.json`, **When** I parse it, **Then** it contains an array of destination objects with fields: `id`, `name`, `region`, `description`, `amenities`, `pricing`
- **Given** the KB, **When** I read it, **Then** it includes ≥5 real destinations (e.g., Bali, Phuket, Koh Samui, Tokyo, Bangkok) with substantive descriptions (≥3 sentences each)
- **Given** the KB, **When** I search for "Production swap point", **Then** a comment exists: `# Production swap point: replace MockKnowledgeBase with BedrockKnowledgeBase(kb_id=os.getenv("BEDROCK_KB_ID"))`
- **Given** the mock KB, **When** RAG Agent queries it, **Then** keyword matching works: "beach" returns Bali/Phuket, "city" returns Tokyo/Bangkok
- **And** the KB structure is self-documenting: a new developer can add a destination by copying an existing entry without reading code

### Story 5.2: Implement RAG Agent to Retrieve from Mock JSON KB

As a **developer**, I want the RAG Agent to load the JSON KB, keyword-match the user query, and return relevant entries as `state["rag_results"]`, so that Knowledge Retrieval routing produces structured, inspectable results.

**Acceptance Criteria:**

- **Given** user query "Best beach destinations in Southeast Asia", **When** RAG Agent runs, **Then** it queries the KB and returns entries where region="Southeast Asia" and amenities include "beach"
- **Given** the RAG Agent, **When** `agents/rag_agent.py` is implemented, **Then** it receives only the current user query (FR14: scoped context, not full conversation history)
- **Given** the RAG Agent, **When** it completes, **Then** `state["rag_results"]` is populated with a list of KB entries and `trace("rag_agent", event="retrieval_complete", results_count=N)` is called
- **Given** the RAG Agent, **When** it queries the KB, **Then** per-agent `max_tokens` is enforced before any LLM call (if RAG uses LLM ranking)
- **Given** no matching KB entries, **When** it occurs, **Then** `state["rag_results"] = []` (empty list, not `None`) and a fallback message is prepared

### Story 5.3: Implement Research Agent with DuckDuckGo Web Search

As a **developer**, I want the Research Agent to call DuckDuckGo search API, parse results, and return them as `state["research_results"]`, so that live web search augments KB-only answers.

**Acceptance Criteria:**

- **Given** user query "latest travel trends to Southeast Asia", **When** Research Agent runs, **Then** it calls DuckDuckGo search with the query
- **Given** DuckDuckGo results, **When** they're returned, **Then** the agent parses them into a list with fields: `title`, `link`, `snippet`
- **Given** the Research Agent, **When** it completes, **Then** `state["research_results"]` is populated and `trace("research_agent", event="search_complete", results_count=N)` is called
- **Given** the Research Agent, **When** it receives state, **Then** it operates on scoped context only (current query + last 3 turns max, not full conversation history) — FR14
- **Given** the Research Agent, **When** results are returned, **Then** per-agent `max_tokens` is enforced before LLM-based result ranking/synthesis
- **Given** DuckDuckGo success, **When** results are available, **Then** at least 3 results are returned (or fewer if search returns fewer)

### Story 5.4: Implement Graceful Degradation When Web Search Unavailable

As a **developer**, I want the system to degrade gracefully when DuckDuckGo is unavailable or rate-limited, falling back to KB-only results with a visible label, so that the demo doesn't fail on network issues.

**Acceptance Criteria:**

- **Given** DuckDuckGo timeout or rate limit, **When** Research Agent catches the error, **Then** it sets `state["research_results"] = []` and `state["degradation_label"] = "[WEB SEARCH UNAVAILABLE — serving from internal KB only]"`
- **Given** degradation, **When** it occurs, **Then** the error is caught at the Research Agent node boundary — no exception escapes to graph routing
- **Given** `state["degradation_label"]` set, **When** Response Synthesis runs, **Then** it includes the label in the final response if only KB results are being cited
- **And** `trace("research_agent", event="search_unavailable", reason="timeout")` is called
- **Given** graceful degradation, **When** the user sees the response, **Then** they understand why only internal KB results are shown — the label is clear and helpful

### Story 5.5: Implement Response Synthesis with Blended Output and Inline Source Attribution

As a **developer**, I want Response Synthesis to merge RAG and Research results, generate a blended answer, and inline source tags (`[RAG]` vs `[Web]`), so that the hiring manager sees sophisticated result synthesis in action.

**Acceptance Criteria:**

- **Given** both `state["rag_results"]` and `state["research_results"]` populated, **When** Response Synthesis runs, **Then** it generates a blended response citing both sources: `"Based on our current offerings [RAG] and latest travel trends [Web], here are the top 3 Southeast Asian destinations..."`
- **Given** the blended response, **When** it's generated, **Then** `state["source_attribution"]` is populated with: `["[RAG] Bali — internal KB entry", "[Web] Latest Bali travel trends from travel blogs"]`
- **Given** `role: system_summary` messages in `conversation_history`, **When** Response Synthesis generates output, **Then** it filters them out before passing to the LLM (FR27 complement)
- **Given** only RAG results available (no web search), **When** Response Synthesis runs, **Then** it still generates a complete response, tagging sources as `[RAG]` only
- **Given** the final response, **When** I read it, **Then** sources are consistently tagged and distinguishable: `[RAG]` vs `[Web]`
- **Given** BookingAgent stub response (Pydantic model), **When** Response Synthesis receives it, **Then** it formats the message field for user display without crashing — agent type determines response format (retrieval vs. stub)
- **And** `trace("response_synthesis", event="synthesis_complete", sources_cited=2)` is called

### Story 5.6: Enforce Per-Agent `max_tokens` Output Limit Before Each LLM Call

As a **developer**, I want the system to enforce per-agent `max_tokens` from `AgentPolicy` before any LLM call, so that token budgets are predictable and Dispatcher's 128-token cap is honored.

**Acceptance Criteria:**

- **Given** `prompts/dispatcher/policy.yaml` with `max_tokens: 128`, **When** the Dispatcher is invoked, **Then** the LLM call includes `max_tokens=128` parameter
- **Given** `prompts/rag_agent/policy.yaml` with `max_tokens: 512`, **When** RAG Agent runs, **Then** if it calls an LLM for ranking, `max_tokens=512` is enforced
- **Given** `prompts/research_agent/policy.yaml` with `max_tokens: 1024`, **When** Research Agent synthesis happens, **Then** `max_tokens=1024` is used
- **Given** any agent, **When** I inspect `agents/*/agent_class.py`, **Then** the LLM call reads `policy.max_tokens` and passes it to `anthropic.Anthropic().messages.create(max_tokens=...)`
- **Given** a misconfigured `max_tokens` value, **When** `validate_config.py` runs, **Then** it flags invalid or missing values before the first LLM call
- **And** the Dispatcher's 128-token cap (load-bearing for routing integrity) is explicitly validated in `validate_config.py`

---

## Epic 6: Governance, Safety & Graph Edges — "The System Knows What It Can't Do"

**Goal:** The system handles ambiguous queries, out-of-scope requests, and booking inquiries gracefully. The Follow-Up Node demonstrates a conditional graph edge. The BookingAgent stub communicates engineering judgment via its Pydantic integration contract.

**FRs covered:** FR22, FR23, FR24, FR25, FR26, FR27, FR28
**NFRs covered:** (none new)

### Story 6.1: Implement Guardrail Node with Confidence Threshold Check and Clarifying Question

As a **developer**, I want the Guardrail node to check if Dispatcher confidence is below `confidence_threshold`, and if so, emit a single clarifying question to the user, so that ambiguous intents are resolved before routing to a sub-agent.

**Acceptance Criteria:**

- **Given** Dispatcher confidence 0.61 with `confidence_threshold=0.75`, **When** Guardrail runs, **Then** it sets `state["clarification_needed"] = True`
- **Given** clarification needed, **When** Guardrail generates a question, **Then** it's stored in `state["clarification_question"]` and printed to the user: `"Of course — are you looking to research a destination, check on a booking, or something else?"`
- **Given** the clarifying question, **When** it's posed, **Then** exactly ONE question is asked (not multiple), and the user's response is appended to `conversation_history` on the next turn
- **Given** the user provides clarification, **When** the next turn runs, **Then** the Dispatcher re-classifies with the clarified context (intent confidence likely increases)
- **And** `trace("guardrail", event="clarification_fired", confidence=0.61, threshold=0.75)` is called

### Story 6.2: Implement Out-of-Domain Detection and Deflection

As a **developer**, I want the Guardrail node to detect when a query is completely out-of-domain (e.g., "What's the weather in London?"), classify it with low confidence, and return a labeled deflection response, so that the user understands the system's boundaries gracefully.

**Acceptance Criteria:**

- **Given** user query "What's the weather in London?", **When** Guardrail classifies it, **Then** it detects out-of-domain intent (confidence < 0.4 after LLM pass)
- **Given** out-of-domain detection, **When** it occurs, **Then** `state["guardrail_passed"] = False` and a deflection response is prepared: `"I specialize in travel planning and concierge services. For weather, I'd suggest a weather service — but I can tell you the best time of year to visit London if that helps."`
- **Given** the deflection, **When** it's emitted, **Then** it's friendly and offers an alternative (not just a blunt rejection)
- **And** `trace("guardrail", event="out_of_domain", confidence=0.32, query="weather london")` is called
- **Given** the deflection response, **When** it's printed to the user, **Then** the session does NOT end — the user can continue with travel-related queries

### Story 6.3: Implement Human Handoff After Max Clarification Attempts

As a **developer**, I want the system to track clarification attempts per session and route to human handoff when the limit is exceeded, so that users stuck in clarification loops get escalated to human support gracefully.

**Acceptance Criteria:**

- **Given** `AgentPolicy.max_clarifications=3` for the Guardrail, **When** 3 clarifying questions have been asked in a session without resolving the intent, **Then** `state["human_handoff"] = True`
- **Given** human handoff triggered, **When** the next response is generated, **Then** the terminal response message ends with: `"I'm having trouble understanding your request. A human travel specialist can assist — please wait or contact support."`
- **Given** the human handoff, **When** it occurs, **Then** the session does NOT crash or terminate — it ends gracefully with a help message
- **And** `trace("guardrail", event="human_handoff", clarification_count=3, session_id=X)` is called
- **Given** a session with clarifications, **When** I inspect `state["max_clarifications"]`, **Then** it's read from the Guardrail's `AgentPolicy`

### Story 6.4: Implement BookingAgent Stub with `BookingAgentResponse` Pydantic Model

As a **developer**, I want the BookingAgent stub to return a `BookingAgentResponse` Pydantic model (not a bare string), exposing an integration contract and documenting the swap-point to a real booking service, so that the stub communicates engineering judgment.

**Acceptance Criteria:**

- **Given** `agents/booking_agent.py`, **When** I read it, **Then** `BookingAgentResponse` is defined as a Pydantic model with fields: `status`, `message`, `integration_point`, `required_env_vars`
- **Given** user query "Can you book me a flight to Bali?", **When** BookingAgent runs, **Then** it returns: `BookingAgentResponse(status="unavailable", message="Booking is not available in this version. A human travel specialist can assist — shall I connect you?", integration_point="Replace with BedrockBookingAPI(region=X, api_key=...)", required_env_vars=["BOOKING_API_KEY", "BOOKING_REGION"])`
- **Given** the stub response, **When** it's parsed, **Then** the message is clear and helpful (not cryptic), and the integration contract is visible in the Response Synthesis output
- **Given** the `integration_point` field, **When** a future developer reads it, **Then** they have explicit guidance on how to wire a real booking service (no guessing required)
- **And** `trace("booking_agent", event="unavailable", message="stub_integration_contract")` is called

### Story 6.5: Implement Follow-Up Node with Conditional Graph Edge

As a **developer**, I want the Follow-Up node to run conditionally AFTER Research Agent completes (not after RAG), so that proactive suggestions are offered when research-driven answers are delivered, demonstrating LangGraph's conditional edge capability.

**Acceptance Criteria:**

- **Given** Dispatcher routed to Research Agent, **When** Research Agent completes, **Then** the graph edge routes to Follow-Up node (conditional check: `route == "research_agent"`)
- **Given** Dispatcher routed to RAG Agent or other agents, **When** they complete, **Then** the graph skips Follow-Up and routes directly to Response Synthesis
- **Given** Follow-Up node triggered, **When** it runs, **Then** it generates a proactive suggestion: `"Based on your interest in Southeast Asia, you might also want to explore mountain retreats. Should I research that for you?"`
- **Given** the Follow-Up suggestion, **When** it's added to state, **Then** `state["proactive_suggestion"]` is set and `trace("followup", event="suggestion_generated")` is called
- **And** the conditional edge in `graph/__init__.py` is documented with a comment explaining why Follow-Up runs only after Research Agent (demonstrates architectural judgment)

### Story 6.6: Implement `system_summary` Message Filtering in Response Synthesis

As a **developer**, I want Response Synthesis to filter out `role: system_summary` messages from `conversation_history` before passing to the LLM, so that internal memory management messages never leak into user-facing responses.

**Acceptance Criteria:**

- **Given** `conversation_history` containing messages with `role: "system_summary"`, **When** Response Synthesis generates output, **Then** it creates a filtered copy excluding all `role == "system_summary"` messages
- **Given** the filtered history, **When** it's passed to the LLM, **Then** only user/assistant messages are included (summary messages never appear in prompts)
- **Given** the final response generated, **When** it's returned, **Then** no `[SUMMARY]` markers or summary content appear in the user-facing message
- **And** the filtering is done per-turn (a summary created in Turn 5 doesn't affect Turn 6 filtering)

---

## Epic 7: The Repo Is the Argument — "The Demo Runs Perfectly Every Time"

**Goal:** A hiring manager can run the full pre-validated demo script with confidence. Every Layer 1 (30s README scan) and Layer 2 (3min source reading) artifact is polished. Extensibility is validated by a mocked integration test. `TokenBudgetManager` stub signals production readiness.

**FRs covered:** FR36, FR37, FR39, FR40, FR55, FR56
**NFRs covered:** (none new)

### Story 7.1: Implement `TokenBudgetManager` Stub with Activation Threshold Comment

As a **developer**, I want the `TokenBudgetManager` stub to declare the activation threshold explicitly in a code comment, so that the stub communicates production-readiness and sets expectations for future implementation.

**Acceptance Criteria:**

- **Given** `agents/token_budget_manager.py`, **When** I read it, **Then** it contains a `TokenBudgetManager` class with a `check_and_summarize(history: list[Message]) -> list[Message]` method
- **Given** the stub, **When** I read the docstring/comment, **Then** it states: `# Stub implementation. In production, summarize when token count exceeds 6000 (leaving 2000 for output). Activation threshold: 80% of model context window.`
- **Given** the stub method, **When** called, **Then** it returns the history unchanged (no-op in MVP), but the interface and activation threshold are documented
- **And** a `@property` in the method reads from config (deferred to future) or a hardcoded threshold marked with `# TODO: make configurable`

### Story 7.2: Implement Token Limit Detection and Turn Compression Logic (Stub)

As a **developer**, I want the system to detect when conversation context approaches the token limit, and have a documented path to compress oldest turns using `TokenBudgetManager`, so that production scalability is architecturally clear even if not fully implemented in MVP.

**Acceptance Criteria:**

- **Given** `agents/dispatcher.py`, **When** the Dispatcher calls `TokenBudgetManager.check_and_summarize()` before LLM invocation, **Then** the call checks if `len(conversation_history)` approaches a threshold (documented threshold: 80% of context window)
- **Given** the stub in MVP, **When** the threshold is approached, **Then** it logs: `[TOKEN_BUDGET] Context approaching limit. In production, oldest turns would be summarized here.`
- **Given** the compression logic, **When** triggered, **Then** `role: system_summary` messages are created (for Response Synthesis to filter), preserving key facts but reducing token count
- **And** `trace("token_budget", event="check_performed", token_count=X, threshold=6000)` is called

### Story 7.3: Create Demo Script with Pre-Validated Queries and Expected Routing Paths

As a **developer**, I want a documented demo script containing 5 pre-validated user queries with expected routing outcomes, so that a hiring manager can run the demo with confidence and validate that the system behaves as expected.

**Acceptance Criteria:**

- **Given** `demo_script.md`, **When** I read it, **Then** it contains 5 queries in order, each with: (1) the query text, (2) expected intent from Stage 1 or Stage 2, (3) expected confidence, (4) expected routing destination (e.g., `research_agent`)
- **Given** Query 1: `"I'm thinking Southeast Asia but not sure where"`, **When** I run it, **Then** Dispatcher routes to Research Agent (confidence 0.84), and the demo output shows exactly that
- **Given** Query 2: `"What about the Wyndham property in Phuket?"`, **When** I run it, **Then** Dispatcher routes to RAG Agent (confidence 0.91 from Stage 1 keyword match on "property")
- **Given** Query 3: `"Can you help me?"` (ambiguous), **When** I run it, **Then** Dispatcher confidence < 0.75, Guardrail fires with clarifying question
- **Given** Query 4: `"What's the weather?"` (out-of-domain), **When** I run it, **Then** Guardrail detects out-of-domain and returns deflection
- **Given** Query 5: `"Book me a flight"`, **When** I run it, **Then** Dispatcher routes to BookingAgent, stub returns availability message
- **And** each expected routing is pre-validated against actual Stage 1 `routing_rules.yaml` scores before the demo script is finalized
- **IMPORTANT NOTE:** Queries 2, 5 route via Stage 1 (deterministic). Queries 1, 3, 4 depend on LLM Stage 2 escalation (non-deterministic). Demo script should document: "Stage 2 routing may vary ±0.05 confidence; expected range provided. Pre-validate actual confidence scores before demo."

### Story 7.4: Implement New Agent Extension Validation Test (Extensibility for FR36)

As a **developer**, I want a mocked integration test that validates a new agent can be added with zero Dispatcher changes, so that extensibility is proven and future contributors trust the architecture.

**Acceptance Criteria:**

- **Given** `tests/test_new_agent_extension.py`, **When** I run it, **Then** a mocked test adds a hypothetical `hotel_agent` to the graph
- **Given** the extension test, **When** it adds the agent, **Then** it: (1) creates `prompts/hotel_agent/policy.yaml`, (2) creates a mock `agents/hotel_agent.py` class, (3) wires one `add_node` in graph, (4) routes to it via Dispatcher
- **Given** the routing, **When** user query matches "hotel", **Then** Dispatcher routes to `hotel_agent` without any Dispatcher code changes
- **Given** the test, **When** it passes, **Then** it proves FR36: adding a new agent requires new YAML + new node only, no Dispatcher rewrite
- **And** the test is documented with a comment: `# This test proves extensibility. In production, follow these exact steps to add a new agent.`

### Story 7.5: Implement Prompt Versioning Demonstration (Extensibility for FR37)

As a **developer**, I want the system to support prompt versioning without code changes, so that a contributor can change `prompt_version: v1` → `v2` in YAML and the system automatically picks up the new prompt.

**Acceptance Criteria:**

- **Given** `prompts/dispatcher/policy.yaml`, **When** I change `prompt_version: v1` to `v2`, **Then** the system loads `prompts/dispatcher/v2.yaml` instead
- **Given** `AgentPolicy.prompt_version` as a field, **When** agents are instantiated, **Then** they read this value and load the corresponding prompt file dynamically
- **Given** a missing `v2.yaml`, **When** it's referenced, **Then** `validate_config.py` catches it at startup with an actionable error: "prompts/dispatcher/v2.yaml not found"
- **And** `tests/test_prompt_versioning.py` validates that bumping version loads the correct prompt file without code changes

### Story 7.6: Polish All Layer 1 and Layer 2 Artifacts and Document Profile Reset

As a **developer**, I want every artifact visible to a hiring manager (README, ADRs, memory profile) to be polished and self-documenting, and the profile reset command to be clearly documented, so that the demo is flawless.

**Acceptance Criteria:**

- **Given** the README, **When** I read it, **Then** it contains: (1) Mermaid topology diagram at the top, (2) JD mapping table below it, (3) "Navigating This Repo" section with 5-step reading path, (4) quick-start command, (5) demo script reference, (6) link to `spec/concierge-spec.md`
- **Given** `docs/adr/001-context-window-ownership.md`, **When** I read it, **Then** it's ≤20 lines, has decision context, options considered, and rationale — no fluff
- **Given** `memory/profiles/alex.json`, **When** I parse it, **Then** it has a `_demo_notes` field explaining the test scenario
- **Given** the profile reset command, **When** documented in README, **Then** it states: `git checkout -- memory/profiles/alex.json` to restore the pre-seeded state
- **And** `memory/README.md` explains the memory model (profile vs. session distinction) in 3–5 lines
- **Given** all Layer 2 artifacts (source files), **When** a developer reads them, **Then** every production swap-point is a readable design statement (e.g., Bedrock KB swap point is clear)
