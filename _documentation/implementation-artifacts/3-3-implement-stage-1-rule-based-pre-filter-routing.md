# Story 3.3: Implement Stage 1 Rule-Based Pre-Filter Routing

Status: review

## Story

As a **developer**,
I want the Dispatcher's Stage 1 to load `routing_rules.yaml`, keyword-match user input, and route directly if confidence is above `escalation_threshold`,
so that deterministic intents do not consume LLM budget.

## Acceptance Criteria

1. **Given** `routing_rules.yaml`, **When** loaded at startup, **Then** it parses into a valid rule list with `intent`, `route`, `pattern`, and confidence score fields
2. **Given** user input `"I want to book a flight"`, **When** Stage 1 checks rules, **Then** booking keyword match resolves booking intent with confidence `0.95`
3. **Given** confidence `0.95` and `escalation_threshold=0.72`, **When** Stage 1 runs, **Then** it returns `route="booking_stub"` without invoking Stage 2 LLM
4. **Given** user input `"something else"`, **When** no rule keyword matches, **Then** confidence is `0.0` and routing escalates to Stage 2
5. **Given** Stage 1 direct routing, **When** it routes directly, **Then** `trace("dispatcher", intent=X, confidence=Y, route=Z, stage="pre_filter")` is emitted
6. **And** `config/routing_rules.yaml` keeps inline comments explaining every rule's purpose

## Tasks / Subtasks

- [x] Task 1: Add Stage 1 pre-filter tests before implementation (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_3_3_stage1_prefilter.py`
  - [x] 1.2: Add startup loading contract test for escalation threshold and non-empty rules
  - [x] 1.3: Add booking-input deterministic routing test validating direct route and pre-filter trace
  - [x] 1.4: Add no-match escalation test validating `confidence=0.0` and `route=None`

- [x] Task 2: Implement Dispatcher Stage 1 pre-filter routing (AC: 1, 2, 3, 4, 5)
  - [x] 2.1: Extend `DispatcherAgent` to load and validate `config/routing_rules.yaml` at initialization
  - [x] 2.2: Implement Stage 1 rule evaluation with regex matching and highest-confidence selection
  - [x] 2.3: Route directly only when matched confidence meets `escalation_threshold`
  - [x] 2.4: Emit centralized trace for direct Stage 1 route with `stage="pre_filter"`
  - [x] 2.5: Preserve existing graph stub behavior by no-oping when route is already pre-populated

- [x] Task 3: Align Stage 1 config and validate regression safety (AC: 2, 3, 6)
  - [x] 3.1: Update booking rule confidence and intent naming in `config/routing_rules.yaml`
  - [x] 3.2: Keep escalation threshold distinct from per-agent confidence thresholds
  - [x] 3.3: Run targeted and full test suites and confirm no regressions

## Dev Notes

### Implementation Guardrails

- Stage 1 is deterministic and file-driven; no network or LLM call required.
- `DispatcherAgent` loads routing config once on initialization and reuses compiled regex rules.
- Pre-filter trace emission uses centralized `trace()` to preserve observability consistency and field allowlist compliance.

### Previous Story Intelligence

- Story 3.1 introduced `reset_turn_state()` and deterministic turn-reset contracts.
- Story 3.2 introduced centralized safe `trace()` and node seam trace-call conventions.
- Story 2.2 graph fallback path depends on pre-populated route behavior for stub route-path tests.

### Testing Notes

- Added pure unit tests for startup rule loading, deterministic booking route, and no-match escalation.
- Full regression suite rerun to ensure no breakage across prior story contracts.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.3]
- [Source: _bmad-output/planning-artifacts/architecture.md#Dispatcher Hybrid Routing Architecture]
- [Source: spec/concierge-spec.md#Routing]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_3_3_stage1_prefilter.py -q` -> 3 failed (`DispatcherAgent` missing Stage 1 contracts).
- Green phase: implemented YAML-backed Stage 1 loader, deterministic pre-filter matcher, threshold gating, and direct-route trace emission in `src/concierge/agents/dispatcher.py`.
- Green phase: updated `config/routing_rules.yaml` booking intent confidence and threshold tuning.
- Targeted validation: `pytest tests/unit/test_story_3_3_stage1_prefilter.py -q` -> 3 passed.
- Regression validation: `pytest tests -q` -> initially failed (`escalation_threshold` duplicated policy threshold); adjusted threshold to `0.72`.
- Final regression: `pytest tests -q` -> 82 passed, 2 skipped.

### Completion Notes List

- Implemented Stage 1 rule-based dispatcher pre-filter with startup rule loading and deterministic route selection.
- Added dedicated Story 3.3 unit tests covering direct booking route and Stage 2 escalation path when no rule matches.
- Preserved existing graph stub contracts while introducing Stage 1 routing behavior.

### File List

- _bmad-output/implementation-artifacts/3-3-implement-stage-1-rule-based-pre-filter-routing.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/dispatcher.py (modified)
- config/routing_rules.yaml (modified)
- tests/unit/test_story_3_3_stage1_prefilter.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented Stage 1 pre-filter routing, added unit coverage, reran full regression, and moved status to review.
