# Story 3.1: Implement `reset_turn_state()` Helper and Stale-State Unit Test

Status: review

## Story

As a **developer**,
I want `reset_turn_state(state)` to explicitly reset all sub-agent fields to `None`/`[]` at turn start, and want a unit test proving that stale data never bleeds across turns,
so that the stale-state bug is architecturally impossible.

## Acceptance Criteria

1. **Given** `agents/dispatcher.py`, **When** I read `reset_turn_state()`, **Then** it resets these fields: `rag_results`, `research_results`, `source_attribution`, `clarification_question`, `proactive_suggestion`, `error`, `human_handoff`, `guardrail_passed`, and all per-turn routing fields
2. **Given** `validate_config.py`, **When** I run the static check, **Then** it asserts that every turn-reset contract field appears in `reset_turn_state()`
3. **Given** `tests/unit/test_state_reset.py`, **When** I run it, **Then** a test verifies: Turn 1 sets `rag_results = [KB Entry]`, Turn 2 calls `reset_turn_state()`, Turn 2 route check sees `rag_results = None` (no bleed)
4. **Given** the stale-state test, **When** it runs, **Then** it passes on 100% of executions (no non-determinism)
5. **And** `tests/conftest.py` provides a fixture for a fresh `ConciergeState` dict with optional output fields initialized

## Tasks / Subtasks

- [x] Task 1: Add contract-first stale-state and static-check tests (AC: 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_state_reset.py`
  - [x] 1.2: Add test for `reset_turn_state()` return payload completeness and deterministic reset values
  - [x] 1.3: Add stale-state test proving Turn 1 `rag_results` does not bleed into Turn 2 after reset
  - [x] 1.4: Add test asserting `validate_config` reset-contract static check passes
  - [x] 1.5: Add `tests/conftest.py` fixture for fresh `ConciergeState`

- [x] Task 2: Implement reset helper and typed reset contract (AC: 1, 2)
  - [x] 2.1: Add `TurnResetUpdate` TypedDict contract to `src/concierge/state.py`
  - [x] 2.2: Implement `reset_turn_state(state)` in `src/concierge/agents/dispatcher.py`
  - [x] 2.3: Keep `reset_turn_state()` deterministic and side-effect free (returns update payload only)
  - [x] 2.4: Preserve current Story 2.x graph stub behavior while introducing helper

- [x] Task 3: Strengthen validate-config static reset contract check (AC: 2)
  - [x] 3.1: Update `validate_config.check_reset_turn_state_contract_non_blocking(...)` to compare reset fields against typed reset contract definition
  - [x] 3.2: Keep diagnostics actionable when fields are missing in `reset_turn_state()`

- [x] Task 4: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5)
  - [x] 4.1: Run `pytest tests/unit/test_state_reset.py -q`
  - [x] 4.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 4.3: Update story `Dev Agent Record`, `File List`, and `Change Log`
  - [x] 4.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Keep reset semantics in one helper: `reset_turn_state()` returns a reset payload and does not mutate global/session state by side effect.
- Reset only turn-scoped and sub-agent output fields; session identity and memory profile remain session-owned.
- Preserve Story 2.2 contracts while adding Dispatcher reset helper (do not break deterministic stub path tests).
- Static check should be syntax-level (no runtime graph invocation required) and fail with explicit missing field names.

### Previous Story Intelligence

- Story 2.2 established deterministic graph stubs and route-path assertions that must not regress.
- Story 2.3/2.4 introduced `main.py` startup contracts but did not add Dispatcher routing logic yet; 3.1 should remain helper-focused.
- Current `validate_config` includes placeholder `reset_turn_state` presence check; this story converts it to contract completeness check.

### Testing Notes

- Use pure unit tests; no LLM calls and no network dependency.
- Prefer fixture-based fresh state setup from `tests/conftest.py` for repeatability.
- Assert exact reset payload equality to prevent partial/incomplete resets from silently passing.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.1]
- [Source: _bmad-output/planning-artifacts/architecture.md#`reset_turn_state()` — Single Source of Truth]
- [Source: spec/concierge-spec.md#§State — ConciergeState]
- [Source: spec/concierge-spec.md#Per-Node Update TypedDicts]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_state_reset.py -q` -> collection error (`reset_turn_state` missing in `concierge.agents.dispatcher`).
- Green phase: added `TurnResetUpdate` contract to `src/concierge/state.py`.
- Green phase: implemented deterministic `reset_turn_state(state)` helper in `src/concierge/agents/dispatcher.py`.
- Green phase: added `fresh_concierge_state` fixture to `tests/conftest.py`.
- Green phase: strengthened `validate_config.check_reset_turn_state_contract_non_blocking(...)` to statically compare reset helper fields against `TurnResetUpdate` via AST.
- Targeted validation: `pytest tests/unit/test_state_reset.py -q` -> 3 passed.
- Full regression: `pytest tests -q` -> 74 passed, 2 skipped.

### Completion Notes List

- Implemented Story 3.1 turn-reset helper and stale-state guard tests with deterministic reset payload assertions.
- Added typed reset contract so reset coverage is explicit and machine-checkable.
- Preserved Story 2.x graph stub behavior by introducing helper without changing dispatcher stub routing behavior yet.

### File List

- _bmad-output/implementation-artifacts/3-1-implement-reset-turn-state-helper-and-stale-state-unit-test.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_state_reset.py (created)
- tests/conftest.py (modified)
- src/concierge/state.py (modified)
- src/concierge/agents/dispatcher.py (modified)
- validate_config.py (modified)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented `reset_turn_state()` helper, stale-state tests, and static reset-contract validation; moved status to review after full suite pass.
