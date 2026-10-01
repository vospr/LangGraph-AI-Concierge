# Story 2.1: Create `graph/__init__.py` State Initialization and Graph Compilation

Status: review

## Story

As a **developer**,
I want `graph/__init__.py` to initialize `ConciergeState` with all default values and compile the graph with all edges,
so that the graph is a single importable unit that can be invoked without side effects.

## Acceptance Criteria

1. **Given** `ConciergeState`, **When** initialized, **Then** all optional fields (e.g., `rag_results`, `error`, `proactive_suggestion`) default to `None` or `[]`
2. **Given** `graph/__init__.py`, **When** imported, **Then** `compiled_graph` is returned as the compiled, runnable graph
3. **Given** the compiled graph, **When** I inspect it, **Then** all 7 nodes are present and all expected edges (including conditional edges) are wired
4. **Given** the graph, **When** I call `compiled_graph.invoke(state)`, **Then** the invocation produces a modified `state` dict with no side effects to the original

## Tasks / Subtasks

- [x] Task 1: Add contract-first tests for state defaults and graph assembly (AC: 1, 2, 3, 4)
  - [x] 1.1: Create `tests/unit/test_story_2_1_graph_init_contract.py` validating default state initialization contract
  - [x] 1.2: Add tests asserting importable `compiled_graph` and runnable `.invoke(...)` behavior
  - [x] 1.3: Add tests asserting presence of all 7 nodes and required edge/conditional-edge metadata
  - [x] 1.4: Add test proving invocation does not mutate input object in place

- [x] Task 2: Implement typed state initialization module (AC: 1)
  - [x] 2.1: Create `src/concierge/state.py` with `ConciergeState` TypedDict and helper `initialize_state(...)`
  - [x] 2.2: Ensure all optional per-turn and sub-agent fields are initialized to `None`/`[]` defaults
  - [x] 2.3: Add lightweight node/route constants for graph assembly consistency

- [x] Task 3: Implement graph compilation/export in `graph/__init__.py` (AC: 2, 3, 4)
  - [x] 3.1: Create graph package `src/concierge/graph/__init__.py`
  - [x] 3.2: Define seven node stubs and expected topology wiring metadata
  - [x] 3.3: Export `compiled_graph` and provide deterministic invoke behavior returning a modified copy
  - [x] 3.4: Keep import side effects minimal and graph importable as a single unit

- [x] Task 4: Validate and finalize story implementation (AC: 1, 2, 3, 4)
  - [x] 4.1: Run `pytest tests/unit/test_story_2_1_graph_init_contract.py -q`
  - [x] 4.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 4.3: Update story `Dev Agent Record`, `File List`, and `Change Log` with implementation evidence
  - [x] 4.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Keep state contract aligned with `spec/concierge-spec.md` (`ConciergeState` keys and route vocabulary).
- Graph topology must reflect architecture-level flow:
  - dispatcher -> rag/research/booking_stub/guardrail paths
  - synthesis -> followup conditional path
- Invocation behavior must operate on a copy of incoming state to avoid in-place mutation side effects.
- Node logic in this story remains stub-level; real agent delegation follows in Story 2.2.

### Testing Notes

- Use pure unit tests; no network calls and no external service dependencies.
- Validate graph structure using explicit exported metadata to avoid brittle framework internals.
- Ensure deterministic assertions around state copy semantics and modified output.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.1]
- [Source: spec/concierge-spec.md#§State — ConciergeState]
- [Source: spec/concierge-spec.md#§GraphTopology]
- [Source: _bmad-output/planning-artifacts/architecture.md#StateGraph assembly]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_2_1_graph_init_contract.py -q` -> 4 failed (`concierge.state` / `concierge.graph` missing).
- Green phase: implemented `src/concierge/state.py` with `ConciergeState`, `NodeName`, and `initialize_state(...)` defaults.
- Green phase: implemented `src/concierge/graph/__init__.py` with 7-node topology metadata, conditional edge map, importable `compiled_graph`, and deterministic invoke semantics on deep-copied state.
- Targeted validation: `pytest tests/unit/test_story_2_1_graph_init_contract.py -q` -> 4 passed.
- Full regression: `pytest tests -q` -> 54 passed, 2 skipped.

### Completion Notes List

- Implemented Story 2.1 state initialization and graph compilation contracts end-to-end.
- Added graph contract tests covering state defaults, runnable compiled graph export, 7-node edge wiring, and input immutability guarantees.
- Added framework-safe graph builder with graceful fallback compiled graph when LangGraph runtime is unavailable in the active interpreter.

## File List

- _bmad-output/implementation-artifacts/2-1-create-graph-init-py-state-initialization-and-graph-compilation.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_2_1_graph_init_contract.py (created)
- src/concierge/state.py (created)
- src/concierge/graph/__init__.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 2.1 state/graph skeleton with tests and moved status to review after full suite pass.
