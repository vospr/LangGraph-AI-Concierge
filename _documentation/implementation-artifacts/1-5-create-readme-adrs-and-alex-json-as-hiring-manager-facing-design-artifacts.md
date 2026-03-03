# Story 1.5: Create README, ADRs, and `alex.json` as Hiring-Manager-Facing Design Artifacts

Status: review

## Story

As a **hiring manager**,
I want the README to lead with a Mermaid agent topology diagram and a JD mapping table, and `memory/profiles/alex.json` to demonstrate the full `UserProfile` schema,
so that I can evaluate the architectural judgment in 30 seconds without running any code.

## Acceptance Criteria

1. **Given** `README.md`, **When** I view the first screen-height, **Then** a Mermaid agent topology diagram and the JD mapping table are both visible before any scrolling
2. **Given** the README JD mapping table, **When** I read it, **Then** >=7 of the 9 MVP items are mapped to specific job description bullets
3. **Given** `README.md`, **When** I search for "Navigating This Repo", **Then** a section exists with a 5-step ordered reading path immediately after the Mermaid graph
4. **Given** `docs/adr/` directory, **When** I list it, **Then** ADR-001 through ADR-005 exist, each <=20 lines, each with decision context, options considered, and rationale
5. **Given** `memory/profiles/alex.json`, **When** I parse it, **Then** it demonstrates the full `UserProfile` schema including past trips, preferences, a cached research session, and a `_demo_notes` field
6. **Given** `memory/README.md`, **When** I read it, **Then** it explains the memory model (profile vs. session, read vs. write) in 3-5 lines

## Tasks / Subtasks

- [x] Task 1: Add story contract tests for README, ADR, and memory artifacts (AC: 1, 2, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_1_5_docs_contract.py` with assertions for README top-of-file structure, JD mapping table depth, and "Navigating This Repo" ordering
  - [x] 1.2: Add assertions for ADR file existence (`001`-`005`), per-file line cap (`<=20`), and required decision fields
  - [x] 1.3: Add assertions for `memory/profiles/alex.json` required schema fields and `memory/README.md` 3-5 line explanatory contract

- [x] Task 2: Implement README as Layer-1 hiring-manager scan artifact (AC: 1, 2, 3)
  - [x] 2.1: Add Mermaid topology diagram at top section and keep document concise enough for first-screen visibility
  - [x] 2.2: Add "Navigating This Repo" section immediately after Mermaid with exactly 5 ordered steps
  - [x] 2.3: Add JD mapping table with 9 MVP items and ensure at least 7 rows map to specific JD bullets
  - [x] 2.4: Keep explicit authoritative link to `spec/concierge-spec.md`

- [x] Task 3: Add ADR set `001` through `005` (AC: 4)
  - [x] 3.1: Create `docs/adr/001-context-window-ownership.md`
  - [x] 3.2: Create `docs/adr/002-multi-model-strategy.md`
  - [x] 3.3: Create `docs/adr/003-anthropic-only-mvp.md`
  - [x] 3.4: Create `docs/adr/004-file-based-memory.md`
  - [x] 3.5: Create `docs/adr/005-langgraph-framework-selection.md`
  - [x] 3.6: Ensure each ADR is <=20 lines and includes Decision Context, Options Considered, and Rationale

- [x] Task 4: Align memory profile and memory README artifacts (AC: 5, 6)
  - [x] 4.1: Verify/update `memory/profiles/alex.json` to reflect full demo profile schema with past trips, preferences, cached research session context, and `_demo_notes`
  - [x] 4.2: Rewrite `memory/README.md` to a clear 3-5 line explanation of profile vs. session and read vs. write behavior

- [x] Task 5: Finalize story implementation and quality gates (AC: 1, 2, 3, 4, 5, 6)
  - [x] 5.1: Run `pytest tests/unit/test_story_1_5_docs_contract.py -q`
  - [x] 5.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 5.3: Update story `Dev Agent Record`, `File List`, and `Change Log` with execution evidence
  - [x] 5.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Treat README as a 30-second Layer-1 artifact for hiring-manager scanability.
- Preserve concise, deterministic markdown structures so tests can verify contract requirements.
- ADR files are short decision records, not long design docs; cap at <=20 lines each.
- Keep memory artifacts aligned with `spec/concierge-spec.md` `UserProfile` semantics.

### Testing Notes

- Use pure unit tests; no network calls or runtime dependencies required.
- Validate README ordering by section positions, not visual rendering.
- Validate ADR brevity by non-empty line count to avoid false passes via blank padding.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.5]
- [Source: spec/concierge-spec.md#§MemorySchema]
- [Source: _bmad-output/planning-artifacts/architecture.md#Canonical Directory Tree]
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_1_5_docs_contract.py -q` -> 6 failed, 1 passed (missing README sections, missing ADR files, memory README line-count contract).
- Green phase: updated `README.md` with top Mermaid block, immediate "Navigating This Repo" 5-step section, and 9-row JD mapping table.
- Green phase: created ADR files `001`-`005` in `docs/adr/`, each concise and structured with Decision Context / Options Considered / Rationale.
- Green phase: rewrote `memory/README.md` to a 4-line profile/session read-write explanation.
- Targeted validation: `pytest tests/unit/test_story_1_5_docs_contract.py -q` -> 7 passed.
- Full regression: `pytest tests -q` -> 50 passed, 2 skipped.

### Completion Notes List

- Implemented Story 1.5 as a hiring-manager-facing artifact set with deterministic markdown contracts.
- Added executable tests for README structure and density, ADR presence/brevity, and memory artifact schema.
- Preserved `memory/profiles/alex.json` because it already satisfied full schema expectations; validated via new tests.
- Verified no regressions across all existing stories after documentation-layer updates.

## File List

- _bmad-output/implementation-artifacts/1-5-create-readme-adrs-and-alex-json-as-hiring-manager-facing-design-artifacts.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_1_5_docs_contract.py (created)
- README.md (modified)
- memory/README.md (modified)
- docs/adr/001-context-window-ownership.md (created)
- docs/adr/002-multi-model-strategy.md (created)
- docs/adr/003-anthropic-only-mvp.md (created)
- docs/adr/004-file-based-memory.md (created)
- docs/adr/005-langgraph-framework-selection.md (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 1.5 README/ADR/memory artifacts, added contract tests, and moved status to review after full suite pass.
