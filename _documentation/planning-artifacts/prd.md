---
stepsCompleted: [step-01-init, step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish]
classification:
  projectType: api_backend
  domain: scientific_ai
  complexity: medium
  projectContext: greenfield
inputDocuments:
  - _bmad-output/brainstorming/brainstorming-session-2026-02-25.md
workflowType: 'prd'
briefCount: 0
researchCount: 0
brainstormingCount: 1
projectDocsCount: 0
---

# Product Requirements Document - TNL-HELP

**Author:** Andrey
**Date:** 2026-02-25

## Executive Summary

A LangGraph-based multi-agent AI Concierge MVP demonstrating that a senior AI engineer can translate a business requirement into a governed, traceable, production-quality multi-agent flow — without losing either the business logic or the engineering discipline. The primary user is a hiring manager evaluating the AI-Native Developer / Client Concierge role. The travel/hospitality domain (Club Wyndham, from TNL-HELP production experience) provides the business case wrapper. The repo itself is the deliverable — a structured argument, in running code, for why Andrey should be hired.

The system architecture: `Client → Dispatcher → [RAG Agent | Research Agent | Fallback] → Guardrail → Response`. A pre-seeded "Alex" persona makes personalization visible from the first CLI invocation (`python main.py --user alex`). A CLI trace logs every routing decision in real time. No UI, no cloud infrastructure — complexity is architectural, not operational.

### What Makes This Special

Three things a LangGraph weekend reader cannot replicate:

1. **Production-pattern fidelity.** Prompt orchestration in `prompts/{agent}/{version}.yaml`, guardrail patterns, and architectural commentary directly adapted from TNL-HELP Bedrock + LangGraph production systems. The sophistication is visible in file structure and code comments, not just in the graph.

2. **Spec-driven architecture.** `TypedDict` state schema covers all agent handoffs. `AgentPolicy` (Pydantic) defines `allowed_tools`, `confidence_threshold`, `max_clarifications` per agent. The spec is executable — it IS the graph, not documentation about the graph.

3. **Honest stubs as architectural statements.** The `BookingAgent` stub with an integration contract comment communicates more engineering judgment than a fake booking flow. Every cut in the explicitly-defined cut list signals boundary awareness.

The differentiating insight: the hiring manager evaluating the repo IS the user. Every design decision — the hybrid dispatcher's confidence trace, the file-based memory's transparency, the Mermaid graph in README — is optimized for a 3-minute repo review, not for production throughput.

## Project Classification

| Attribute | Value |
|---|---|
| **Project Type** | API Backend (LangGraph orchestration, CLI demo interface) |
| **Domain** | Scientific / AI — multi-agent coordination, retrieval architecture, prompt engineering |
| **Complexity** | Medium — novel AI technology stack; no regulatory or compliance overhead |
| **Project Context** | Greenfield |

## Success Criteria

### User Success

The primary user is a hiring manager evaluating an AI-Native Developer / Client Concierge candidate.

- **3-minute comprehension:** A hiring manager with LangGraph familiarity can clone the repo, run `python main.py --user alex`, and fully understand the system's architecture from CLI output alone — without reading source code first
- **Proactive personalization visible immediately:** The memory-driven greeting fires before any user input, proving the "proactive outcome completion" job requirement in the first 5 seconds
- **Routing intelligence is observable:** Every dispatcher decision prints `[DISPATCHER] intent=X confidence=0.87 → routing to ResearchAgent` — structured observability with no external tooling required
- **Architectural judgment is legible:** The `BookingAgent` stub with integration contract comment, the explicit cut list in documentation, and the `AgentPolicy` Pydantic constraints communicate more sophistication than a complete but shallow implementation

### Business Success

This MVP is Andrey's portfolio centerpiece for the AI-Native Developer / Client Concierge application.

- **Primary:** Advances the interview process — the repo functions as a technical screen pass on its own merit
- **Secondary:** Demonstrates spec-driven methodology (BMAD docs + SDD principles) as a repeatable engineering practice, not a one-off
- **5-day build constraint honored:** MVP delivered within the Day 1–5 plan — demonstrates estimation discipline and scope judgment

### Technical Success

