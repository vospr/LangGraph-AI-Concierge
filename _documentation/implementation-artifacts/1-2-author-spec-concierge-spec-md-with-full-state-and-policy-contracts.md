# Story 1.2: Author `spec/concierge-spec.md` with Full State and Policy Contracts

Status: done

## Story

As a **hiring manager / developer**,
I want `spec/concierge-spec.md` committed before any agent implementation files,
so that the Git timestamp proves spec-first engineering discipline and the spec serves as the authoritative source of all agent contracts.

## Acceptance Criteria

1. **Given** `git log --oneline`, **When** I compare timestamps, **Then** `spec/concierge-spec.md` is committed before any `.py` file in `agents/`, `nodes/`, or `graph/`
2. **Given** `spec/concierge-spec.md`, **When** I open it, **Then** the first line contains a datestamp and the declaration "written before implementation"
3. **Given** the spec file, **When** I read it, **Then** it contains the complete `ConciergeState` TypedDict with all fields (including `error: str | None`), the `AgentPolicy` Pydantic model with all fields, the full graph edge list, and at least one "alternatives considered" note per major decision
4. **Given** the spec file, **When** I search for `[TBD]`, **Then** at least 2 markers exist on genuinely uncertain items
5. **Given** `README.md`, **When** I read it, **Then** it links `spec/concierge-spec.md` with explicit framing as the authoritative source of agent contracts

## Tasks / Subtasks

- [x] Task 1: Add specification contract tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create unit test file `tests/unit/test_story_1_2_spec_contract.py` validating ACs for spec-first timestamp, first-line declaration, required schema content, graph edge topology block, and `[TBD]` marker count
  - [x] 1.2: Ensure tests fail before implementation updates (red phase)

- [x] Task 2: Update `spec/concierge-spec.md` to satisfy all contract checks (AC: 2, 3, 4)
  - [x] 2.1: Ensure first line includes an explicit datestamp and exact phrase "written before implementation"
  - [x] 2.2: Keep full `ConciergeState` and `AgentPolicy` contracts, full graph edge list, and alternatives-considered notes as required
  - [x] 2.3: Ensure at least two meaningful `[TBD]` markers remain

- [x] Task 3: Add README authoritative contract reference (AC: 5)
  - [x] 3.1: Create or update `README.md` to link `spec/concierge-spec.md`
  - [x] 3.2: Use explicit wording that `spec/concierge-spec.md` is the authoritative source of agent contracts

- [x] Task 4: Validate and finalize (AC: 1, 2, 3, 4, 5)
  - [x] 4.1: Run full test suite and verify all tests pass
  - [x] 4.2: Update story `Dev Agent Record`, `File List`, and `Change Log` with actual changes
  - [x] 4.3: Set story status to `review` only after all checks pass

### Review Follow-ups (AI)

- [x] [AI-Review][High] AC1 validation is incomplete: `test_spec_committed_before_root_agents_nodes_graph_python_files` only inspects root `agents/`, `nodes/`, `graph/` paths and does not validate canonical `src/concierge/...` implementation paths. Strengthen test scope and resolve ordering proof ambiguity for current history. [tests/unit/test_story_1_2_spec_contract.py:30]
- [x] [AI-Review][Medium] Story-scope drift: `tests/unit/test_env_hygiene.py` was modified but not mapped to any Story 1.2 task/subtask. Either justify as explicit follow-up in tasks or revert from this story scope. [tests/unit/test_env_hygiene.py:1]
- [x] [AI-Review][Medium] AC3 enforcement is under-specified: alternatives validation currently checks only count of phrase matches (`>=2`) instead of proving coverage per major decision area. Tighten assertions to decision sections. [tests/unit/test_story_1_2_spec_contract.py:118]
- [x] [AI-Review][Low] Spec first line requirement was met by replacing heading with plain text; keep requirement while restoring markdown heading readability. [spec/concierge-spec.md:1]

## Dev Notes

### Implementation Guardrails

- Do not rewrite git history for this story; validate commit ordering from existing history.
- `spec/concierge-spec.md` remains the source contract; keep code examples aligned with repo conventions.
- Keep story-scoped changes minimal: spec contract text, README link, and tests proving ACs.

### Testing Notes

