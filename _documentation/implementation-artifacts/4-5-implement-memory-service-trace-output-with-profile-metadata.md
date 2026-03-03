# Story 4.5: Implement Memory Service Trace Output with Profile Metadata

Status: review

## Story

As a **developer**,
I want the Memory Service to emit structured trace entries when loading and writing profiles,
so that session boundaries are observable in the CLI output.

## Acceptance Criteria

1. **Given** profile load at session start, **When** it occurs, **Then** `trace("memory", event="profile_loaded", user_id="alex", past_trips_count=2)` is called
2. **Given** session write at exit, **When** it occurs, **Then** `trace("memory", event="session_written", session_id=X, turn_count=N)` is called
3. **Given** profile not found, **When** it occurs, **Then** `trace("memory", event="profile_not_found", user_id=X)` is called
4. **Given** trace output, **When** I inspect it, **Then** it follows the `[memory]` bracket-label convention with outcome-oriented fields (no sensitive data leaked)

## Tasks / Subtasks

- [x] Task 1: Add Story 4.5 tests (AC: 1, 2, 3, 4)
  - [x] 1.1: Create `tests/unit/test_story_4_5_memory_trace_output.py`
  - [x] 1.2: Add profile-load trace test asserting `profile_loaded` payload with `past_trips_count`
  - [x] 1.3: Add missing-profile trace test asserting `profile_not_found` payload
  - [x] 1.4: Add session-write trace test asserting `session_written` payload with `session_id` and `turn_count`
  - [x] 1.5: Add trace rendering test asserting `[memory]` prefix and non-sensitive, outcome-oriented fields

- [x] Task 2: Implement memory trace emission and metadata fields (AC: 1, 2, 3, 4)
  - [x] 2.1: Emit `profile_loaded` event from Memory Service profile-load success path
  - [x] 2.2: Emit `profile_not_found` event from not-found/fallback path
  - [x] 2.3: Emit `session_written` event from session-write success path
  - [x] 2.4: Ensure trace allowlist supports required Story 4.5 fields without expanding sensitive surface

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 4.5 tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep memory trace fields outcome-oriented; avoid raw profile/session payload dumps.
- Preserve Story 4.1-4.4 behavior for warnings, greeting, and session persistence.
- Keep trace shape compatible with `src/concierge/trace.py` allowlist/denylist contract.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.5]
- [Source: src/concierge/agents/memory_service.py]
- [Source: src/concierge/trace.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_4_5_memory_trace_output.py -q`
  - Result: 4 failed (expected before implementation)
- Targeted validation:
  - `pytest tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_4_2_proactive_greeting.py tests/unit/test_story_4_3_session_write_on_exit.py tests/unit/test_story_4_4_fresh_session_fallback.py tests/unit/test_story_4_5_memory_trace_output.py tests/unit/test_trace.py -q`
  - Result: 24 passed
- Full regression:
  - `pytest tests -q`
  - Result: 121 passed, 2 skipped

### Completion Notes List

- Added Story 4.5 regression tests for memory trace events on profile load, profile fallback, and session-write paths.
- Implemented Memory Service trace emission for `profile_loaded`, `profile_not_found`, and `session_written` events.
- Added `past_trips_count` to trace allowlist so metadata output remains structured and compliant with trace filtering.
- Validated no regression across existing Story 4.1-4.4 memory and trace contracts.

### File List

- _bmad-output/implementation-artifacts/4-5-implement-memory-service-trace-output-with-profile-metadata.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/memory_service.py (modified)
- src/concierge/trace.py (modified)
- tests/unit/test_story_4_5_memory_trace_output.py (created)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented memory trace metadata/events with Story 4.5 tests; validated targeted and full regression; set status to review.
