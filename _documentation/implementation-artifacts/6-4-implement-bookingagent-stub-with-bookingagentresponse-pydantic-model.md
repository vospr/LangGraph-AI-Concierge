# Story 6.4: Implement BookingAgent Stub with `BookingAgentResponse` Pydantic Model

Status: review

## Story

As a **developer**,
I want the BookingAgent stub to return a `BookingAgentResponse` Pydantic model with a visible integration contract,
so that booking behavior is explicit and future wiring is unambiguous.

## Acceptance Criteria

1. **Given** `booking_agent.py`, **When** inspected, **Then** `BookingAgentResponse` is defined with fields: `status`, `message`, `integration_point`, `required_env_vars`
2. **Given** booking query, **When** BookingAgent runs, **Then** it returns:
   `status="unavailable"`, integration message, integration point, and required env vars
3. **Given** stub response, **When** response synthesis renders booking output, **Then** integration contract details are visible in user-facing response
4. **Given** integration point field, **When** future developers inspect output, **Then** real service swap guidance is explicit
5. **And** `trace("booking_agent", event="unavailable", message="stub_integration_contract")` is called

## Tasks / Subtasks

- [x] Task 1: Add Story 6.4 tests (AC: 1, 2, 3, 5)
  - [x] 1.1: Create `tests/unit/test_story_6_4_booking_stub_contract.py`
  - [x] 1.2: Add model-contract field test for `BookingAgentResponse`
  - [x] 1.3: Add booking-agent run test validating payload + trace
  - [x] 1.4: Add graph-level synthesis visibility test for integration contract output

- [x] Task 2: Implement BookingAgent stub contract (AC: all)
  - [x] 2.1: Add `BookingAgentResponse` Pydantic model in booking agent
  - [x] 2.2: Return unavailability payload with explicit integration point/env vars
  - [x] 2.3: Emit booking unavailable trace event
  - [x] 2.4: Extend response synthesis booking rendering to include integration contract visibility

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run Story 6.4 + Story 5.5 booking compatibility tests
  - [x] 3.2: Run impacted graph/node-boundary/guardrail/synthesis regression slice
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Booking remains explicit stub behavior (never fakes booking success).
- Response synthesis still prioritizes booking message, now appending integration metadata for transparency.
- Existing Story 5.5 booking formatting contract (`startswith`) preserved.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.4]
- [Source: src/concierge/agents/booking_agent.py]
- [Source: src/concierge/agents/response_synthesis.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_6_4_booking_stub_contract.py -q`
  - Result: 3 failed (expected before implementation)
- Story 6.4 validation:
  - `pytest tests/unit/test_story_6_4_booking_stub_contract.py tests/unit/test_story_5_5_response_synthesis_blending.py -q`
  - Result: 8 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_6_4_booking_stub_contract.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_story_6_3_human_handoff_after_max_clarifications.py tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_trace.py -q`
  - Result: 37 passed
- Full regression:
  - `pytest tests -q`
  - Result: 164 passed, 2 skipped

### Completion Notes List

- Added `BookingAgentResponse` model and stub unavailability payload with integration contract fields.
- Added booking unavailable trace emission with story-defined event metadata.
- Updated booking synthesis rendering to include integration point and required env vars in final output.
- Added Story 6.4 coverage for model contract, stub payload, trace, and graph-path visibility.

### File List

- _bmad-output/implementation-artifacts/6-4-implement-bookingagent-stub-with-bookingagentresponse-pydantic-model.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/booking_agent.py (modified)
- src/concierge/agents/response_synthesis.py (modified)
- tests/unit/test_story_6_4_booking_stub_contract.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented BookingAgent Pydantic stub contract and synthesis visibility; validated targeted and full regression; moved status to review.