- All LangGraph edges wire correctly: `Dispatcher → [RAG | Research | Fallback] → Guardrail → Response`
- Hybrid dispatcher: rule-based pre-filter executes first; LLM escalates only for ambiguous intents; confidence score emitted on every routing decision
- File-based memory reads profile on session start, writes session data on close; `memory/profiles/alex.json` inspectable mid-demo
- Guardrail node: blocks out-of-scope queries, emits one clarifying question at `confidence < threshold`, routes to human handoff message when unresolvable
- Zero external infrastructure required: no AWS, no LangSmith, no vector DB — runs with `python main.py --user alex`

### Measurable Outcomes

| Outcome | Target |
|---|---|
| Demo cold-start to first response | < 10 seconds |
| CLI trace completeness | Every graph node transition printed |
| Job description coverage | ≥ 7 of 9 MVP items mapped to JD bullets in README |
| Dispatcher confidence output | Emitted on 100% of routing decisions |
| Memory profile load on greeting | Fires before first user prompt, 100% of runs |

## Product Scope

### MVP — Minimum Viable Product

1. Dispatcher with hybrid routing (rule-based pre-filter + LLM escalation) + confidence trace
2. Prompt Orchestration Layer — `prompts/{agent_name}/{version}.yaml` for all agents
3. File-Based Memory service + pre-seeded `memory/profiles/alex.json`
4. LangGraph CLI flow trace — every node transition labeled and printed
5. Mock JSON Knowledge Base (5–10 destinations) with production swap-point comments
6. Proactive concierge opening — profile loaded at session start, memory-driven greeting
7. `BookingAgent` stub with integration contract comment
8. Blended Response with Source Attribution — RAG + Research results merged, sources cited inline: *"Based on our current offerings [RAG] and latest travel trends [Web]..."*
9. Agent-Initiated Follow-Up node — conditional `proactive_suggestion_node` edge after Research Agent completion

### Growth Features (Post-MVP)

- Production deployment on AWS Bedrock with real Knowledge Bases replacing mock JSON KB
- Live booking API integration replacing the stub
- Multi-user persona support beyond the "Alex" demo character
- `TokenBudgetManager` full summarization implementation (currently a documented stub)
- `AgentPolicy.allowed_tools` runtime enforcement

### Vision (Future)

- Web or Streamlit UI for non-CLI audiences
- LangSmith observability layer replacing CLI trace
- Full multi-tenant concierge platform serving real travel customers
- Provider abstraction (multi-provider support via `AgentPolicy.provider`)

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Portfolio MVP — a single, completable, runnable system that proves spec-driven multi-agent engineering capability. Success is one hiring manager running the demo and saying *"this person has built this before."*

**Resource Requirements:** 1 developer (Andrey), full-time, 5 days. No team, no infrastructure, no deployment.

**Scope constraint:** If it cannot be built, tested, and demo-scripted in 5 days — it is not MVP.

### 5-Day Build Plan

**Core Journeys Supported:** Hiring Manager (Journey 1), Alex Happy Path (Journey 2), Alex Edge Cases (Journey 3). Developer Extension (Journey 4) is supported by design but not validated in MVP.

| Day | Focus | Deliverables |
|---|---|---|
| **Day 1** | Spec | `spec/concierge-spec.md`, `ConciergeState` TypedDict, `AgentPolicy` Pydantic model, Mermaid graph in README |
| **Day 2** | Skeleton | LangGraph graph wired (all nodes, no LLM logic), file-based Memory service, prompt YAML structure, `memory/profiles/alex.json` pre-seeded |
| **Day 3** | Agents | Dispatcher with hybrid routing + confidence trace, RAG Agent + JSON KB, Research Agent + DuckDuckGo, Memory service R/W |
| **Day 4** | Polish | Proactive opening, CLI trace format, Guardrail node, BookingAgent stub, `TokenBudgetManager` (stub with comment), `validate_config.py`, `--fast-mode` |
| **Day 5** | Docs + Demo | BMAD-generated architecture docs, README with JD mapping table, 3-minute demo script, blended source attribution, Follow-Up node |

