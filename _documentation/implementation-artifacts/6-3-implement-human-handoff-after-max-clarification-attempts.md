# Story 6.3: Implement Human Handoff After Max Clarification Attempts

Status: review

## Story

As a **developer**,
I want the system to track clarification attempts per session and route to human handoff when the limit is exceeded,
so that users stuck in clarification loops get escalated to human support gracefully.

## Acceptance Criteria

1. **Given** `max_clarifications=3`, **When** 3 clarification questions were already asked, **Then** `human_handoff=True`
2. **Given** human handoff triggered, **When** terminal response is generated, **Then** it ends with: `"I'm having trouble understanding your request. A human travel specialist can assist - please wait or contact support."`
3. **Given** handoff flow, **When** graph runs, **Then** it remains non-crashing and completes gracefully
4. **And** `trace("guardrail", event="human_handoff", clarification_count=3, session_id=X)` is emitted
5. **Given** session clarifications, **When** state is inspected, **Then** `max_clarifications` is present from guardrail policy

## Tasks / Subtasks

- [x] Task 1: Add Story 6.3 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py`
  - [x] 1.2: Add guardrail-unit test for max-attempt handoff trigger + trace payload
  - [x] 1.3: Add below-max test to preserve clarification flow
  - [x] 1.4: Add graph-level terminal handoff message test

- [x] Task 2: Implement clarification-loop escalation behavior (AC: all)
  - [x] 2.1: Add clarification-attempt counting from session `conversation_history`
  - [x] 2.2: Trigger handoff when prior clarification count reaches `max_clarifications`
  - [x] 2.3: Emit guardrail `human_handoff` trace with `clarification_count` and `session_id`
  - [x] 2.4: Include `max_clarifications` in guardrail updates
  - [x] 2.5: Preserve upstream handoff state (do not clear dispatcher/node-error handoff)
  - [x] 2.6: Update response synthesis to preserve explicit handoff text when provided by guardrail

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run Story 6.3 + 6.1 + 6.2 + node-boundary regression tests
  - [x] 3.2: Run impacted graph/synthesis/dispatcher/state/trace slice
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Clarification count is derived from persisted `conversation_history` assistant clarification messages.
- Handoff remains non-terminal at graph engine level; session ends gracefully with message.
- Existing dispatcher-error handoff behavior is preserved by guardrail no-op when `human_handoff` is already set.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.3]
- [Source: src/concierge/agents/guardrail.py]
- [Source: src/concierge/agents/response_synthesis.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py -q`
  - Result: 3 failed (expected before implementation)
- Story 6.3 + guardrail regression:
  - `pytest tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_6_2_out_of_domain_deflection.py -q`
  - Result: 18 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_story_3_5_dispatcher_orchestration.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_state_reset.py tests/unit/test_trace.py -q`
  - Result: 34 passed
- Full regression:
  - `pytest tests -q`
  - Result: 161 passed, 2 skipped

### Completion Notes List

- Implemented max-clarification handoff escalation in `GuardrailAgent` using session history-derived attempt count.
- Added explicit handoff terminal message and propagated `max_clarifications` in guardrail update payload.
- Added guardrail trace event for human handoff with clarification count and session id.
- Updated response synthesis to preserve pre-built handoff message from guardrail while retaining existing error-path suffix behavior.
- Added Story 6.3 test coverage for threshold crossing, below-threshold behavior, and graph-level graceful completion.

### File List

- _bmad-output/implementation-artifacts/6-3-implement-human-handoff-after-max-clarification-attempts.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/guardrail.py (modified)
- src/concierge/agents/response_synthesis.py (modified)
- tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented max-clarification handoff escalation and terminal message preservation; validated targeted and full regression; moved status to review.
