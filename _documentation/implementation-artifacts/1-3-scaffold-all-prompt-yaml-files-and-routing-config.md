# Story 1.3: Scaffold All Prompt YAML Files and Routing Config

Status: done

## Story

As a **developer**,
I want all agent `policy.yaml` and `v1.yaml` files scaffolded with the standard 5-section schema and `config/routing_rules.yaml` created with inline comments,
so that any contributor can understand every agent's configuration without reading Python source code.

## Acceptance Criteria

1. **Given** `prompts/` directory, **When** I list it, **Then** 6 subdirectories exist: `dispatcher/`, `rag_agent/`, `research_agent/`, `response_synthesis/`, `guardrail/`, `followup/` — each containing `policy.yaml` and `v1.yaml`
2. **Given** any `policy.yaml`, **When** I parse it as `AgentPolicy`, **Then** it contains valid values for `agent_name`, `model`, `prompt_version`, `max_tokens`, `confidence_threshold`, `max_clarifications`, `allowed_tools`
3. **Given** any `v1.yaml`, **When** I read it, **Then** it contains all 5 sections: `role`, `context`, `constraints`, `output_format`, `examples` — none empty
4. **Given** `prompts/dispatcher/policy.yaml`, **When** I read `max_tokens`, **Then** the value is exactly `128`
5. **Given** `config/routing_rules.yaml`, **When** I read it, **Then** every rule has an inline comment explaining its intent, and it contains `escalation_threshold` distinct from any per-agent `confidence_threshold`

## Tasks / Subtasks

- [x] Task 1: Scaffold required prompt directories and files (AC: 1)
  - [x] 1.1: Ensure `prompts/dispatcher/`, `prompts/rag_agent/`, `prompts/research_agent/`, `prompts/response_synthesis/`, `prompts/guardrail/`, `prompts/followup/` exist
  - [x] 1.2: Create `policy.yaml` and `v1.yaml` in each directory (replace `.gitkeep` placeholders where applicable)
  - [x] 1.3: Add unit test `tests/unit/test_prompt_scaffold_structure.py` to validate required directories and files

- [x] Task 2: Define valid `policy.yaml` for each agent (AC: 2, 4)
  - [x] 2.1: Populate each `policy.yaml` with fields: `agent_name`, `model`, `prompt_version`, `max_tokens`, `confidence_threshold`, `max_clarifications`, `allowed_tools`, `prompt_sections`
  - [x] 2.2: Set `prompts/dispatcher/policy.yaml` `max_tokens: 128` exactly
  - [x] 2.3: Add unit test `tests/unit/test_prompt_policy_contract.py` to parse every policy and validate field presence/types/constraints

- [x] Task 3: Define non-empty `v1.yaml` prompt contracts (AC: 3)
  - [x] 3.1: Populate each `v1.yaml` with all required sections: `role`, `context`, `constraints`, `output_format`, `examples`
  - [x] 3.2: Ensure each section is non-empty and agent-specific (no blank placeholders)
  - [x] 3.3: Add unit test `tests/unit/test_prompt_v1_sections.py` to validate section existence and non-empty content

- [x] Task 4: Create routing rules config with inline intent comments (AC: 5)
  - [x] 4.1: Create `config/routing_rules.yaml` including `escalation_threshold` and deterministic rule blocks
  - [x] 4.2: Ensure each routing rule includes inline comment explaining intent/behavior
  - [x] 4.3: Add unit test `tests/unit/test_routing_rules_config.py` validating `escalation_threshold` exists and is distinct from per-agent confidence thresholds

- [x] Task 5: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5)
  - [x] 5.1: Run `pytest tests -q` and confirm no regressions
  - [x] 5.2: Update story `Dev Agent Record`, `File List`, and `Change Log` with actual implementation evidence
  - [x] 5.3: Set story Status to `review` only after all tests pass and all ACs are satisfied

### Review Follow-ups (AI)