All 9 MVP items (as defined in Product Scope) must be complete by end of Day 5. Items 8 and 9 are Day 5 deliverables — first to cut if Day 3 agents exceed scope.

### Risk Mitigation Strategy

**Technical Risks:**

| Risk | Likelihood | Mitigation |
|---|---|---|
| Dispatcher Opus latency kills demo experience | Medium | `[DISPATCHER] classifying...` printed immediately; `--fast-mode` for testing; README sets expectations |
| State stale-data bug across turns | Medium | Per-turn reset protocol + `turn_id` validation |
| DuckDuckGo rate limit or availability | Low | KB-only fallback with labeled output; no hard dependency |
| LangGraph API change breaks graph wiring | Low | Version-pinned in `requirements.txt`; no bleeding-edge features |
| Day 5 runs out before demo script | Medium | Demo script drafted on Day 1 alongside spec — it defines what must work |

**Market Risks:**

| Risk | Mitigation |
|---|---|
| Hiring manager doesn't run the demo | README + demo script are the backup — repo must be comprehensible without running it |
| Architecture looks over-engineered for a demo | Honest stubs + explicit cut list signal judgment; ADRs explain every non-obvious decision |
| Another candidate submits a similar repo | TNL-HELP production provenance is the differentiator — visible in prompt patterns and architectural comments |

**Resource Risks:**

| Risk | Mitigation |
|---|---|
| Day 3 agents take longer than expected | Items 8 and 9 are Day 5 — cut them if needed without breaking the core demo |
| Scope creep from architecture decisions | All architecture decisions locked in Day 1 spec; no mid-build design changes |
| Single developer, context loss between sessions | BMAD docs + spec file serve as session-independent state; git commits after each day |

## User Journeys

### Journey 1: The Hiring Manager — "Is This Person Worth Interviewing?"

**Persona:** Sarah, Senior Engineering Manager at a hospitality AI company. She's reviewed 40 LangGraph repos this quarter. Most are tutorial rewrites. She has 10 minutes.

**Opening Scene:** Sarah receives a link to the repo. She opens the README. The first thing she sees is a Mermaid graph of the agent topology and a table mapping every architectural decision to a job description bullet. She reads for 90 seconds and thinks: *"Someone actually thought about this."*

**Rising Action:** She clones the repo, runs `pip install -r requirements.txt`, then `python main.py --user alex`. Before she types anything, the system prints:

```
[MEMORY] Loaded profile: alex — 2 past trips, 1 cached research session
Welcome back, Alex. Based on your March trip to Bali, you might be interested in upcoming deals to Southeast Asia.
```

She hasn't typed a single character. The "proactive outcome completion" requirement from the JD just ran in front of her eyes.

**Climax:** She types *"I'm thinking Southeast Asia but not sure where"* — an intentionally ambiguous query. The CLI prints:

```
[DISPATCHER] intent=travel_research confidence=0.61 → ambiguous, escalating to LLM
[DISPATCHER] LLM classification: destination_research confidence=0.84 → routing to ResearchAgent
[FLOW] dispatcher → research_agent → rag_lookup → response_synthesis → guardrail_check → response
```

She sees the hybrid routing logic execute live. The response cites both RAG (internal KB) and web research with labeled sources.

**Resolution:** Sarah opens `prompts/dispatcher/v1.yaml`, reads the prompt structure, then checks `memory/profiles/alex.json`. She closes the laptop and writes in her notes: *"This person has built this before. Schedule a call."*

*Reveals requirements: proactive opening, CLI trace format, hybrid dispatcher confidence output, file-based memory inspectability, blended source attribution, README JD mapping*

---

### Journey 2: Alex — Happy Path Traveler

**Persona:** Alex, a frequent traveler with two logged past trips (Bali, Tokyo). Profile pre-seeded with preferences and a cached Southeast Asia research session.

**Opening Scene:** Alex launches the concierge for the first time in a new session. Without prompting, the system greets him by name and references his Bali trip.

**Rising Action:** Alex asks: *"What are the best beach destinations in Southeast Asia right now?"* The dispatcher routes confidently to the Research Agent (intent clear, confidence > 0.85). The Research Agent queries both the JSON knowledge base (Bali, Phuket, Koh Samui entries) and a live web search tool. The response blends both, attributing sources.