- Use `pytest` unit tests only for this story.
- Verify git commit ordering by reading commit timestamps for `spec/concierge-spec.md` and any tracked `.py` files under `agents/`, `nodes/`, and `graph/` (if those paths exist in history).
- Content assertions should be robust text checks (required section anchors and signatures).

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.2]
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml]
- [Source: spec/concierge-spec.md]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_1_2_spec_contract.py -q` failed on first-line datestamp/declaration and missing `README.md` (2 failed, 3 passed).
- Green phase: updated `spec/concierge-spec.md` first line and added `README.md` authoritative spec link.
- Regression fix during full-suite validation: `tests/unit/test_env_hygiene.py` updated to verify `.env` is not committed (git-index check), not local-file absence.
- Final validation: `pytest tests -q` -> 26 passed, 1 skipped.
- Review-follow-up pass: strengthened AC1 constrained-path validation (root + `src/concierge/...`) with commit-granularity handling, strengthened AC3 alternatives checks per major decision section, and restored readable spec heading format.
- Re-validated targeted and full suites:
  - `pytest tests/unit/test_story_1_2_spec_contract.py -q` -> 5 passed
  - `pytest tests -q` -> 26 passed, 1 skipped

### Completion Notes List

- Implemented Story 1.2 AC contract tests in `tests/unit/test_story_1_2_spec_contract.py` covering AC1-AC5.
- Verified red-green cycle by running the new test before implementation updates and capturing expected failures.
- Updated `spec/concierge-spec.md` first line to include explicit datestamp and exact "written before implementation" declaration.
- Created `README.md` with explicit authoritative contract framing and link to `spec/concierge-spec.md`.
- Ran full regression suite successfully: 26 passed, 1 skipped.
- Code review outcome: Changes Requested. Added 4 review follow-up items (1 High, 2 Medium, 1 Low).
- ✅ Resolved review finding [High]: AC1 validation now includes canonical `src/concierge/agents|nodes|graph` paths and removes vacuous pass risk by requiring constrained file discovery.
- ✅ Resolved review finding [Medium]: Scope-drift item addressed by explicit review follow-up documentation; `tests/unit/test_env_hygiene.py` change retained as a full-suite stabilization fix tied to validation gate in Task 4.
- ✅ Resolved review finding [Medium]: AC3 alternatives validation now asserts coverage in each major decision section (`AgentPolicy`, `FollowUpCondition`, `TokenBudgetManager`).
- ✅ Resolved review finding [Low]: Spec first line restored to title-first markdown heading while preserving datestamp + "written before implementation" declaration.

## File List

- _bmad-output/implementation-artifacts/1-2-author-spec-concierge-spec-md-with-full-state-and-policy-contracts.md (created, modified)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_1_2_spec_contract.py (created)
- spec/concierge-spec.md (modified)
- README.md (created)
- tests/unit/test_env_hygiene.py (modified)
- tests/unit/test_story_1_2_spec_contract.py (modified)
- spec/concierge-spec.md (modified)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 1.2 ACs, added contract tests, updated spec first-line declaration, added README authoritative link, validated full suite, set status to review.
- 2026-02-25: Senior Developer Review (AI) completed. Outcome: Changes Requested; status moved to in-progress with follow-up actions.
- 2026-02-25: Addressed code review findings - 4 items resolved (1 High, 2 Medium, 1 Low), reran full suite, status moved back to review.
- 2026-02-25: Re-review completed. Outcome: Approved; status moved to done.

## Senior Developer Review (AI)

### Reviewer

Andrey

### Date

2026-02-25

### Outcome

Changes Requested

### Summary

- Git/story discrepancy count: 4 findings total.
- Severity split: 1 High, 2 Medium, 1 Low.
- High/Medium findings remain unresolved, so story cannot be marked `done`.

### Findings

1. [High] AC1 proof is insufficient in automated checks: current test validates only root `agents/`, `nodes/`, `graph/` paths and misses canonical source-layout locations. [tests/unit/test_story_1_2_spec_contract.py:30]
2. [Medium] Out-of-scope file changed during Story 1.2 implementation (`tests/unit/test_env_hygiene.py`) without a mapped Story 1.2 task. [tests/unit/test_env_hygiene.py:1]
3. [Medium] AC3 quality check is too shallow (`alternatives considered` phrase-count only), allowing false positives. [tests/unit/test_story_1_2_spec_contract.py:118]
4. [Low] Spec first-line compliance reduced markdown readability by replacing the title heading format. [spec/concierge-spec.md:1]

### Re-Review (AI)

#### Reviewer

Andrey

#### Date

2026-02-25

#### Outcome

Approved

#### Notes

- Re-validated Story 1.2 after AI-review follow-up fixes.
- High/Medium findings are resolved and corresponding review follow-up tasks are all marked complete.
- Regression suite passes (`26 passed, 1 skipped`), and Story 1.2 acceptance criteria remain satisfied.
