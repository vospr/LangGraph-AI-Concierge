# Story 4.6: Implement Dual-Store Architecture (In-Session State + Persisted File)

Status: review

## Story

As a **developer**,
I want conversation history to be stored in two places (in-session `ConciergeState` for active routing + persisted `memory/sessions/{session_id}.json` for cross-session continuity),
so that session context is never lost even if the process crashes.

## Acceptance Criteria

1. **Given** active session, **When** I inspect `state["conversation_history"]`, **Then** it contains all turns in memory for LLM context window management
2. **Given** session write, **When** it occurs at exit, **Then** the full `conversation_history` is appended to `memory/sessions/{session_id}.json`
3. **Given** a new session for the same user, **When** it starts, **Then** the greeting can read `memory/sessions/{previous_session_id}/state.json` to access `cached_research_session` or other context
4. **Given** `state["conversation_history"]` vs. the persisted file, **When** I compare them, **Then** the persisted file is the authoritative long-term record independent of in-memory state
5. **Given** NFR8 graceful degradation, **When** session write fails (disk full, permissions), **Then** `state["human_handoff"] = True` and the user is notified: `Session could not be saved — a human can assist`
6. **And** the in-session routing continues (degradation, not crash)

## Tasks / Subtasks

- [x] Task 1: Add Story 4.6 tests (AC: 1, 2, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_4_6_dual_store_architecture.py`
  - [x] 1.2: Add active-session in-memory history continuity test
  - [x] 1.3: Add persisted-session history test asserting full write payload behavior
  - [x] 1.4: Add previous-session context load test proving access to `cached_research_session`
  - [x] 1.5: Add persisted-authority test proving file record is independent of post-write in-memory mutation
  - [x] 1.6: Add graceful-degradation test for session-write failure (`human_handoff` + user notification + no crash)

- [x] Task 2: Implement dual-store behavior and degradation handling (AC: all)
  - [x] 2.1: Ensure in-session conversation history remains complete through loop updates
  - [x] 2.2: Ensure session writer persists full in-memory conversation history snapshot
  - [x] 2.3: Load previous session context (including `cached_research_session`) during new-session profile load
  - [x] 2.4: Implement save-failure graceful degradation (`human_handoff` and explicit user message) without uncaught exception

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 4.6 and impacted memory/startup tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Preserve Story 3.7 conversation-history ownership guarantees.
- Preserve Story 4.1-4.5 memory load/write and trace behavior.
- Keep graceful degradation scoped to session persistence boundary; do not introduce process crashes.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.6]
- [Source: src/concierge/agents/memory_service.py]
- [Source: main.py]
- [Source: src/concierge/state.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_4_6_dual_store_architecture.py -q`
  - Result: 3 failed, 3 passed (expected before implementation)
- Story 4.6 validation:
  - `pytest tests/unit/test_story_4_6_dual_store_architecture.py -q`
  - Result: 7 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_2_3_main_entrypoint.py tests/unit/test_story_4_1_memory_profile_loader.py tests/unit/test_story_4_2_proactive_greeting.py tests/unit/test_story_4_3_session_write_on_exit.py tests/unit/test_story_4_4_fresh_session_fallback.py tests/unit/test_story_4_5_memory_trace_output.py tests/unit/test_story_4_6_dual_store_architecture.py tests/unit/test_trace.py -q`
  - Result: 37 passed
- Full regression:
  - `pytest tests -q`
  - Result: 128 passed, 2 skipped

### Completion Notes List

- Added Story 4.6 tests covering in-memory history continuity, persisted history snapshot integrity, previous-session context hydration, and save-failure graceful degradation.
- Updated Memory Service profile load to hydrate `cached_research_session` from the latest matching prior session state file.
- Updated Memory Service session writes to persist `cached_research_session` when available, preserving cross-session context continuity.
- Added proactive greeting fallback that can reference cached prior-session research context when trip-history greeting data is unavailable.
- Hardened session persistence boundary in `main.py` to degrade gracefully on write failures: set `human_handoff`, set actionable error, and notify user without crashing.

### File List

- _bmad-output/implementation-artifacts/4-6-implement-dual-store-architecture-in-session-state-plus-persisted-file.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- main.py (modified)
- src/concierge/agents/memory_service.py (modified)
- tests/unit/test_story_4_6_dual_store_architecture.py (created)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented dual-store memory/session continuity and graceful degradation with Story 4.6 tests; validated targeted and full regression; set status to review.