**Climax:** Alex follows up: *"What about the Wyndham property in Phuket?"* This is a KB-specific query. The dispatcher routes directly to the RAG Agent. The response pulls from the mock KB, cites the internal source.

**Resolution:** Alex ends the session. `memory/sessions/{session_id}/` is written with the full conversation. On next run, the concierge will remember Southeast Asia was the last research context.

*Reveals requirements: session memory write, confident dispatcher routing, RAG-first for property queries, web-first for trend queries, session continuity*

---

### Journey 3: Alex — Edge Cases and Guardrails

**Scenario A — Ambiguous intent:** Alex asks *"Can you help me with something?"* Dispatcher confidence is 0.31 — below threshold. Guardrail node fires one clarifying question: *"Of course — are you looking to research a destination, check on a booking, or something else?"* Alex clarifies, flow continues.

**Scenario B — Out-of-scope query:** Alex asks *"Can you book me a flight to Bali?"* Dispatcher routes to BookingAgent (stub). The stub returns: *"Booking is not available in this version. A human travel specialist can assist — shall I connect you?"* Human handoff message fires. No fake booking flow executes.

**Scenario C — Completely out-of-scope:** Alex asks *"What's the weather like in London?"* Guardrail node classifies as out-of-domain (confidence < 0.4 after LLM pass). Response: *"I specialize in travel planning and concierge services. For weather, I'd suggest a weather service — but I can tell you the best time of year to visit London if that helps."*

*Reveals requirements: confidence threshold configuration, one-clarifying-question rule, BookingAgent stub contract, out-of-domain guardrail, graceful fallback messaging*

---

### Journey 4: The Developer — Extending the System

**Persona:** A developer (Andrey, or a future contributor) who wants to swap the mock JSON KB for a real AWS Bedrock Knowledge Base.

**Opening Scene:** Developer opens `agents/rag_agent.py`. Finds the comment: `# Production swap point: replace MockKnowledgeBase with BedrockKnowledgeBase(kb_id=os.getenv("BEDROCK_KB_ID"))`. One environment variable change, no graph rewiring needed.

**Rising Action:** Developer wants to add a new agent. Opens `prompts/` directory — sees versioned YAML files for each agent. Adds `prompts/hotel_agent/v1.yaml`. Follows the `AgentPolicy` Pydantic model to define the new agent's constraints. Wires one new node into the graph.

**Resolution:** The developer never touches the dispatcher logic to add a new agent capability — the graph topology is the extension point. The prompt is the spec; the graph is the contract.

*Reveals requirements: production swap-point comments, AgentPolicy Pydantic model as extension interface, prompt versioning convention, graph node isolation*

---

### Journey Requirements Summary

| Journey | Capabilities Required |
|---|---|
| Hiring Manager | Proactive opening, CLI trace, hybrid dispatcher, file-based memory, blended source attribution, README JD mapping |
| Alex — Happy Path | Session memory R/W, confident routing, RAG vs. web routing logic, session continuity |
| Alex — Edge Cases | Confidence threshold, clarifying question, BookingAgent stub, out-of-domain guardrail, fallback messaging |
| Developer Extension | Production swap-point comments, AgentPolicy model, prompt versioning, graph node isolation |

## Domain-Specific Requirements

### Compliance & Regulatory

No regulatory compliance. No certifications required.

**Security:** API keys loaded from `.env` file (gitignored). Repo ships with `.env.example` showing required variables. No keys committed.

### Technical Constraints

**Runtime Environment**
- Requires: Python 3.11+, `pip install -r requirements.txt`, `.env` with `ANTHROPIC_API_KEY`
- Entry point: `python main.py --user alex`
- Runs fully offline except for LLM API calls and web search

**LLM**
- Claude via Anthropic SDK (`ANTHROPIC_API_KEY`) — the only required credential
- Model pinned per agent in `AgentPolicy.model` — tunable without code changes
- Non-determinism handled by hybrid dispatcher: rule-based pre-filter for deterministic routing, LLM only for ambiguous classification

