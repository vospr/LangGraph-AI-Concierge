# Story 4.2: Implement Proactive Memory-Driven Greeting Before First User Input

Status: review

## Story

As a **developer**,
I want the system to generate and print a proactive greeting from the loaded profile before the user types anything,
so that the hiring manager sees the proactive outcome completion requirement fire automatically in the first few seconds.

## Acceptance Criteria

1. **Given** a loaded profile for Alex with past trips including Bali and Tokyo, **When** the session starts, **Then** greeting prints before any user input prompt: `Welcome back, Alex. Based on your March trip to Bali, you might be interested in upcoming deals to Southeast Asia.`
2. **Given** proactive greeting and `--fast-mode`, **When** session starts, **Then** greeting prints immediately after fast-mode banner
3. **Given** no profile loaded, **When** session starts, **Then** no proactive greeting prints and Story 4.1 warning behavior remains
4. **Given** greeting text, **When** inspected, **Then** it references actual profile data (trip month/destination/region), not generic placeholders
5. **Given** greeting generated, **When** emitted, **Then** `trace("memory", event="greeting_fired", user_id="alex")` is called

## Tasks / Subtasks

- [x] Task 1: Add Story 4.2 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_4_2_proactive_greeting.py`
  - [x] 1.2: Add startup test asserting greeting + trace emitted before loop
  - [x] 1.3: Add fast-mode ordering test (banner then greeting)
  - [x] 1.4: Add no-profile test asserting no greeting
  - [x] 1.5: Add greeting-content test asserting profile-derived values

- [x] Task 2: Implement proactive greeting generation + startup emission (AC: 1, 2, 3, 4, 5)
  - [x] 2.1: Add greeting formatter in memory service using profile data
  - [x] 2.2: Emit greeting before entering input loop
  - [x] 2.3: Emit memory trace event for greeting
  - [x] 2.4: Preserve Story 4.1 warning behavior for missing profiles

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 4.2 + impacted startup tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status

## Dev Notes

### Guardrails

- Greeting must happen before first prompt/read loop.
- No greeting in missing-profile path.
- Keep startup deterministic for tests by using isolated helper functions.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.2]
- [Source: main.py]
- [Source: src/concierge/agents/memory_service.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Targeted validation:
  - `pytest tests/unit/test_story_4_2_proactive_greeting.py tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_2_3_main_entrypoint.py tests/unit/test_trace.py -q`
  - Result: 20 passed
- Full regression:
  - `pytest tests -q`
  - Result: 111 passed, 2 skipped

### Completion Notes List

- Added profile-derived greeting formatter to memory service.
- Emitted proactive greeting before loop start and preserved missing-profile no-greeting behavior.
- Added memory greeting trace emission: `trace("memory", event="greeting_fired", user_id=...)`.
- Added Story 4.2 unit tests for greeting content, startup timing, fast-mode ordering, and no-profile path.
- Hardened trace writer handling for closed-capture streams to avoid runtime `ValueError` during repeated test runs.

### File List

- _bmad-output/implementation-artifacts/4-2-implement-proactive-memory-driven-greeting-before-first-user-input.md (created and updated)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- main.py (modified)
- src/concierge/agents/memory_service.py (modified)
- src/concierge/trace.py (modified)
- tests/unit/test_story_2_3_main_entrypoint.py (modified)
- tests/unit/test_story_4_2_proactive_greeting.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented proactive memory-driven greeting and trace emission; validated with targeted and full regression; moved status to review.
