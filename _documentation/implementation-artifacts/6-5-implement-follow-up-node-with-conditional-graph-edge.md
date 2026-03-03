# Story 6.5: Implement Follow-Up Node with Conditional Graph Edge

Status: review

## Story

As a **developer**,
I want the Follow-Up node to run conditionally AFTER Research Agent completes (not after RAG),
so that proactive suggestions are offered when research-driven answers are delivered.

## Acceptance Criteria

1. **Given** Dispatcher route `research`, **When** graph executes, **Then** flow includes Follow-Up
2. **Given** non-research routes (`rag`, `booking_stub`, fallback), **When** graph executes, **Then** Follow-Up is skipped
3. **Given** Follow-Up triggers, **When** it runs, **Then** it sets:
   `"Based on your interest in Southeast Asia, you might also want to explore mountain retreats. Should I research that for you?"`
4. **Given** suggestion generation, **When** update is emitted, **Then** `proactive_suggestion` is set and `trace("followup", event="suggestion_generated")` is called
5. **And** graph source documents research-only conditional edge rationale

## Tasks / Subtasks

- [x] Task 1: Add Story 6.5 tests (AC: all)
  - [x] 1.1: Create `tests/unit/test_story_6_5_followup_conditional_edge.py`
  - [x] 1.2: Add follow-up agent suggestion + trace test
  - [x] 1.3: Add graph sequence test for research vs rag/booking routes
  - [x] 1.4: Add source-comment assertion for conditional-edge rationale

- [x] Task 2: Implement conditional edge and follow-up behavior (AC: all)
  - [x] 2.1: Implement `FollowUpAgent` generation logic for `route=="research"` only
  - [x] 2.2: Emit follow-up suggestion trace event
  - [x] 2.3: Add `should_run_followup(state)` helper in `graph/__init__.py`
  - [x] 2.4: Route synthesis via conditional edge to `followup` only for research; otherwise end
  - [x] 2.5: Update fallback graph execution path sequencing for research-only follow-up

- [x] Task 3: Align existing route-sequence tests to new topology (AC: 1, 2)
  - [x] 3.1: Update legacy tests that expected `followup` for all routes
  - [x] 3.2: Keep research-route follow-up expectations intact

- [x] Task 4: Validate and finalize (AC: all)
  - [x] 4.1: Run Story 6.5 + impacted route-sequence regressions
  - [x] 4.2: Run full suite `pytest tests -q`
  - [x] 4.3: Update sprint status to review

## Dev Notes

### Guardrails

- Follow-up is now strictly route-conditioned at graph level (`research` only).
- Follow-up agent also guards against handoff and guardrail-failed paths.
- Existing node-boundary trace-once and error handling contracts remain unchanged.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.5]
- [Source: src/concierge/graph/__init__.py]
- [Source: src/concierge/agents/followup.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_6_5_followup_conditional_edge.py -q`
  - Result: 3 failed
- Story 6.5 + impacted routing regression:
  - `pytest tests/unit/test_story_6_5_followup_conditional_edge.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py tests/unit/test_story_6_4_booking_stub_contract.py tests/unit/test_story_5_4_research_degradation.py -q`
  - Result: 35 passed
- Full regression:
  - `pytest tests -q`
  - Result: 167 passed, 2 skipped

### Completion Notes List

- Implemented follow-up suggestion generation and trace emission in `FollowUpAgent`.
- Implemented route-aware graph conditional edge (`should_run_followup`) with explicit architecture comment.
- Updated fallback and compiled graph paths to skip follow-up on non-research routes.
- Updated pre-existing route sequence tests to reflect the new conditional topology.

### File List

- _bmad-output/implementation-artifacts/6-5-implement-follow-up-node-with-conditional-graph-edge.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/followup.py (modified)
- src/concierge/graph/__init__.py (modified)
- tests/unit/test_story_6_5_followup_conditional_edge.py (created)
- tests/unit/test_story_2_2_node_stub_wiring.py (modified)
- tests/unit/test_story_3_6_node_boundary_error_handling.py (modified)
- tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py (modified)
- tests/unit/test_story_6_2_out_of_domain_deflection.py (modified)
- tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py (modified)
- tests/unit/test_story_6_4_booking_stub_contract.py (modified)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented research-only follow-up conditional routing and proactive suggestion flow; updated affected graph-sequence tests; validated targeted and full regression; moved status to review.
