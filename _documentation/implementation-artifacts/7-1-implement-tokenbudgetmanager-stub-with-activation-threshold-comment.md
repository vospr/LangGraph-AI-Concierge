# Story 7.1: Implement `TokenBudgetManager` Stub with Activation Threshold Comment

Status: review

## Story

As a **developer**,
I want the `TokenBudgetManager` stub to declare the activation threshold explicitly in a code comment,
so that the stub communicates production-readiness and sets expectations for future implementation.

## Acceptance Criteria

1. **Given** `agents/token_budget_manager.py`, **When** I read it, **Then** it contains a `TokenBudgetManager` class with a `check_and_summarize(history: list[Message]) -> list[Message]` method
2. **Given** the stub, **When** I read the docstring/comment, **Then** it states: `# Stub implementation. In production, summarize when token count exceeds 6000 (leaving 2000 for output). Activation threshold: 80% of model context window.`
3. **Given** the stub method, **When** called, **Then** it returns the history unchanged (no-op in MVP), but the interface and activation threshold are documented
4. **And** a `@property` in the method reads from config (deferred to future) or a hardcoded threshold marked with `# TODO: make configurable`

## Tasks / Subtasks

- [x] Task 1: Add Story 7.1 tests (AC: 1-4)
  - [x] 1.1: Create `tests/unit/test_story_7_1_token_budget_manager_stub.py`
  - [x] 1.2: Verify interface signature for `check_and_summarize(history: list[Message]) -> list[Message]`
  - [x] 1.3: Verify activation-threshold comment text is present in source
  - [x] 1.4: Verify MVP no-op behavior and threshold property TODO marker

- [x] Task 2: Implement `TokenBudgetManager` stub (AC: 1-4)
  - [x] 2.1: Create `src/concierge/agents/token_budget_manager.py` with `Message` type and `TokenBudgetManager` class
  - [x] 2.2: Add exact stub comment with `6000` threshold and `80%` activation note
  - [x] 2.3: Add hardcoded threshold `@property` marked with `# TODO: make configurable`
  - [x] 2.4: Ensure `check_and_summarize(...)` returns history unchanged

- [x] Task 3: Validate and finalize
  - [x] 3.1: Run Story 7.1 targeted tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update sprint status to review

## Dev Notes

### Guardrails

- Story 7.1 is a contract-first stub story; behavior remains no-op in MVP.
- The activation threshold must be explicit to signal production-ready design intent.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 7.1]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 7.1 targeted validation:
  - `pytest tests/unit/test_story_7_1_token_budget_manager_stub.py -q`
  - Result: 4 passed
- Full regression:
  - `pytest tests -q`
  - Result: 174 passed, 2 skipped

### Completion Notes List

- Added `TokenBudgetManager` stub with explicit activation-threshold contract and no-op MVP behavior.
- Added Story 7.1 unit tests for signature contract, exact threshold comment text, no-op semantics, and threshold property TODO marker.
- Updated sprint status to mark Epic 7 as in-progress and Story 7.1 as review.

### File List

- _bmad-output/implementation-artifacts/7-1-implement-tokenbudgetmanager-stub-with-activation-threshold-comment.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/token_budget_manager.py (created)
- tests/unit/test_story_7_1_token_budget_manager_stub.py (created)

## Change Log

- 2026-02-25: Story file initialized; Story 7.1 implementation and tests added.
- 2026-02-25: Story 7.1 validations passed; status moved to review.