- [x] [AI-Review][Medium] Enforce Task 3.2 ("agent-specific" prompt content) with explicit anti-generic assertions in `tests/unit/test_prompt_v1_sections.py` instead of only non-empty checks. [tests/unit/test_prompt_v1_sections.py:26]
- [x] [AI-Review][Medium] Harden `config/routing_rules.yaml` regex patterns with word-boundary matching to reduce false-positive routes (e.g., `book` matching `bookkeeping`, `stock` matching `stockholm`). [config/routing_rules.yaml:9]
- [x] [AI-Review][Low] Make `ALLOWED_MODELS` validation less brittle (version family/prefix validation) to avoid unnecessary test churn on expected model-version updates. [tests/unit/test_prompt_policy_contract.py:17]

## Dev Notes

### Implementation Guardrails

- Keep policy schema aligned with `AgentPolicy` contract in `spec/concierge-spec.md` (`prompt_sections` must include exactly: `role`, `context`, `constraints`, `output_format`, `examples`).
- Use explicit, deterministic YAML values that can be validated in tests.
- `dispatcher` token limit is a hard architectural constraint (`max_tokens: 128`) and must not drift.
- Keep `routing_rules.yaml` self-documenting with inline comments per rule; avoid opaque scoring values without rationale.

### Suggested Starting Defaults (can be tuned later)

- `prompt_version: v1` for all agents.
- `allowed_tools`: empty list `[]` where no external tools are used yet.
- conservative `confidence_threshold` per agent, while keeping routing `escalation_threshold` as separate config concern in `config/routing_rules.yaml`.

### Testing Notes

