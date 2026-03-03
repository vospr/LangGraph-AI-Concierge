# Story 7.2: Implement Token Limit Detection and Turn Compression Logic (Stub)

Status: review

## Story

As a **developer**,
I want the system to detect when conversation context approaches the token limit, and have a documented path to compress oldest turns using `TokenBudgetManager`,
so that production scalability is architecturally clear even if not fully implemented in MVP.

## Acceptance Criteria

1. **Given** `agents/dispatcher.py`, **When** the Dispatcher calls `TokenBudgetManager.check_and_summarize()` before LLM invocation, **Then** the call checks if `len(conversation_history)` approaches a threshold (documented threshold: 80% of context window)
2. **Given** the stub in MVP, **When** the threshold is approached, **Then** it logs: `[TOKEN_BUDGET] Context approaching limit. In production, oldest turns would be summarized here.`
3. **Given** the compression logic, **When** triggered, **Then** `role: system_summary` messages are created (for Response Synthesis to filter), preserving key facts but reducing token count
4. **And** `trace("token_budget", event="check_performed", token_count=X, threshold=6000)` is called

## Tasks / Subtasks

- [x] Task 1: Add Story 7.2 tests (AC: 1-4)
  - [x] 1.1: Create `tests/unit/test_story_7_2_token_limit_and_compression_stub.py`
  - [x] 1.2: Validate Dispatcher invokes `TokenBudgetManager.check_and_summarize()` before Stage-2 path
  - [x] 1.3: Validate threshold-triggered logging and `system_summary` message creation
  - [x] 1.4: Validate `trace("token_budget", event="check_performed", token_count=X, threshold=6000)` call

- [x] Task 2: Implement Dispatcher and TokenBudgetManager updates (AC: 1-4)
  - [x] 2.1: Extend `TokenBudgetManager` with stub compression path that emits `system_summary` when threshold reached
  - [x] 2.2: Integrate token budget check in Dispatcher before Stage-2 LLM invocation
  - [x] 2.3: Emit required token-budget warning log line on compression trigger
  - [x] 2.4: Emit token-budget trace with token count and threshold

- [x] Task 3: Validate and finalize
  - [x] 3.1: Run Story 7.2 targeted tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update sprint status to review

## Dev Notes

### Guardrails

- Token counting remains approximate in MVP; threshold detection uses history length proxy.
- Story 7.2 introduces documented compression behavior to create `system_summary` records consumable by Story 6.6 filtering.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 7.2]
- [Source: src/concierge/agents/dispatcher.py]
- [Source: src/concierge/agents/token_budget_manager.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 7.2 targeted validation:
  - `pytest tests/unit/test_story_7_2_token_limit_and_compression_stub.py tests/unit/test_story_3_5_dispatcher_orchestration.py tests/unit/test_story_7_1_token_budget_manager_stub.py -q`
  - Result: 10 passed
- Full regression:
  - `pytest tests -q`
  - Result: 177 passed, 2 skipped

### Completion Notes List

- Added Dispatcher token-budget check on Stage-2 path before LLM invocation.
- Added token-budget trace event with token count and threshold, and expanded trace allowlist for `token_count`.
- Added stub compression behavior in `TokenBudgetManager` to emit a `system_summary` message and retain recent turns when threshold is reached.
- Added required token-budget warning log line when compression path is triggered.
- Updated existing dispatcher orchestration test expectations for the new token-budget trace behavior.

### File List

- _bmad-output/implementation-artifacts/7-2-implement-token-limit-detection-and-turn-compression-logic-stub.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/dispatcher.py (modified)
- src/concierge/agents/token_budget_manager.py (modified)
- src/concierge/trace.py (modified)
- tests/unit/test_story_3_5_dispatcher_orchestration.py (modified)
- tests/unit/test_story_7_2_token_limit_and_compression_stub.py (created)

## Change Log

- 2026-02-25: Story file initialized; implementation and tests started.
- 2026-02-25: Story 7.2 validations passed; status moved to review.
