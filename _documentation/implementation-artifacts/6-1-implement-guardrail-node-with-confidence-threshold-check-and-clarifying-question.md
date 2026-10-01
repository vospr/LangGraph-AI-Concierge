# Story 6.1: Implement Guardrail Node with Confidence Threshold Check and Clarifying Question

Status: review

## Story

As a **developer**,
I want the Guardrail node to check if Dispatcher confidence is below `confidence_threshold`, and if so, emit a single clarifying question to the user,
so that ambiguous intents are resolved before routing to a sub-agent.

## Acceptance Criteria

1. **Given** Dispatcher confidence `0.61` with threshold `0.75`, **When** Guardrail runs, **Then** `clarification_needed=True`
2. **Given** clarification needed, **When** Guardrail generates a question, **Then** it stores exactly one question in `clarification_question`
3. **Given** the clarifying question, **When** user responds on next turn, **Then** Dispatcher appends that user response to `conversation_history`
4. **Given** confidence at/above threshold, **When** Guardrail runs, **Then** it passes without clarification
5. **And** `trace("guardrail", event="clarification_fired", confidence=0.61, threshold=0.75)` is emitted

## Tasks / Subtasks

- [x] Task 1: Add Story 6.1 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_6_1_guardrail_clarification.py`
  - [x] 1.2: Add low-confidence clarification + trace payload test
  - [x] 1.3: Add high-confidence pass-through test
  - [x] 1.4: Add next-turn dispatcher history append assertion after clarification

- [x] Task 2: Implement Guardrail confidence-check behavior (AC: 1, 2, 4, 5)
  - [x] 2.1: Implement `GuardrailAgent` policy loading for dispatcher threshold and guardrail max clarifications
  - [x] 2.2: Add threshold comparison and clarification update payload
  - [x] 2.3: Emit `clarification_fired` trace with `confidence` and `threshold`
  - [x] 2.4: Return pass-through update when confidence is sufficient or unavailable

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run Story 6.1 + node-boundary regression tests
  - [x] 3.2: Run impacted dispatcher/graph/state/trace slice
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Uses dispatcher policy threshold (`0.75`) as clarification boundary for this story.
- Clarification question is a single deterministic prompt (one `?`).
- Leaves clarification-attempt counting/handoff escalation for Story 6.3.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.1]
- [Source: src/concierge/agents/guardrail.py]
- [Source: src/concierge/agents/dispatcher.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_6_1_guardrail_clarification.py -q`
  - Result: 2 failed, 1 passed (`trace`/guardrail behavior not implemented)
- Story 6.1 validation:
  - `pytest tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_3_6_node_boundary_error_handling.py -q`
  - Result: 13 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_3_5_dispatcher_orchestration.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_state_reset.py tests/unit/test_trace.py -q`
  - Result: 24 passed
- Full regression:
  - `pytest tests -q`
  - Result: 156 passed, 2 skipped

### Completion Notes List

- Implemented `GuardrailAgent` confidence threshold gate with dispatcher policy-driven threshold loading.
- Added deterministic single clarifying question update payload for below-threshold confidence.
- Added guardrail trace emission for clarification firing (`event`, `confidence`, `threshold`).
- Added Story 6.1 tests for low/high confidence paths and next-turn history append behavior.
- Preserved node-boundary exception handling behavior in `guardrail_node`.

### File List

- _bmad-output/implementation-artifacts/6-1-implement-guardrail-node-with-confidence-threshold-check-and-clarifying-question.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/guardrail.py (modified)
- tests/unit/test_story_6_1_guardrail_clarification.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented guardrail threshold clarification flow and validation coverage; validated targeted and full regression; moved status to review.
