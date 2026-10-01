# Story 3.4: Implement Stage 2 LLM-Based Escalation and Intent Classification

Status: review

## Story

As a **developer**,
I want the Dispatcher's Stage 2 to invoke Claude for ambiguous intents, parse structured routing output (`intent` + `confidence`), and decide whether to route or escalate to fallback,
so that hybrid routing works for queries that Stage 1 cannot classify confidently.

## Acceptance Criteria

1. **Given** user input with low confidence from Stage 1, **When** Stage 2 runs, **Then** `anthropic.Anthropic().messages.create()` is called with the configured Dispatcher model
2. **Given** the Dispatcher prompt, **When** I read `prompts/dispatcher/v1.yaml`, **Then** it explicitly instructs JSON output with `intent` and `confidence` fields only
3. **Given** LLM response `{"intent":"destination_research","confidence":0.84}`, **When** parsed, **Then** dispatcher state updates set `intent` and `confidence`
4. **Given** confidence `0.84` and `confidence_threshold=0.75`, **When** Stage 2 completes, **Then** route is set to `research`
5. **Given** confidence `0.61` (below threshold), **When** Stage 2 completes, **Then** route is set to `fallback` (guardrail path)
6. **Given** Stage 2 routing, **When** it completes, **Then** `trace("dispatcher", intent=X, confidence=Y, stage="llm_escalation")` is emitted

## Tasks / Subtasks

- [x] Task 1: Add Stage 2 escalation tests before implementation (AC: 1, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_3_4_stage2_llm_escalation.py`
  - [x] 1.2: Add test verifying Anthropic call uses dispatcher policy model and token cap
  - [x] 1.3: Add test verifying high-confidence Stage 2 intent routes to `research`
  - [x] 1.4: Add test verifying low-confidence Stage 2 intent routes to `fallback`
  - [x] 1.5: Add test verifying Stage 2 trace includes `stage="llm_escalation"`

- [x] Task 2: Implement Stage 2 LLM escalation in dispatcher agent (AC: 1, 3, 4, 5, 6)
  - [x] 2.1: Load Dispatcher policy (`model`, `max_tokens`, `confidence_threshold`, `prompt_version`) at agent initialization
  - [x] 2.2: Load and compose dispatcher prompt from `prompts/dispatcher/{prompt_version}.yaml`
  - [x] 2.3: Invoke `anthropic.Anthropic().messages.create(...)` for Stage 2 when Stage 1 does not resolve a route
  - [x] 2.4: Parse LLM JSON response and apply thresholded route decision
  - [x] 2.5: Emit Stage 2 trace entry with intent/confidence/route and stage marker

- [x] Task 3: Update prompt contract and validate regressions (AC: 2)
  - [x] 3.1: Update `prompts/dispatcher/v1.yaml` output contract to `intent` + `confidence` only
  - [x] 3.2: Preserve Stage 1 behavior and graph route prepopulation contract
  - [x] 3.3: Run targeted and full test suites with no regressions

## Dev Notes

### Implementation Guardrails

- Stage 2 only runs when Stage 1 does not produce a direct route.
- Stage 2 model and threshold values are loaded from `prompts/dispatcher/policy.yaml`.
- JSON parsing is resilient to wrapper text around JSON blocks.
- Routing remains graph-compatible (`rag`, `research`, `booking_stub`, `fallback`).

### Previous Story Intelligence

- Story 3.3 introduced deterministic Stage 1 pre-filter and startup route-rule loading.
- Story 3.2 introduced centralized trace formatting and field controls.
- Story 2.2 tests require route-preserving behavior when graph pre-populates `state["route"]`.

### Testing Notes

- New Stage 2 tests use a fake `anthropic` module injected via `sys.modules` (pure unit approach).
- Full suite rerun confirms no regressions in prior stories.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.4]
- [Source: _bmad-output/planning-artifacts/architecture.md#Dispatcher Hybrid Routing Architecture]
- [Source: prompts/dispatcher/policy.yaml]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase (new tests first): added `tests/unit/test_story_3_4_stage2_llm_escalation.py`.
- Green phase: implemented Stage 2 escalation flow in `src/concierge/agents/dispatcher.py`:
  - dispatcher policy and prompt loading
  - LLM invocation via Anthropic client
  - structured response parse (`intent`, `confidence`)
  - threshold-based route decision (`research` or `fallback`)
  - Stage 2 trace emission with `stage="llm_escalation"`
- Prompt contract update: `prompts/dispatcher/v1.yaml` now requires JSON with `intent` and `confidence` only.
- Targeted validation: `pytest tests/unit/test_story_3_3_stage1_prefilter.py tests/unit/test_story_3_4_stage2_llm_escalation.py -q` -> 6 passed.
- Full regression: `pytest tests -q` -> 85 passed, 2 skipped.

### Completion Notes List

- Implemented Story 3.4 Stage 2 LLM escalation with policy-driven model/threshold and structured parsing.
- Added deterministic unit coverage for Anthropic invocation, high/low confidence routing, and trace stage marker.
- Preserved Story 3.3 and graph stub route contracts while extending dispatcher capabilities.

### File List

- _bmad-output/implementation-artifacts/3-4-implement-stage-2-llm-based-escalation-and-intent-classification.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/dispatcher.py (modified)
- prompts/dispatcher/v1.yaml (modified)
- tests/unit/test_story_3_4_stage2_llm_escalation.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented Stage 2 LLM escalation, updated dispatcher prompt output contract, added unit coverage, and moved status to review.
