# Story 2.4: Implement `--fast-mode` via Environment Variable and `AgentPolicy.model` Property

Status: review

## Story

As a **developer**,
I want `--fast-mode` to set `os.environ["FAST_MODE"] = "1"` and `AgentPolicy.model` to check this env var before returning the configured model,
so that lightweight testing is available without code changes.

## Acceptance Criteria

1. **Given** `python main.py --user alex --fast-mode`, **When** the flag is parsed, **Then** `os.environ["FAST_MODE"]` is set to `"1"` before any `AgentPolicy` instantiation
2. **Given** `AgentPolicy.model` as a property, **When** `FAST_MODE` env var is set, **Then** it returns `"claude-haiku-4-5"` regardless of the configured model in `policy.yaml`
3. **Given** `AgentPolicy.model` property, **When** `FAST_MODE` is not set, **Then** it returns the value from `policy.yaml` unchanged
4. **Given** `--fast-mode` active, **When** the session starts, **Then** a banner prints: `[FAST MODE] Using claude-haiku-4-5 across all agents - not the demo path`
5. **Given** `validate_config.py`, **When** `FAST_MODE` env var is set, **Then** the Opus model allow-list check is skipped

## Tasks / Subtasks

- [x] Task 1: Add contract tests for fast-mode runtime behavior and model override (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_2_4_fast_mode_contract.py`
  - [x] 1.2: Add test proving `main.py` sets `FAST_MODE=1` before runtime dependency loading
  - [x] 1.3: Add tests proving `AgentPolicy.model` returns configured model normally and Haiku override in fast mode
  - [x] 1.4: Add test proving fast-mode banner is printed once at session start
  - [x] 1.5: Add test proving `check_model_allowlist()` short-circuits when `FAST_MODE=1`

- [x] Task 2: Implement `main.py` fast-mode environment activation and banner (AC: 1, 4)
  - [x] 2.1: Set `os.environ["FAST_MODE"] = "1"` immediately after argument parsing when `--fast-mode` is present
  - [x] 2.2: Ensure env var is set before `_load_runtime_dependencies()` executes
  - [x] 2.3: Print fast-mode banner once before entering input loop
  - [x] 2.4: Keep non-fast-mode startup output unchanged (silent)

- [x] Task 3: Implement `AgentPolicy.model` property behavior (AC: 2, 3, 5)
  - [x] 3.1: Refactor `validate_config.AgentPolicy` to preserve configured model value while exposing `model` as property
  - [x] 3.2: Return `claude-haiku-4-5` when `FAST_MODE=1`, otherwise return configured model from policy YAML
  - [x] 3.3: Preserve existing policy validation behavior and schema loading
  - [x] 3.4: Keep allow-list skip behavior deterministic when `FAST_MODE=1`

- [x] Task 4: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5)
  - [x] 4.1: Run `pytest tests/unit/test_story_2_4_fast_mode_contract.py -q`
  - [x] 4.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 4.3: Update story `Dev Agent Record`, `File List`, and `Change Log`
  - [x] 4.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Keep boot order from Story 2.3 intact: Python version check first, runtime loading only after argument parse.
- FAST_MODE must be set before any runtime path that can instantiate or resolve `AgentPolicy.model`.
- Preserve current behavior that allow-list check is skipped when `FAST_MODE=1`.
- Do not alter non-fast-mode startup silence guarantees.

### Previous Story Intelligence

- Story 2.3 already introduced `main.py` parser and startup sequence.
- Story 2.3 tests assert non-fast-mode startup is silent; fast-mode banner must not regress this.
- `validate_config.check_model_allowlist` already has FAST_MODE guard; this story must keep that path and make model property consistent.

### Testing Notes

- Use monkeypatch to isolate environment variable side effects per test.
- Assert runtime order with a patched dependency loader and observable env state.
- Keep tests unit-level and deterministic; avoid network calls and full preflight execution.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.4]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4: `--fast-mode` Implementation]
- [Source: spec/concierge-spec.md#§AgentPolicy]
- [Source: _bmad-output/implementation-artifacts/2-3-implement-main-py-with-python-version-check-and-argument-parsing.md]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_2_4_fast_mode_contract.py -q` -> 3 failed (FAST_MODE not set before runtime loader, fast-mode banner missing, `AgentPolicy.model` not overriding in fast mode).
- Green phase: updated `main.py` to set `os.environ["FAST_MODE"]="1"` immediately after parsing `--fast-mode`.
- Green phase: added one-time startup banner `[FAST MODE] Using claude-haiku-4-5 across all agents - not the demo path` for fast-mode sessions.
- Green phase: refactored `validate_config.AgentPolicy` to store `configured_model` with alias `model` and expose `model` property with FAST_MODE override.
- Targeted validation: `pytest tests/unit/test_story_2_4_fast_mode_contract.py -q` -> 5 passed.
- Full regression: `pytest tests -q` -> 71 passed, 2 skipped.

### Completion Notes List

- Implemented fast-mode runtime activation in `main.py` before dependency loading to guarantee model override availability.
- Added contract coverage for fast-mode env timing, banner output, model property override semantics, and allow-list short-circuit behavior.
- Preserved Story 2.3 non-fast-mode silence behavior while adding fast-mode-only startup messaging.

### File List

- _bmad-output/implementation-artifacts/2-4-implement-fast-mode-via-environment-variable-and-agentpolicy-model-property.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_2_4_fast_mode_contract.py (created)
- main.py (modified)
- validate_config.py (modified)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented fast-mode env override and `AgentPolicy.model` property behavior; moved status to review after full suite pass.