- Prefer pure unit tests for YAML contracts and file structure checks.
- Parse YAML in tests with deterministic assertions for schema shape and required section content.
- Add explicit failure messages to make misconfigured files immediately actionable.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.3]
- [Source: spec/concierge-spec.md#AgentPolicy]
- [Source: _bmad-output/implementation-artifacts/sprint-status.yaml]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Task 1 red phase: `pytest tests/unit/test_prompt_scaffold_structure.py -q` failed (missing `policy.yaml` files).
- Task 1 green phase: scaffolded `policy.yaml` and `v1.yaml` for all six prompt directories and removed per-directory `.gitkeep` placeholders.
- Task 1 validation: `pytest tests -q` -> 28 passed, 1 skipped.
- Task 2 red phase: `pytest tests/unit/test_prompt_policy_contract.py -q` failed (empty YAML mappings).
- Task 2 green phase: populated all `policy.yaml` files with full contract fields and enforced `dispatcher.max_tokens: 128`.
- Task 2 validation: `pytest tests -q` -> 30 passed, 1 skipped.
- Task 3 red phase: `pytest tests/unit/test_prompt_v1_sections.py -q` failed (empty `v1.yaml` files).
- Task 3 green phase: populated all `v1.yaml` files with non-empty `role/context/constraints/output_format/examples`.
- Task 3 validation: `pytest tests -q` -> 31 passed, 1 skipped.
- Task 4 red phase: `pytest tests/unit/test_routing_rules_config.py -q` failed (missing `config/routing_rules.yaml`).
- Task 4 green phase: created routing config with inline comments and distinct `escalation_threshold`.
- Final validation: `pytest tests -q` -> 34 passed, 1 skipped.
- Review follow-up red phase: `pytest tests/unit/test_prompt_v1_sections.py tests/unit/test_routing_rules_config.py tests/unit/test_prompt_policy_contract.py -q` -> 3 failed.
- Review follow-up green phase: added agent-specific prompt assertions/content markers, enforced regex word-boundary patterns, and switched model validation to supported prefix families.
- Re-validation:
  - `pytest tests/unit/test_prompt_v1_sections.py tests/unit/test_routing_rules_config.py tests/unit/test_prompt_policy_contract.py -q` -> 9 passed
  - `pytest tests -q` -> 37 passed, 1 skipped

### Completion Notes List

- Implemented Story 1.3 end-to-end using strict red/green/refactor per task.
- Added six agent prompt policy files and six `v1` prompt contract files.
- Added four new unit test modules covering scaffold structure, policy contract, prompt section completeness, and routing config contract.
- Added `config/routing_rules.yaml` with deterministic rules, inline intent comments, and distinct escalation threshold.
- Verified no regressions after each task and at completion.
- Code review outcome: Changes Requested. Added 3 review follow-up items (2 Medium, 1 Low).
- ✅ Resolved review finding [Medium]: agent-specific prompt content is now explicitly enforced by tests and reflected in prompt text.
- ✅ Resolved review finding [Medium]: routing patterns now use word-boundary matching.
- ✅ Resolved review finding [Low]: model validation now accepts supported version-family updates via prefixes.

## File List

- _bmad-output/implementation-artifacts/1-3-scaffold-all-prompt-yaml-files-and-routing-config.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- prompts/dispatcher/.gitkeep (deleted)
- prompts/dispatcher/policy.yaml (created)
- prompts/dispatcher/v1.yaml (created)
- prompts/rag_agent/.gitkeep (deleted)
- prompts/rag_agent/policy.yaml (created)
- prompts/rag_agent/v1.yaml (created)
- prompts/research_agent/.gitkeep (deleted)
- prompts/research_agent/policy.yaml (created)
- prompts/research_agent/v1.yaml (created)
- prompts/response_synthesis/.gitkeep (deleted)
- prompts/response_synthesis/policy.yaml (created)
- prompts/response_synthesis/v1.yaml (created)
- prompts/guardrail/.gitkeep (deleted)
- prompts/guardrail/policy.yaml (created)
- prompts/guardrail/v1.yaml (created)
- prompts/followup/.gitkeep (deleted)
- prompts/followup/policy.yaml (created)
- prompts/followup/v1.yaml (created)
- config/routing_rules.yaml (created)
- tests/unit/test_prompt_scaffold_structure.py (created)
- tests/unit/test_prompt_policy_contract.py (created)
- tests/unit/test_prompt_v1_sections.py (created)
- tests/unit/test_routing_rules_config.py (created)
- tests/unit/test_prompt_policy_contract.py (modified)
- tests/unit/test_prompt_v1_sections.py (modified)
- tests/unit/test_routing_rules_config.py (modified)
- prompts/dispatcher/v1.yaml (modified)
- prompts/response_synthesis/v1.yaml (modified)
- prompts/guardrail/v1.yaml (modified)
- config/routing_rules.yaml (modified)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented Story 1.3 prompt/config scaffolding, added validation tests, and moved status to review after full suite pass.
- 2026-02-25: Senior Developer Review (AI) completed. Outcome: Changes Requested; status moved to in-progress with follow-up actions.
- 2026-02-25: Resolved AI-review follow-ups (2 Medium, 1 Low), reran full suite, and moved status back to review.
- 2026-02-25: Re-review completed. Outcome: Approved; status moved to done.

## Senior Developer Review (AI)

### Reviewer

Andrey

### Date

2026-02-25

### Outcome

Changes Requested

### Summary

- AC coverage is broadly implemented and tests are passing.
- 2 Medium and 1 Low issue remain for robustness/maintainability.
- Story is returned to `in-progress` until review follow-ups are resolved.

### Findings

1. [Medium] Task 3.2 requires agent-specific content, but current test coverage only validates non-empty sections and can allow generic copy/paste regressions. [tests/unit/test_prompt_v1_sections.py:26]
2. [Medium] Routing regex patterns are prone to false positives due to missing word boundaries in keyword alternatives. [config/routing_rules.yaml:9]
3. [Low] Model allowlist is hard-coded to exact versions, likely creating avoidable maintenance churn when approved model patch versions change. [tests/unit/test_prompt_policy_contract.py:17]

### Re-Review (AI)

#### Reviewer

Andrey

#### Date

2026-02-25

#### Outcome

Approved

#### Notes

- Validated all previously requested follow-ups as implemented.
- Re-ran full test suite successfully (`37 passed, 1 skipped`).
- No remaining High/Medium findings for Story 1.3.