**Web Search**
- DuckDuckGo search — no API key required, zero configuration
- **Fallback:** KB-only response with labeled output: `[WEB SEARCH UNAVAILABLE — serving from internal KB only]`

**Prompt Reproducibility**
- All prompts stored in `prompts/{agent_name}/{version}.yaml`
- Version pinned in `AgentPolicy.prompt_version`; prompt changes require version bump

**File-Based Memory**
- Read/write local JSON: `memory/profiles/{user_id}.json`, `memory/sessions/{session_id}.json`
- `memory/profiles/alex.json` pre-seeded in repo
- Inspectable by hiring manager mid-demo — no database, no external state

### Integration Requirements

| Integration | Type | Key |
|---|---|---|
| Anthropic SDK (Claude) | Required | `ANTHROPIC_API_KEY` |
| DuckDuckGo search | Required | No key required |
| File System | Required | Local JSON — no setup |

### Risk Mitigations

| Risk | Mitigation |
|---|---|
| Hiring manager missing API key | `.env.example` + clear README setup section (one key only) |
| LLM routing inconsistency | Rule-based pre-filter handles high-confidence intents deterministically |
| Web search unavailable | Graceful degradation: DuckDuckGo → KB-only with labeled output |
| Memory files missing | Fresh session started without personalization; no crash |
| API key committed to repo | `.gitignore` enforced; noted in README |

## Technical Architecture

### Overview

Python LangGraph CLI application. Entry point: `python main.py --user alex`. The LangGraph graph is the system — the CLI is a thin adapter. Sub-agents receive scoped context from the dispatcher; they do not hold the conversation history. All user interaction flows through the dispatcher's context window.

**Runtime:** Python 3.11+, LangGraph as the core framework, Anthropic SDK for all LLM calls.

**Graph as API:** `graph.invoke(state)` / `graph.stream(state)` is the primary interface. No I/O inside nodes — all input/output flows through LangGraph state.

**Conversation ownership:** The Dispatcher node owns the full conversation context window across the entire session. Last 10 turns passed verbatim to LLM context; older turns summarized by `token_budget_manager`. Full history stored in `memory/sessions/{session_id}.json` on disk. Sub-agents receive only task-relevant slices — they never see the full history.

**Note:** Summary buffer never fires in a standard 5–8 turn demo. It is a production-readiness signal, not a demo dependency.

### State Schema (TypedDict)

```python
class ConciergeState(TypedDict):
    # Conversation — owned by Dispatcher, full session history
    user_id: str
    session_id: str
    turn_id: int                           # incremented each turn; sub-agents validate currency
    conversation_history: list[Message]    # full context, Dispatcher only
    current_input: str
    current_response: str

    # Routing — set by Dispatcher, reset to None each turn before routing
    intent: str
    confidence: float
    route: Literal["rag", "research", "fallback", "booking_stub"]

    # Sub-agent outputs — reset to None by Dispatcher at start of each turn
    rag_results: list[KBEntry] | None
    research_results: list[SearchResult] | None
    source_attribution: list[str]

    # Memory
    memory_profile: UserProfile | None
    proactive_suggestion: str | None

    # Governance
    guardrail_passed: bool
    clarification_needed: bool
    clarification_question: str | None
    human_handoff: bool
```

**State reset protocol:** Dispatcher explicitly resets `rag_results`, `research_results`, `source_attribution`, `clarification_question`, `proactive_suggestion` to `None`/`[]` at the start of every turn before routing. Prevents stale sub-agent data from bleeding across turns.

### Multi-Model Strategy

Model declared in `AgentPolicy.model` per agent — configurable in `prompts/{agent}/policy.yaml` without code changes.

| Agent / Node | Model | Rationale |
|---|---|---|
| Dispatcher | `claude-opus-4-5` | Full conversation context + complex intent classification |
| Research Agent | `claude-sonnet-4-5` | Multi-step reasoning over web results + synthesis |
| Response Synthesis | `claude-sonnet-4-5` | Blending sources with attribution requires coherent reasoning |
| RAG Agent | `claude-haiku-4-5` | Fast retrieval formatting from structured KB |
| Guardrail Node | `claude-haiku-4-5` | Pattern matching + confidence check only |
| Follow-Up Node | `claude-haiku-4-5` | Template-driven proactive suggestion |

