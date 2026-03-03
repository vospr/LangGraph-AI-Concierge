# Story 7.6: Polish All Layer 1 and Layer 2 Artifacts and Document Profile Reset

Status: review

## Story

As a **developer**,
I want every artifact visible to a hiring manager (README, ADRs, memory profile) to be polished and self-documenting, and the profile reset command to be clearly documented,
so that the demo is flawless.

## Acceptance Criteria

1. **Given** the README, **When** I read it, **Then** it contains: (1) Mermaid topology diagram at the top, (2) JD mapping table below it, (3) "Navigating This Repo" section with 5-step reading path, (4) quick-start command, (5) demo script reference, (6) link to `spec/concierge-spec.md`
2. **Given** `docs/adr/001-context-window-ownership.md`, **When** I read it, **Then** it's <=20 lines and includes decision context, options considered, and rationale
3. **Given** `memory/profiles/alex.json`, **When** I parse it, **Then** it has a `_demo_notes` field explaining the test scenario
4. **Given** the profile reset command, **When** documented in README, **Then** it states `git checkout -- memory/profiles/alex.json`
5. **And** `memory/README.md` explains the memory model (profile vs. session distinction) in 3-5 lines
6. **Given** Layer 2 source artifacts, **When** a developer reads them, **Then** production swap-points are explicit readable design statements

## Tasks / Subtasks

- [x] Task 1: Polish README and artifact visibility (AC: 1, 4)
  - [x] 1.1: Ensure README has Mermaid topology, JD table, and Navigating section with 5 steps
  - [x] 1.2: Add quick-start command and demo script reference
  - [x] 1.3: Add explicit profile reset command in README
  - [x] 1.4: Keep authoritative link to `spec/concierge-spec.md`

- [x] Task 2: Validate Layer 1/Layer 2 documentation contracts (AC: 2, 3, 5, 6)
  - [x] 2.1: Validate ADR-001 line count and required decision fields
  - [x] 2.2: Validate `_demo_notes` in `memory/profiles/alex.json`
  - [x] 2.3: Validate `memory/README.md` line-length and model explanation
  - [x] 2.4: Validate explicit production swap-point statements in source

- [x] Task 3: Add Story 7.6 tests and finalize
  - [x] 3.1: Create `tests/unit/test_story_7_6_layer_artifact_polish.py`
  - [x] 3.2: Run Story 7.6 targeted tests
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- README ordering preserves prior story contract requiring "Navigating This Repo" immediately after Mermaid.
- Story validation is encoded in tests to keep Layer 1 and Layer 2 artifact quality regression-safe.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 7.6]
- [Source: README.md]
- [Source: docs/adr/001-context-window-ownership.md]
- [Source: memory/profiles/alex.json]
- [Source: memory/README.md]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 7.6 targeted validation:
  - `pytest tests/unit/test_story_7_6_layer_artifact_polish.py tests/unit/test_story_1_5_docs_contract.py -q`
  - Result: 12 passed
- Full regression:
  - `pytest tests -q`
  - Result: 189 passed, 2 skipped

### Completion Notes List

- Updated README with quick-start commands, demo script reference, explicit profile reset command, and preserved 5-step navigation and spec link.
- Added Story 7.6 contract tests for README content, ADR-001 structure/length, memory documentation, `_demo_notes`, and source swap-point clarity.
- Verified all Story 7.6 and full-suite tests pass.

### File List

- _bmad-output/implementation-artifacts/7-6-polish-all-layer-1-and-layer-2-artifacts-and-document-profile-reset.md (created)
- README.md (modified)
- tests/unit/test_story_7_6_layer_artifact_polish.py (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)

## Change Log

- 2026-02-25: Story file initialized; artifact polish and Story 7.6 tests added.
- 2026-02-25: Story 7.6 validations passed; status moved to review.
