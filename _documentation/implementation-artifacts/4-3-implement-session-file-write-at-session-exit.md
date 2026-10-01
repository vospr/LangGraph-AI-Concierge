# Story 4.3: Implement Session File Write at Session Exit

Status: review

## Story

As a **developer**,
I want the Memory Service to write the full conversation state to `memory/sessions/{session_id}.json` when the user exits,
so that session continuity is preserved across runs.

## Acceptance Criteria

1. **Given** a completed session, **When** the user exits (`CTRL+C` or natural end), **Then** `memory/sessions/{session_id}/state.json` is written
2. **Given** the session file, **When** parsed, **Then** it contains: `session_id`, `user_id`, `timestamp_start`, `timestamp_end`, `conversation_history`, `turn_count`
3. **Given** the session directory, **When** listed, **Then** each session has a unique `session_id` subdirectory with readable JSON
4. **Given** memory paths, **When** resolved, **Then** `Path(__file__).parent` is used (not CWD), working from any directory
5. **And** current startup/loop behavior remains stable with existing stories and tests

## Tasks / Subtasks

- [x] Task 1: Add Story 4.3 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_4_3_session_write_on_exit.py`
  - [x] 1.2: Add memory service write test asserting required payload fields in `state.json`
  - [x] 1.3: Add path-resolution test proving write works when CWD changes
  - [x] 1.4: Add main integration test asserting write occurs on normal exit

- [x] Task 2: Implement session persistence on exit (AC: 1, 2, 3, 4)
  - [x] 2.1: Extend memory service with `write_session_state(...)`
  - [x] 2.2: Resolve session storage path relative to module file
  - [x] 2.3: Persist required fields and JSON formatting
  - [x] 2.4: Integrate write call into main shutdown path after loop returns

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 4.3 + impacted main/memory tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story file and sprint status to review

## Dev Notes

### Guardrails

- Do not regress Story 4.1/4.2 startup behavior.
- Keep session write path deterministic and file-relative.
- Keep persisted payload minimal and explicit per AC.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.3]
- [Source: main.py]
- [Source: src/concierge/agents/memory_service.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Targeted validation:
  - `pytest tests/unit/test_story_4_3_session_write_on_exit.py tests/unit/test_story_4_2_proactive_greeting.py tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_2_3_main_entrypoint.py -q`
  - Result: 18 passed
- Full regression:
  - `pytest tests -q`
  - Result: 114 passed, 2 skipped

### Completion Notes List

- Added memory service session persistence API writing to `memory/sessions/{session_id}/state.json`.
- Added startup/shutdown timestamps and integrated write-on-exit into `main.py`.
- Updated run loop state handling to preserve latest graph state object for final persistence.
- Added Story 4.3 tests for payload contract, path resolution independent of CWD, and main natural-exit persistence.

### File List

- _bmad-output/implementation-artifacts/4-3-implement-session-file-write-at-session-exit.md (created and updated)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- main.py (modified)
- src/concierge/agents/memory_service.py (modified)
- tests/unit/test_story_4_3_session_write_on_exit.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented session write-at-exit flow with required payload and path guarantees; validated with targeted/full regression; moved status to review.