**`--fast-mode`:** CLI flag overrides all agents to `claude-haiku-4-5` for budget-conscious development testing. Prints banner: `[FAST MODE] Using Haiku across all agents — for production demo run without --fast-mode`. Positioned in README as dev-only, not the demo path.

### AgentPolicy (Pydantic)

```python
class AgentPolicy(BaseModel):
    agent_name: str
    model: str                    # e.g. "claude-opus-4-5"
    prompt_version: str           # e.g. "v1"
    max_tokens: int               # enforced before LLM call
    confidence_threshold: float   # below this → clarification or fallback
    max_clarifications: int       # max per session before human handoff
    allowed_tools: list[str]      # tool allowlist — declarative, not runtime-enforced in MVP
```

### Token Budget Management

| Agent | Context In | Max Output | Notes |
|---|---|---|---|
| Dispatcher | Last 10 turns + summaries | `128` | `# Structured routing output only` |
| Research Agent | Task slice (query + 3 recent turns) | `1024` | Summarized web results |
| RAG Agent | Query only | `512` | Direct KB match |
| Response Synthesis | RAG + Research results | `1024` | Final user-facing response |
| Guardrail | Current response draft | `256` | Pass/fail + reason only |

**`TokenBudgetManager` utility class:** Checks token count of `conversation_history` before each Dispatcher call. When approaching context limit: summarizes oldest turns into a `role: system_summary` message using `claude-haiku-4-5`. `[SUMMARY]` messages never leak into user-facing responses — Response Synthesis filters `role == "system_summary"` before generation.

```python
# Uses claude-haiku-4-5 when implemented
# Summary buffer never fires in a standard 5–8 turn demo
# Production-readiness signal — not a demo dependency
class TokenBudgetManager:
    def check_and_summarize(self, history: list[Message]) -> list[Message]: ...
```

### Node Contracts

```
python main.py --user alex
    └─► [MEMORY] Load profile → proactive greeting if profile found
            │
            ▼
    User Input
            │
            ▼
    Dispatcher (Opus) ← resets sub-agent fields; appends to conversation_history
            ├─► intent=rag, confidence≥threshold       → RAG Agent (Haiku)
            ├─► intent=research, confidence≥threshold  → Research Agent (Sonnet)
            ├─► intent=booking                         → BookingAgent Stub
            ├─► confidence<threshold                   → Guardrail (Haiku) → clarifying Q
            └─► out_of_domain                          → Guardrail (Haiku) → human handoff
                        │
                        ▼
              Response Synthesis (Sonnet)  ← filters system_summary messages
                        │
                        ▼
              Follow-Up Node (Haiku) [conditional edge]
                        │
                        ▼
              Output to CLI
```

### Architecture Decision Records

**ADR-001: Single Context Window for Dispatcher**
Dispatcher owns `conversation_history` across the full session. Last 10 turns passed verbatim; older turns summarized. Sub-agents receive scoped slices only. Full history persisted to disk. *Rationale: routing quality requires recency + session context; sub-agents need only task-relevant input.*

**ADR-002: Multi-Model Per Agent**
Each agent declares its model in `AgentPolicy.model`. Dispatcher uses Opus (complex routing, full context); reasoning agents use Sonnet; utility agents use Haiku. `--fast-mode` overrides to Haiku for development. *Rationale: cost-aware model selection is a production signal; Opus on dispatcher is the architectural statement.*

**ADR-003 (note):** Anthropic-only for MVP. Provider abstraction deferred post-MVP.

**ADR-004 (note):** Per-agent `max_tokens` declared in `AgentPolicy`. Dispatcher output capped at 128 tokens — structured routing only.

### Error Handling

| Scenario | Behavior |
|---|---|
| DuckDuckGo unavailable | Degrade to KB-only; labeled `[WEB SEARCH UNAVAILABLE]` |
| Anthropic API timeout | Retry once; return `"I'm having trouble connecting — please try again"` |
| Memory profile missing | Fresh session, no personalization, no crash |
| Confidence below threshold 3× consecutive | Human handoff message; session flagged |
| Stale sub-agent data across turns | Dispatcher resets all sub-agent fields to `None` at turn start |
| `[SUMMARY]` marker in response | Response Synthesis filters `role: system_summary` before generation |
| Policy YAML references unavailable model | `validate_config.py` catches at startup before first LLM call |

