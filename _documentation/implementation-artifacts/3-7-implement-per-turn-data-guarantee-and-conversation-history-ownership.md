# Story 3.7: Implement Per-Turn Data Guarantee and Conversation History Ownership

Status: done

## Story

As a **developer**,
I want the Dispatcher to guarantee that all agents in a turn operate on current-turn data (no stale sub-agent results from prior turns), and that the full conversation history is persisted independently of LLM context windows,
so that session continuity is reliable.

## Acceptance Criteria

1. **Given** Turn 2 of a conversation, **When** the Dispatcher calls `reset_turn_state()`, **Then** all sub-agent fields from Turn 1 are reset to `None`
2. **Given** Turn 2 routing to RAG Agent, **When** RAG Agent receives state, **Then** `state["rag_results"] = None` (guaranteed fresh, not Turn 1 stale data)
3. **Given** `state["conversation_history"]`, **When** inspected at the end of Turn N, **Then** it contains all N turns verbatim (complete session history independent of LLM context window)
4. **Given** the Dispatcher managing history, **When** it receives a new user message in Turn N+1, **Then** the message is appended to `conversation_history` before any routing decision
5. **And** NFR3 is met: dispatch loop overhead (reset + routing decision emission) is < 2s per turn, excluding LLM API latency

## Tasks / Subtasks

- [x] Task 1: Add story-specific failing tests for per-turn data guarantees (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py`
  - [x] 1.2: Add test verifying stale sub-agent fields are reset in Dispatcher update payload
  - [x] 1.3: Add graph-level test verifying RAG Agent receives `rag_results=None` on Turn 2
  - [x] 1.4: Add multi-turn history ownership test asserting verbatim carry-forward + append-before-routing behavior
  - [x] 1.5: Add dispatch overhead test (<2s, excluding LLM latency) using deterministic no-LLM path

- [x] Task 2: Implement and harden per-turn freshness/history behavior (AC: 1, 2, 3, 4)
  - [x] 2.1: Ensure Dispatcher reset contract covers all turn-scoped sub-agent fields
  - [x] 2.2: Ensure Turn 2 stale data cannot leak to specialist nodes during graph invocation
  - [x] 2.3: Preserve full `conversation_history` ownership in Dispatcher run flow
  - [x] 2.4: Keep existing Story 3.5 orchestration and Story 3.6 error-path behavior intact

- [x] Task 3: Validate NFR3 and finalize artifacts (AC: all)
  - [x] 3.1: Run targeted Story 3.7 + impacted Dispatcher/graph tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record, file list, change log, and sprint status

## Dev Notes

### Architecture Guardrails

- Dispatcher remains the sole owner of session conversation history.
- Per-turn freshness is enforced by `reset_turn_state()` and must be visible at specialist node entry.
- No stale sub-agent payloads (`rag_results`, `research_results`, `source_attribution`, etc.) may survive across turns.
- Existing node-boundary error handling from Story 3.6 must remain unchanged.

### Previous Story Intelligence

- Story 3.1 established the baseline reset helper and stale-state unit contract.
- Story 3.5 moved reset/history ownership into Dispatcher orchestration and added sequence coverage.
- Story 3.6 added node-boundary exception handling; freshness logic must not regress this path.

### File Structure Notes

- Primary expected targets:
  - `tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py`
  - `src/concierge/agents/dispatcher.py` (only if additional hardening needed)
  - existing related tests if contract assertions require update

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.7]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 1 and state reset constraints]
- [Source: src/concierge/agents/dispatcher.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Targeted validation:
  - `pytest tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_3_5_dispatcher_orchestration.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_2_2_node_stub_wiring.py -q`
  - Result: 23 passed
- Full regression:
  - `pytest tests -q`
  - Result: 102 passed, 2 skipped

### Completion Notes List

- Added Story 3.7 unit coverage for per-turn freshness, specialist-entry freshness, full-history ownership, and dispatch-overhead threshold.
- Hardened fallback graph execution to route specialists from Dispatcher's current-turn result.
- Updated compiled-graph executed-node reporting to reflect resolved post-dispatch route.
- Kept Story 3.5 orchestration and Story 3.6 node-boundary error behavior passing.
- Code-review fixes applied: fallback now activates only for missing LangGraph dependency, executed-node tracking now captures actual node traversal in compiled path, and NFR3 performance test now validates repeated-run behavior.

### File List

- _bmad-output/implementation-artifacts/3-7-implement-per-turn-data-guarantee-and-conversation-history-ownership.md (created and updated in working tree)
- _bmad-output/implementation-artifacts/sprint-status.yaml (updated in working tree)
- src/concierge/graph/__init__.py (created/updated in working tree)
- tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py (created in working tree)

## Senior Developer Review (AI)

### Review Date

2026-02-25

### Outcome

Approve

### Findings and Resolution

- [x] [HIGH] Story file traceability mismatch vs git baseline (untracked workspace state) resolved by explicit working-tree classification in File List.
- [x] [HIGH] Overbroad graph fallback exception handling narrowed to missing-LangGraph dependency only.
- [x] [MEDIUM] `_executed_nodes` synthesized-path risk resolved by real node-execution tracking wrapper in compiled graph nodes.
- [x] [MEDIUM] NFR3 performance validation strengthened from single sample to repeated measurements.

### Validation Summary

- Targeted validation: 10 passed
- Full regression: 102 passed, 2 skipped

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 3.7 AC coverage and fallback graph route hardening; validated with targeted and full regression; moved status to review.
- 2026-02-25: Code review completed; HIGH/MEDIUM findings fixed automatically; status moved to done.
