# Story 6.6: Implement `system_summary` Message Filtering in Response Synthesis

Status: review

## Story

As a **developer**,
I want Response Synthesis to filter out `role: system_summary` messages from `conversation_history` before synthesis context is consumed,
so that internal memory-management content never leaks into user-facing responses.

## Acceptance Criteria

1. **Given** `conversation_history` containing `role="system_summary"`, **When** Response Synthesis runs, **Then** it creates a filtered copy excluding those messages
2. **Given** filtered history consumption, **When** synthesis context is built, **Then** only user/assistant messages are considered
3. **Given** final response output, **When** returned, **Then** no `[SUMMARY]` markers or summary text appear in user-facing content
4. **And** filtering is applied per-turn (Turn 5 summary does not leak to Turn 6 synthesis context)

## Tasks / Subtasks

- [x] Task 1: Add Story 6.6 tests (AC: all)
  - [x] 1.1: Create `tests/unit/test_story_6_6_system_summary_filtering.py`
  - [x] 1.2: Add filtered-history contract test asserting `system_summary` exclusion
  - [x] 1.3: Add no-summary-leak output test (`[SUMMARY]` and summary content absent)
  - [x] 1.4: Add per-turn independence test for Turn 5/Turn 6 filtering behavior

- [x] Task 2: Validate implementation behavior against story contract (AC: all)
  - [x] 2.1: Confirm `ResponseSynthesisAgent._filter_history(...)` enforces `role != "system_summary"`
  - [x] 2.2: Confirm filtered history is the only context passed into synthesis text construction
  - [x] 2.3: Confirm no additional code changes required beyond contract-hardening tests

- [x] Task 3: Validate and finalize
  - [x] 3.1: Run Story 6.6 + Story 5.5 synthesis compatibility tests
  - [x] 3.2: Run impacted Epic-6 regression slice
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Story 6.6 behavior was already implemented in `ResponseSynthesisAgent._filter_history(...)` from prior synthesis work.
- This story formalizes and locks the contract with dedicated tests, including per-turn filtering assertions.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.6]
- [Source: src/concierge/agents/response_synthesis.py]
- [Source: tests/unit/test_story_6_6_system_summary_filtering.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 6.6 validation:
  - `pytest tests/unit/test_story_6_6_system_summary_filtering.py tests/unit/test_story_5_5_response_synthesis_blending.py -q`
  - Result: 8 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_6_6_system_summary_filtering.py tests/unit/test_story_6_5_followup_conditional_edge.py tests/unit/test_story_6_4_booking_stub_contract.py tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_state_reset.py tests/unit/test_trace.py -q`
  - Result: 30 passed
- Full regression:
  - `pytest tests -q`
  - Result: 170 passed, 2 skipped

### Completion Notes List

- Added Story 6.6 dedicated unit coverage for summary-message filtering and per-turn independence.
- Verified that existing synthesis filtering implementation fully satisfies Story 6.6 AC without additional source-code changes.

### File List

- _bmad-output/implementation-artifacts/6-6-implement-system-summary-message-filtering-in-response-synthesis.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_6_6_system_summary_filtering.py (created)

## Change Log

- 2026-02-25: Story file initialized and validation started.
- 2026-02-25: Added Story 6.6 contract-focused tests; validated targeted and full regression; moved status to review.
