# Story 3.6: Implement Error Handling at Node Boundary with Actionable Messages

Status: review

## Story

As a **developer**,
I want every node to catch LLM API errors, set `state["error"]` to an actionable message, set `state["human_handoff"] = True`, and return state without raising exceptions,
so that the demo never crashes and the user always gets a helpful message.

## Acceptance Criteria

1. **Given** an Anthropic API timeout in the Dispatcher, **When** the node catches it, **Then** `state["error"] = "LLM connection timeout. Please try again."` (no raw stack trace)
2. **Given** a missing or invalid API key, **When** caught, **Then** `state["error"]` contains the exact fix: `"ANTHROPIC_API_KEY not set or invalid"`
3. **Given** any node catching an exception, **When** it returns, **Then** graph routing is not interrupted and terminal response handling can read `state["error"]`
4. **Given** the error path, **When** trace is printed, **Then** the catching node still prints its `[NODE_NAME]` trace entry before exit
5. **Given** `state["human_handoff"] = True`, **When** the graph reaches terminal response handling, **Then** user-facing message ends with `"A human travel specialist can help - please wait"`

## Tasks / Subtasks

- [x] Task 1: Add failing tests for node-boundary error handling (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_3_6_node_boundary_error_handling.py`
  - [x] 1.2: Add dispatcher-timeout catch test asserting actionable message and `human_handoff=True`
  - [x] 1.3: Add invalid-key catch test asserting exact fix message
  - [x] 1.4: Add graph-continuation test proving error path does not break routing sequence
  - [x] 1.5: Add terminal response test asserting message suffix for human handoff path

- [x] Task 2: Implement node-boundary exception handling and terminal message behavior (AC: 1, 2, 3, 4, 5)
  - [x] 2.1: Add shared node error-message normalizer for timeout and API key failures
  - [x] 2.2: Wrap every node delegate in `try/except` while preserving one trace call at node start
  - [x] 2.3: Return update payload with `error` + `human_handoff=True` from catch path (no exception re-raise)
  - [x] 2.4: Update terminal response handling (`ResponseSynthesisAgent`) to emit actionable message from `state["error"]`
  - [x] 2.5: Keep normal non-error behavior unchanged for existing story contracts

- [x] Task 3: Regression validation and story updates (AC: all)
  - [x] 3.1: Run targeted tests for Story 3.6 plus impacted Story 2.2 and trace tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story file record, file list, change log, and sprint status

## Dev Notes

### Architecture Compliance Guardrails

- Catch errors at **node boundary**, not in `main.py`.
- Do not emit stack traces to user-facing output.
- `state["error"]` is internal state and must never be traced directly (`trace` denylist includes `error`).
- Node trace completeness is mandatory: each node must still emit trace at start, including error path.
- Graph must continue through terminal response handling even when a node fails.

### Technical Requirements

- Error mapping rules:
  - Timeout-like failures -> `"LLM connection timeout. Please try again."`
  - API-key/auth-like failures -> `"ANTHROPIC_API_KEY not set or invalid"`
  - Other failures -> actionable generic fallback without stack trace leakage
- Catch path update payload must set at minimum:
  - `human_handoff: True`
  - `error: <actionable message>`
- Terminal response handling must synthesize user-facing output from error/handoff state and include suffix:
  - `A human travel specialist can help - please wait`

### Previous Story Intelligence (3.5)

- Dispatcher orchestration already centralizes per-turn reset and single routing decision traces.
- Preserve Story 3.5 behavior: no stale state leaks, no regression in history ownership, no extra dispatcher trace spam.
- Existing tests assume node modules remain thin delegates; update that contract carefully to reflect node-boundary try/catch requirement.

### File Structure Notes

- Primary targets:
  - `src/concierge/nodes/*.py`
  - `src/concierge/agents/response_synthesis.py`
  - `tests/unit/test_story_3_6_node_boundary_error_handling.py`
  - impacted contract tests in `tests/unit/`
- Keep changes story-scoped; no unrelated architecture rewrites.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.6]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1: Error Handling Propagation]
- [Source: src/concierge/trace.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_3_6_node_boundary_error_handling.py -q` -> 10 failed (node exceptions escaped).
- Green phase: implemented shared node error helper + node-boundary try/except across all nodes; updated terminal synthesis response for error/handoff path.
- Targeted validation:
  - `pytest tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_trace.py tests/unit/test_story_3_3_stage1_prefilter.py tests/unit/test_story_3_4_stage2_llm_escalation.py tests/unit/test_story_3_5_dispatcher_orchestration.py -q`
  - Result: 30 passed
- Full regression: `pytest tests -q` -> 98 passed, 2 skipped.

### Completion Notes List

- Added node-boundary exception handling for all 7 graph nodes while preserving one trace call per node.
- Implemented centralized actionable error mapping for timeout and API-key/auth failure classes.
- Added terminal response synthesis behavior for error/handoff flow with required handoff suffix.
- Updated node contract test to reflect boundary try/except pattern.

### File List

- _bmad-output/implementation-artifacts/3-6-implement-error-handling-at-node-boundary-with-actionable-messages.md (created and updated)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/response_synthesis.py (modified)
- src/concierge/nodes/error_handling.py (created)
- src/concierge/nodes/dispatcher_node.py (modified)
- src/concierge/nodes/rag_node.py (modified)
- src/concierge/nodes/research_node.py (modified)
- src/concierge/nodes/booking_node.py (modified)
- src/concierge/nodes/guardrail_node.py (modified)
- src/concierge/nodes/synthesis_node.py (modified)
- src/concierge/nodes/followup_node.py (modified)
- tests/unit/test_story_2_2_node_stub_wiring.py (modified)
- tests/unit/test_story_3_6_node_boundary_error_handling.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented node-boundary error handling and terminal response behavior; validated with targeted + full regression; moved status to review.
