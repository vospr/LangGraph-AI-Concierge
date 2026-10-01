# Story 2.2: Build LangGraph StateGraph with All 7 Nodes Wired as Stubs

Status: review

## Story

As a **developer**,
I want all 7 LangGraph nodes wired as one-liner stubs that delegate to agent classes,
so that the graph compiles and runs end-to-end even before agent logic is implemented.

## Acceptance Criteria

1. **Given** `graph/__init__.py` from Story 2.1, **When** I wire all 7 nodes, **Then** `compiled_graph` exports without errors
2. **Given** `compiled_graph`, **When** I call `compiled_graph.invoke(state)`, **Then** it routes through all 7 nodes in sequence (Dispatcher -> RAG/Research/Booking -> Guardrail -> Response Synthesis -> Follow-Up)
3. **Given** `nodes/*.py`, **When** I read each file, **Then** it contains a module docstring explaining the agent/node seam and a one-liner function delegating to the corresponding agent class
4. **Given** the graph invocation, **When** no error occurs, **Then** `state` is returned unchanged (all agents return state unmodified while stubbed)
5. **Given** `state["turn_id"]`, **When** agents are invoked, **Then** all agents receive the same turn_id value without modification

## Tasks / Subtasks

- [x] Task 1: Add contract tests for node-stub delegation and wiring sequence (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_2_2_node_stub_wiring.py`
  - [x] 1.2: Assert each `nodes/*.py` contains module docstring and single delegate function
  - [x] 1.3: Assert `compiled_graph` is importable and executable through stub route paths
  - [x] 1.4: Assert core state fields remain unchanged by stub agents and `turn_id` is preserved
  - [x] 1.5: Assert executed route path includes Dispatcher -> Specialist -> Guardrail -> Synthesis -> Follow-Up

- [x] Task 2: Implement stub agent classes for all seven graph roles (AC: 3, 4, 5)
  - [x] 2.1: Create stub agent modules under `src/concierge/agents/` for dispatcher, rag, research, booking, guardrail, response synthesis, followup
  - [x] 2.2: Implement one method per class returning state unchanged
  - [x] 2.3: Keep each class minimal and deterministic (no side effects)

- [x] Task 3: Implement node seam modules delegating to agent stubs (AC: 3, 5)
  - [x] 3.1: Create `src/concierge/nodes/` package and 7 node modules
  - [x] 3.2: Add module docstrings explaining seam responsibility
  - [x] 3.3: Implement one-line delegate functions calling matching agent class `.run(state)`

- [x] Task 4: Update graph wiring to consume node modules and expose sequence metadata (AC: 1, 2, 4, 5)
  - [x] 4.1: Wire graph to node functions in `src/concierge/graph/__init__.py`
  - [x] 4.2: Ensure route path passes through Guardrail then Synthesis then Follow-Up for specialist routes
  - [x] 4.3: Preserve non-mutating invocation semantics for caller-owned state object

- [x] Task 5: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5)
  - [x] 5.1: Run `pytest tests/unit/test_story_2_2_node_stub_wiring.py -q`
  - [x] 5.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 5.3: Update story `Dev Agent Record`, `File List`, and `Change Log` with implementation evidence
  - [x] 5.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Keep agent stubs behavior-neutral: they receive and return state without business logic.
- Node modules are seam-only delegates; routing logic belongs to graph wiring, not node files.
- Preserve compatibility with Story 2.1 contracts (`compiled_graph` importability, no input mutation).
- Prefer deterministic metadata for path verification in tests instead of framework internals.

### Testing Notes

- Use pure unit tests and avoid external runtime dependencies.
- Verify both file-level conventions (docstring + one-liner function) and runtime path behavior.
- Validate `turn_id` continuity across path execution.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.2]
- [Source: spec/concierge-spec.md#§NodeContracts]
- [Source: spec/concierge-spec.md#§GraphTopology]
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_2_2_node_stub_wiring.py -q` -> 4 failed (missing `nodes/*.py`, `turn_id` mutation in dispatcher path, missing executed path metadata).
- Green phase: added seven stub agent classes in `src/concierge/agents/` with identity `run(state)` behavior.
- Green phase: added `src/concierge/nodes/` seam modules, each with module docstring and one-line delegate function.
- Green phase: rewired `src/concierge/graph/__init__.py` to use node delegates, specialist -> guardrail -> synthesis -> followup sequence, and exported deterministic `_executed_nodes` metadata.
- Regression fix: added backward-compatible `GRAPH_EDGES` entries and `CONDITIONAL_EDGES["synthesis"]` metadata to keep Story 2.1 contract tests passing after topology refinement.
- Targeted validation: `pytest tests/unit/test_story_2_2_node_stub_wiring.py -q` -> 6 passed.
- Full regression: `pytest tests -q` -> 60 passed, 2 skipped.

### Completion Notes List

- Implemented Story 2.2 node/agent stub seam with graph wiring that routes specialist paths through Guardrail, Synthesis, and Follow-Up.
- Preserved stub invariants: core state fields remain unchanged, turn_id preserved, and caller-owned input object is not mutated.
- Added dedicated Story 2.2 contract tests plus compatibility updates so Story 2.1 and 2.2 pass together.

## File List

- _bmad-output/implementation-artifacts/2-2-build-langgraph-stategraph-with-all-7-nodes-wired-as-stubs.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_2_2_node_stub_wiring.py (created)
- src/concierge/graph/__init__.py (modified)
- src/concierge/agents/dispatcher.py (created)
- src/concierge/agents/rag_agent.py (created)
- src/concierge/agents/research_agent.py (created)
- src/concierge/agents/booking_agent.py (created)
- src/concierge/agents/guardrail.py (created)
- src/concierge/agents/response_synthesis.py (created)
- src/concierge/agents/followup.py (created)
- src/concierge/nodes/__init__.py (created)
- src/concierge/nodes/dispatcher_node.py (created)
- src/concierge/nodes/rag_node.py (created)
- src/concierge/nodes/research_node.py (created)
- src/concierge/nodes/booking_node.py (created)
- src/concierge/nodes/guardrail_node.py (created)
- src/concierge/nodes/synthesis_node.py (created)
- src/concierge/nodes/followup_node.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 2.2 node/agent stubs, rewired graph sequence, added tests, and moved status to review after full suite pass.
