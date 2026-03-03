# Story 7.5: Implement Prompt Versioning Demonstration (Extensibility for FR37)

Status: review

## Story

As a **developer**,
I want the system to support prompt versioning without code changes,
so that a contributor can change `prompt_version: v1` to `v2` in YAML and the system automatically picks up the new prompt.

## Acceptance Criteria

1. **Given** `prompts/dispatcher/policy.yaml`, **When** I change `prompt_version: v1` to `v2`, **Then** the system loads `prompts/dispatcher/v2.yaml` instead
2. **Given** `AgentPolicy.prompt_version` as a field, **When** agents are instantiated, **Then** they read this value and load the corresponding prompt file dynamically
3. **Given** a missing `v2.yaml`, **When** it's referenced, **Then** `validate_config.py` catches it at startup with an actionable error: `prompts/dispatcher/v2.yaml not found`
4. **And** `tests/test_prompt_versioning.py` validates that bumping version loads the correct prompt file without code changes

## Tasks / Subtasks

- [x] Task 1: Add Story 7.5 tests (AC: 1-4)
  - [x] 1.1: Create `tests/test_prompt_versioning.py`
  - [x] 1.2: Add test proving dispatcher loads `v2` prompt when policy version is `v2`
  - [x] 1.3: Add test proving `validate_config` emits actionable missing-version file error

- [x] Task 2: Implement prompt-versioning validation hardening (AC: 2-3)
  - [x] 2.1: Add `check_prompt_version_files_exist` to `validate_config.py`
  - [x] 2.2: Ensure check runs in startup check sequence
  - [x] 2.3: Update validator tests for new check order

- [x] Task 3: Add dispatcher v2 prompt demonstration asset (AC: 1)
  - [x] 3.1: Add `prompts/dispatcher/v2.yaml`

- [x] Task 4: Validate and finalize
  - [x] 4.1: Run Story 7.5 targeted tests
  - [x] 4.2: Run full suite `pytest tests -q`
  - [x] 4.3: Update sprint status to review

## Dev Notes

### Guardrails

- Prompt versioning remains policy-driven and code-agnostic; tests validate behavior with temporary policy/prompt assets.
- Validation checks now fail fast when a referenced prompt version file is missing.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 7.5]
- [Source: src/concierge/agents/dispatcher.py]
- [Source: validate_config.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 7.5 targeted validation:
  - `pytest tests/test_prompt_versioning.py tests/unit/test_validate_config.py tests/unit/test_prompt_policy_contract.py -q`
  - Result: 11 passed, 1 skipped
- Full regression:
  - `pytest tests -q`
  - Result: 184 passed, 2 skipped

### Completion Notes List

- Added `tests/test_prompt_versioning.py` with contract tests for `v2` prompt loading and actionable missing-version validation errors.
- Added `check_prompt_version_files_exist` to `validate_config.py` and wired it into startup check order.
- Updated `tests/unit/test_validate_config.py` to reflect new check order and run-check monkeypatch setup.
- Added `prompts/dispatcher/v2.yaml` to demonstrate versioned prompt asset support.

### File List

- _bmad-output/implementation-artifacts/7-5-implement-prompt-versioning-demonstration-extensibility-for-fr37.md (created)
- prompts/dispatcher/v2.yaml (created)
- tests/test_prompt_versioning.py (created)
- tests/unit/test_validate_config.py (modified)
- validate_config.py (modified)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)

## Change Log

- 2026-02-25: Story file initialized; prompt-versioning tests and validation updates implemented.
- 2026-02-25: Story 7.5 validations passed; status moved to review.
