# Story 6.2: Implement Out-of-Domain Detection and Deflection

Status: review

## Story

As a **developer**,
I want the Guardrail node to detect when a query is out-of-domain and return a labeled, friendly deflection,
so that users understand system boundaries without a hard stop.

## Acceptance Criteria

1. **Given** query `"What's the weather in London?"`, **When** Guardrail evaluates out-of-domain context, **Then** it detects out-of-domain intent under low confidence (`<0.4`)
2. **Given** out-of-domain detection, **When** it occurs, **Then** `guardrail_passed=False` and a friendly deflection response is prepared
3. **Given** deflection emission, **When** returned, **Then** it offers a travel-relevant alternative
4. **And** `trace("guardrail", event="out_of_domain", confidence=0.32, query="weather london")` is emitted
5. **Given** the deflection path, **When** graph execution completes, **Then** the session remains active (no forced handoff/termination)

## Tasks / Subtasks

- [x] Task 1: Add Story 6.2 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_6_2_out_of_domain_deflection.py`
  - [x] 1.2: Add guardrail-unit test for weather query deflection payload + trace
  - [x] 1.3: Add graph-level test proving deflection response flows through synthesis/followup without ending session

- [x] Task 2: Implement out-of-domain deflection logic in Guardrail (AC: all)
  - [x] 2.1: Add out-of-domain gate for low-confidence (`<0.4`) intent/query conditions
  - [x] 2.2: Add friendly deflection response template with travel alternative
  - [x] 2.3: Add query normalization for trace payload (`weather london`)
  - [x] 2.4: Keep clarification flow from Story 6.1 intact for non-out-of-domain low-confidence cases

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run Story 6.2 + Story 6.1 + node-boundary regression tests
  - [x] 3.2: Run impacted graph/synthesis/dispatcher/state/trace slice
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Out-of-domain deflection is non-terminal (`human_handoff=False`) per story intent.
- Detection currently uses low-confidence plus intent/query signal (`intent=="out_of_domain"` or weather-query heuristic).
- Response synthesis behavior required no changes because existing success-path preserves pre-set `current_response`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 6.2]
- [Source: src/concierge/agents/guardrail.py]
- [Source: src/concierge/agents/response_synthesis.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_6_2_out_of_domain_deflection.py -q`
  - Result: 2 failed (expected before implementation)
- Story 6.2 validation:
  - `pytest tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_3_6_node_boundary_error_handling.py -q`
  - Result: 15 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_6_2_out_of_domain_deflection.py tests/unit/test_story_6_1_guardrail_clarification.py tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_story_3_5_dispatcher_orchestration.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_state_reset.py tests/unit/test_trace.py -q`
  - Result: 31 passed
- Full regression:
  - `pytest tests -q`
  - Result: 158 passed, 2 skipped

### Completion Notes List

- Implemented out-of-domain deflection branch in `GuardrailAgent` for low-confidence out-of-domain/weather queries.
- Added normalized out-of-domain trace payload with `query` and `confidence`.
- Added deflection message with travel-specific alternative suggestion.
- Preserved Story 6.1 clarification behavior and existing node-boundary error handling contracts.

### File List

- _bmad-output/implementation-artifacts/6-2-implement-out-of-domain-detection-and-deflection.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/guardrail.py (modified)
- tests/unit/test_story_6_2_out_of_domain_deflection.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented out-of-domain detection/deflection with trace normalization and graph-path validation; set status to review.
