# Story 2.3: Implement `main.py` with Python Version Check and Argument Parsing

Status: review

## Story

As a **developer**,
I want `main.py` to assert Python 3.11+, parse `--user` and `--fast-mode` flags, and call `validate_config.run_checks()` before graph import,
so that the entry point is self-guiding and catches errors early.

## Acceptance Criteria

1. **Given** Python < 3.11, **When** I run `python main.py`, **Then** an error prints before any imports: "Python 3.11+ required"
2. **Given** `main.py`, **When** I run `python main.py --help`, **Then** output documents `--user` (required) and `--fast-mode` (optional) flags
3. **Given** `--user alex`, **When** `main.py` runs, **Then** `state["user_id"] = "alex"` is set before graph invocation
4. **Given** `main.py`, **When** `validate_config.run_checks()` is called, **Then** it completes before `from graph import compiled_graph`
5. **Given** validation failure, **When** `main.py` runs, **Then** the error from `validate_config` is printed and `sys.exit(1)` is called
6. **Given** validation success, **When** `main.py` runs normally, **Then** no visible output until user input is expected

## Tasks / Subtasks

- [x] Task 1: Add contract-first tests for `main.py` startup behavior (AC: 1, 2, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_2_3_main_entrypoint.py`
  - [x] 1.2: Add test for Python 3.11 guard printing "Python 3.11+ required" and returning exit code `1`
  - [x] 1.3: Add test for `python main.py --help` exposing `--user` and `--fast-mode`
  - [x] 1.4: Add test proving `validate_config.run_checks()` executes before graph import
  - [x] 1.5: Add test proving validation failure exits with status `1`
  - [x] 1.6: Add test proving `state["user_id"]` is set before first graph invocation and startup is silent

- [x] Task 2: Implement `main.py` argument parsing and runtime bootstrap order (AC: 1, 2, 4, 5)
  - [x] 2.1: Add argparse parser with required `--user` and optional `--fast-mode`
  - [x] 2.2: Enforce Python version guard before project runtime imports (`validate_config`, `concierge.*`)
  - [x] 2.3: Ensure `validate_config.run_checks()` is called before importing graph runtime objects
  - [x] 2.4: Convert validation failure to process exit code `1` without stack trace output

- [x] Task 3: Implement minimal session loop bootstrap in `main.py` (AC: 3, 6)
  - [x] 3.1: Initialize state using parsed user id before first `compiled_graph.invoke(...)`
  - [x] 3.2: Add minimal input loop that invokes graph on non-empty user input
  - [x] 3.3: Keep startup silent (no banner/trace output from `main.py` before input prompt)
  - [x] 3.4: Parse `--fast-mode` now; defer env-var behavior and banner to Story 2.4

- [x] Task 4: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5, 6)
  - [x] 4.1: Run `pytest tests/unit/test_story_2_3_main_entrypoint.py -q`
  - [x] 4.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 4.3: Update story `Dev Agent Record`, `File List`, and `Change Log`
  - [x] 4.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Keep runtime import order strict: Python version guard first, then `validate_config.run_checks()`, then graph/state imports.
- Add `src` path bootstrapping in `main.py` so `python main.py ...` can import `concierge.*` reliably from repo root.
- Preserve Story 2.2 graph contracts: `compiled_graph.invoke(state)` must continue to work with `ConciergeState`.
- Parse `--fast-mode` in this story, but do not implement `FAST_MODE` env behavior or banner until Story 2.4.
- Keep `main.py` output minimal and deterministic; avoid startup prints on successful validation.

### Previous Story Intelligence

- Story 2.2 established that graph invocation path is deterministic and non-mutating for input state object.
- Node/agent seam is already wired under `src/concierge/nodes/` and `src/concierge/agents/`; `main.py` should only orchestrate startup and loop control.
- Existing tests depend on importable `concierge.graph.compiled_graph`; entrypoint changes must not break this import contract.

### Testing Notes

- Prefer isolated unit tests with monkeypatch for runtime ordering and failure cases.
- Use subprocess only where CLI parser output contract is required (`--help`).
- Avoid network-bound validations in story tests by patching runtime loader instead of invoking real API checks.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.3]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 3: `validate_config.py` Execution Model]
- [Source: _bmad-output/planning-artifacts/architecture.md#Decision 4: `--fast-mode` Implementation]
- [Source: spec/concierge-spec.md#§ValidateConfig]
- [Source: _bmad-output/implementation-artifacts/2-2-build-langgraph-stategraph-with-all-7-nodes-wired-as-stubs.md]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_2_3_main_entrypoint.py -q` -> 6 failed (`main.py` missing, `ModuleNotFoundError: main`).
- Green phase: created `main.py` with required `--user`/`--fast-mode` parser, Python 3.11 guard, and runtime loader order `validate_config.run_checks()` before importing graph/state.
- Green phase: added `src` path bootstrap for `python main.py` execution from repo root.
- Green phase: implemented minimal silent input loop with state initialization before first graph invocation.
- Targeted validation: `pytest tests/unit/test_story_2_3_main_entrypoint.py -q` -> 6 passed.
- Full regression: `pytest tests -q` -> 66 passed, 2 skipped.

### Completion Notes List

- Implemented Story 2.3 CLI entrypoint with strict startup gate ordering and argument parsing contracts.
- Added contract tests validating help output, import ordering, validation failure exit behavior, and state seeding before invoke.
- Kept startup behavior silent on success to preserve upcoming REPL-oriented stories.

### File List

- _bmad-output/implementation-artifacts/2-3-implement-main-py-with-python-version-check-and-argument-parsing.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_story_2_3_main_entrypoint.py (created)
- main.py (created)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented `main.py` entrypoint and Story 2.3 tests; moved status to review after full suite pass.