### Pre-Run Validation

`validate_config.py` — run before first demo:
- Reads all policy YAMLs
- Verifies `ANTHROPIC_API_KEY` is set
- Asserts all agents use available models
- Prints `[CONFIG OK]` or actionable error

README quickstart: `python validate_config.py && python main.py --user alex`

### SDKs

```
langgraph>=0.2
anthropic>=0.40
pydantic>=2.0
duckduckgo-search>=6.0
```

## Functional Requirements

### Intent Routing & Dispatch

- **FR1:** System can accept a natural language message and initiate the agent routing lifecycle
- **FR2:** Dispatcher can classify high-confidence intents without invoking an LLM
- **FR3:** Dispatcher can escalate ambiguous intents through a secondary classification step
- **FR4:** Dispatcher can emit a structured routing decision including intent label and confidence score on every message
- **FR5:** Dispatcher can route messages to the appropriate agent based on intent classification result
- **FR6:** System can ensure sub-agent outputs from previous turns do not affect current turn processing
- **FR7:** System can accept a `--fast-mode` CLI flag that overrides all agent models to a lightweight model for development testing
- **FR8:** Dispatcher can maintain the full conversation history as the sole context owner across an entire session
- **FR51:** Dispatcher can route messages to specialist agents for response generation — it does not generate user-facing responses directly

### Knowledge Retrieval

- **FR9:** RAG Agent can retrieve relevant entries from a structured JSON file serving as the knowledge base
- **FR10:** Research Agent can perform web search using DuckDuckGo given a user query
- **FR11:** System can degrade gracefully to KB-only responses when web search is unavailable, labeled with `[WEB SEARCH UNAVAILABLE]`
- **FR12:** Response Synthesis can merge RAG Agent and Research Agent results into a single blended response
- **FR13:** Response Synthesis can attribute sources inline in the final response, distinguishing internal KB from web search results
- **FR14:** Research Agent can operate without access to the full session conversation history
- **FR15:** Knowledge base can expose production swap-point comments identifying the replacement path to a hosted vector database
- **FR54:** System can label inline source attributions with consistent tags distinguishing internal KB results from web search results

### Memory & Personalization

- **FR16:** Memory Service can load a user profile from a local JSON file at session start
- **FR17:** Memory Service can write session data to a local JSON file at session end
- **FR18:** System can generate a single proactive memory-driven greeting at session start, before any user input, when a profile exists
- **FR19:** System ships with a pre-seeded demo user profile (`alex`) containing past trips, preferences, and a cached research session
- **FR20:** User can inspect the demo persona's memory state as a readable local JSON file during the demo
- **FR21:** System can start a fresh session without personalization when no profile file exists, without crashing

### Governance & Safety

- **FR22:** Guardrail can detect when response confidence is below the agent's configured `confidence_threshold` and emit one clarifying question per turn
- **FR23:** Guardrail can classify queries as out-of-domain and return a labeled deflection response
- **FR24:** System can route to a human handoff message when confidence remains below threshold after the maximum number of clarification attempts
- **FR25:** BookingAgent stub can return a labeled message indicating the integration point for a real booking service, and expose an integration contract in code
- **FR26:** System can enforce a configurable maximum number of clarification attempts per session before triggering human handoff
- **FR27:** System can ensure internal memory management messages are never exposed in user-facing responses
- **FR28:** Follow-Up Node can conditionally inject a proactive suggestion after a Research Agent response, based on a configured graph edge condition

### Observability & Tracing

- **FR29:** System can print a labeled trace entry for every graph node transition during execution
- **FR30:** System can print Dispatcher routing decisions with intent classification, confidence score, and destination agent
- **FR31:** System can print Memory Service load and write events with profile metadata at session boundaries
- **FR48:** Dispatcher can emit routing decisions in a consistent structured format parseable by the CLI trace printer
- **FR50:** System can format all trace output using a consistent bracket-label convention: `[NODE_NAME] key=value → outcome`
- **FR53:** System can include the active model name in CLI trace output for each agent invocation

