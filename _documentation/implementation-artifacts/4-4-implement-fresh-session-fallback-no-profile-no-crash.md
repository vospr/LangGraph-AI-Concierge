# Story 4.4: Implement Fresh Session Fallback (No Profile, No Crash)

Status: review

## Story

As a **developer**,
I want the system to gracefully handle missing or malformed profiles without crashing, emitting a visible warning and continuing with a fresh session,
so that the demo remains resilient.

## Acceptance Criteria

1. **Given** `--user unknown_user` with no profile file, **When** session starts, **Then** memory service catches missing file and sets `state["memory_profile"] = None`
2. **Given** missing profile, **When** it occurs, **Then** warning is printed: `[MEMORY] Profile for unknown_user not found — starting fresh session`
3. **Given** no profile loaded, **When** session proceeds, **Then** user is prompted for input and system remains functional (no personalization, no crash)
4. **Given** malformed JSON profile, **When** loaded, **Then** it is caught as `JSONDecodeError`, warning is printed, and `state["memory_profile"] = None`
5. **And** no exception escapes to `main.py` — errors are handled at memory service boundary

## Tasks / Subtasks

- [x] Task 1: Add Story 4.4 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_4_4_fresh_session_fallback.py`
  - [x] 1.2: Add missing-profile startup continuation test
  - [x] 1.3: Add malformed JSON loader test asserting warning + `None`
  - [x] 1.4: Add main-path malformed profile test asserting no crash and loop continues

- [x] Task 2: Implement any required fallback hardening (AC: all)
  - [x] 2.1: Ensure memory service catches malformed profile payloads consistently
  - [x] 2.2: Ensure main startup path remains stable when profile load fails
  - [x] 2.3: Ensure no fallback behavior regresses Story 4.1–4.3 behavior

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 4.4 tests plus impacted startup tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- All profile-load errors handled in memory service boundary.
- Keep warning visible and session operational.
- Do not break proactive greeting/session persistence paths.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.4]
- [Source: src/concierge/agents/memory_service.py]
- [Source: main.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Targeted validation:
  - `pytest tests/unit/test_story_4_4_fresh_session_fallback.py tests/unit/test_story_4_3_session_write_on_exit.py tests/unit/test_story_4_2_proactive_greeting.py tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_2_3_main_entrypoint.py -q`
  - Result: 21 passed
- Full regression:
  - `pytest tests -q`
  - Result: 117 passed, 2 skipped

### Completion Notes List

- Added explicit Story 4.4 regression tests for malformed profile handling at memory boundary.
- Added main-path fallback tests proving no crash and continued loop behavior for missing/malformed profiles.
- Verified fallback behavior remains compatible with Story 4.1/4.2/4.3 startup, greeting, and session-persistence contracts.

### File List

- _bmad-output/implementation-artifacts/4-4-implement-fresh-session-fallback-no-profile-no-crash.md (created and updated)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_4_4_fresh_session_fallback.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Validated fresh-session fallback behavior for missing/malformed profiles with targeted and full regression; moved status to review.
