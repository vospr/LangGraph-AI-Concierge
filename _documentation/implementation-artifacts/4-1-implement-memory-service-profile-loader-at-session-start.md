# Story 4.1: Implement Memory Service Profile Loader at Session Start

Status: review

## Story

As a **developer**,
I want the Memory Service to load a user profile from `memory/profiles/{user_id}.json` at session start using paths resolved relative to `Path(__file__).parent`,
so that user context is available before any agent logic runs.

## Acceptance Criteria

1. **Given** `memory/profiles/alex.json` exists, **When** the session starts with `--user alex`, **Then** `state["memory_profile"]` is populated with the full profile (not `None`)
2. **Given** the Memory Service, **When** it loads the profile, **Then** it uses `Path(__file__).parent` to resolve paths (not CWD), working correctly even if `python main.py` is run from a different directory
3. **Given** a profile missing, **When** the session starts, **Then** `state["memory_profile"] = None` (no crash, no exception)
4. **Given** a profile missing, **When** it occurs, **Then** a visible warning is emitted: `[MEMORY] Profile for {user_id} not found — starting fresh session`
5. **Given** `memory/profiles/alex.json`, **When** parsed, **Then** it contains fields: `user_id`, `past_trips`, `preferences`, `cached_research_session`, `last_seen`

## Tasks / Subtasks

- [x] Task 1: Add Story 4.1 failing tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_4_1_memory_profile_loader.py`
  - [x] 1.2: Add test for loading existing `alex` profile into startup state
  - [x] 1.3: Add path-resolution test proving loader works after changing CWD
  - [x] 1.4: Add missing-profile test asserting warning text and `None` return
  - [x] 1.5: Add profile schema-field test for required keys

- [x] Task 2: Implement Memory Service loader and startup integration (AC: 1, 2, 3, 4)
  - [x] 2.1: Add `src/concierge/agents/memory_service.py` with profile load API
  - [x] 2.2: Resolve profile directory relative to `Path(__file__).parent`
  - [x] 2.3: Catch missing-profile case and emit required warning without exception
  - [x] 2.4: Wire loader into `main.py` session startup before graph loop

- [x] Task 3: Ensure `alex` profile compatibility and run regression (AC: all)
  - [x] 3.1: Ensure `memory/profiles/alex.json` includes required Story 4.1 keys
  - [x] 3.2: Run targeted Story 4.1 tests
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update story record, file list, change log, and sprint status

## Dev Notes

### Architecture Guardrails

- Memory loading happens at session start before turn processing.
- Loader behavior must degrade gracefully (missing file -> warning + `None`).
- Avoid CWD-dependent path resolution.

### Previous Story Intelligence

- Story 2.3 established CLI startup flow in `main.py`; integrate without breaking flag/loop behavior.
- Story 3.x stabilized dispatcher/graph; memory load must not alter routing contracts.

### File Structure Notes

- Primary expected targets:
  - `src/concierge/agents/memory_service.py`
  - `main.py`
  - `memory/profiles/alex.json`
  - `tests/unit/test_story_4_1_memory_profile_loader.py`

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.1]
- [Source: _bmad-output/planning-artifacts/prd.md#Memory & Personalization]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Targeted validation:
  - `pytest tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_2_3_main_entrypoint.py tests/unit/test_story_1_5_docs_contract.py -q`
  - Result: 18 passed
- Full regression:
  - `pytest tests -q`
  - Result: 107 passed, 2 skipped

### Completion Notes List

- Added `MemoryService` profile loader with file-relative path resolution.
- Wired memory profile loading into startup flow before entering graph loop.
- Implemented missing-profile graceful fallback with visible warning.
- Added Story 4.1 tests covering loader behavior, pathing, warning, and main integration.
- Extended `alex` profile with `cached_research_session` and `last_seen` fields for Story 4.1 schema requirements.

### File List

- _bmad-output/implementation-artifacts/4-1-implement-memory-service-profile-loader-at-session-start.md (created and updated)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- main.py (modified)
- memory/profiles/alex.json (modified)
- src/concierge/agents/memory_service.py (created)
- tests/unit/test_story_4_1_memory_profile_loader.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 4.1 memory profile loader and startup integration; validated with targeted and full regression; moved status to review.