### Configuration & Extensibility

- **FR34:** Each agent can declare its LLM model and prompt version in a versioned YAML policy file without requiring code changes
- **FR35:** System can enforce per-agent token output limits declared in `AgentPolicy` before each LLM call
- **FR36:** Developer can add a new agent capability by wiring a new graph node without modifying the Dispatcher's core classification logic — routing rules for new agents are declared in configuration
- **FR37:** Developer can change an agent's prompt by incrementing its version in the YAML without touching graph code
- **FR38:** System can validate all policy YAML configurations and API credentials via a standalone pre-run script before the main application starts
- **FR39:** System can detect when conversation context approaches the model's token limit
- **FR40:** System can compress oldest conversation turns to preserve recent context when approaching token limits
- **FR46:** System can assign a different LLM model to each agent based on its declared policy configuration

### Session & State Management

- **FR41:** System can maintain a typed state schema covering all agent handoffs within a session
- **FR42:** System can ensure agents always operate on data from the current conversation turn
- **FR43:** System can persist the full conversation history to a local session file regardless of LLM context window constraints
- **FR45:** System can write session data to disk when the user exits, preserving continuity for the next session
- **FR49:** User can inspect session history files in a labeled directory without additional tooling
- **FR52:** System can maintain conversation history in two distinct stores — in-session state for active routing and a persisted file for cross-session continuity

### Demo Integrity & Developer Experience

- **FR44:** System can run end-to-end from a single terminal command with one required environment variable (`ANTHROPIC_API_KEY`)
- **FR47:** System can notify the user when operating in reduced-capability mode via a visible session banner
- **FR55:** System ships with a documented demo script containing pre-validated queries with known expected routing outcomes
- **FR56:** System can restore the demo user profile to its pre-seeded state via a documented reset command
- **FR57:** System can surface actionable error messages when LLM API calls fail, without exposing raw stack traces

## Non-Functional Requirements

### Performance

- **NFR1:** Cold start to first agent response (including profile load + first Dispatcher LLM call) completes within 10 seconds
- **NFR2:** A full demo script execution (5 user turns, 4 distinct agent routes) completes in under 5 minutes total
- **NFR3:** Dispatch loop overhead (state reset + routing decision emission) adds less than 2 seconds per turn, excluding LLM API latency
- **NFR4:** In `--fast-mode` with Haiku, cold start to first response completes within 5 seconds

### Security

- **NFR5:** API keys are loaded from environment variables or `.env` file only — never written to config files, session files, or trace output
- **NFR6:** No credentials, API keys, or user identifiers are written to any file the system creates during normal operation
- **NFR7:** `.env` is listed in `.gitignore` and absent from all commits; `.env.example` documents required variables without values

### Reliability

- **NFR8:** System must not raise an unhandled exception when any optional component (DuckDuckGo, memory profile, session file) is unavailable — graceful degradation required in all cases
- **NFR9:** If an Anthropic API call fails, system retries once and surfaces an actionable error message — it does not silently drop the user's turn or hang
- **NFR10:** A two-turn conversation that switches agent routes between turns must produce correct, non-stale output on 100% of runs — validated by unit test

### Developer Experience

- **NFR11:** A developer can go from `git clone` to a running first session in under 5 minutes: `pip install` + set `ANTHROPIC_API_KEY` + `validate_config.py` + `main.py`
- **NFR12:** `validate_config.py` surfaces all configuration errors before any LLM call is made, each with a specific fix instruction
- **NFR13:** All agent policy YAML files follow a consistent schema — a new contributor can create a valid policy file by copying an existing one without reading source code

### Documentation

- **NFR14:** README contains a Mermaid agent topology diagram showing the full graph structure
- **NFR15:** README contains a table mapping every major architectural decision to a specific job description requirement
- **NFR16:** ADR-001 (context window ownership) and ADR-002 (multi-model strategy) are documented in the repo with decision context, options considered, and rationale
- **NFR17:** `spec/concierge-spec.md` exists and is written before any implementation begins — it serves as the authoritative source of agent contracts, state schema, and edge conditions
