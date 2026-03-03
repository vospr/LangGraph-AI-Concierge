# Story 3.2: Implement Centralized `trace()` Function with Field Allowlist/Denylist

Status: review

## Story

As a **developer**,
I want a centralized `trace(node_name, **kwargs)` function that enforces an allowlist of emittable fields and rejects any field containing sensitive data,
so that CLI trace output is safe and consistent across all nodes.

## Acceptance Criteria

1. **Given** the `trace()` function, **When** called with `trace("dispatcher", intent="travel", confidence=0.87)`, **Then** it prints `[dispatcher] intent=travel confidence=0.87`
2. **Given** the `trace()` function, **When** called with a denylist field like `trace("dispatcher", current_input="secret")`, **Then** it raises a `ValueError` with message `"current_input is not emittable"`
3. **Given** the denylist, **When** I inspect it, **Then** it includes: `current_input`, `memory_profile`, `conversation_history`, `rag_results`, `research_results`, and API-key fields
4. **Given** the allowlist, **When** I inspect it, **Then** it includes: `intent`, `confidence`, `route`, `model`, `session_id`, `turn_id`, and outcome-oriented fields
5. **Given** `nodes/*.py`, **When** I search for trace calls, **Then** every node calls `trace()` exactly once at start, never with ad-hoc f-strings
6. **And** `tests/unit/test_trace.py` validates denylist fields raise `ValueError` on trace attempts

## Tasks / Subtasks

- [x] Task 1: Add trace contract tests before implementation (AC: 1, 2, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_trace.py`
  - [x] 1.2: Add output-format test for allowlisted fields
  - [x] 1.3: Add denylist enforcement tests (`current_input`, API-key shaped fields)
  - [x] 1.4: Add allowlist/denylist contents tests
  - [x] 1.5: Add static node seam test ensuring one `trace()` call per node and no `print()` calls

- [x] Task 2: Implement centralized trace module (AC: 1, 2, 3, 4, 6)
  - [x] 2.1: Create `src/concierge/trace.py` with injectable writer and `trace(...)`
  - [x] 2.2: Define explicit allowlist and denylist constants
  - [x] 2.3: Raise actionable `ValueError` for denylisted/sensitive fields
  - [x] 2.4: Keep formatting deterministic and stable for unit tests

- [x] Task 3: Wire trace calls into all node seams (AC: 5)
  - [x] 3.1: Update each file in `src/concierge/nodes/*.py` to call `trace()` once at node start
  - [x] 3.2: Preserve Story 2.2 seam contract (single function, one return statement delegate form)
  - [x] 3.3: Ensure no ad-hoc trace printing in node seams

- [x] Task 4: Validate and finalize story implementation (AC: 1, 2, 3, 4, 5, 6)
  - [x] 4.1: Run `pytest tests/unit/test_trace.py -q`
  - [x] 4.2: Run full suite `pytest tests -q` and confirm no regressions
  - [x] 4.3: Update story `Dev Agent Record`, `File List`, and `Change Log`
  - [x] 4.4: Set story status to `review` only after all checks pass

## Dev Notes

### Implementation Guardrails

- Trace function is the only observability formatter; node seams must not use ad-hoc `print()` formatting.
- Keep node seam implementation compatible with Story 2.2 structural tests (single delegate function with one return statement).
- Denylist rejection should happen before emission; message format must be deterministic and actionable.
- Allowlist filtering should include routing essentials and outcome fields while excluding sensitive or internal payloads.

### Previous Story Intelligence

- Story 2.2 enforces strict node seam shape; Story 3.2 must add trace behavior without violating that contract.
- Story 3.1 introduced static enforcement patterns in `validate_config.py`; Story 3.2 should mirror that determinism in tests.
- Existing graph tests assert invocation path and state preservation; tracing changes must not mutate state.

### Testing Notes

- Use injectable writer (`_trace_writer`) and `io.StringIO` for output assertions.
- Use AST/static checks for node trace-call count and print prohibition.
- Keep tests pure-unit with no network and no runtime dependency on LLM clients.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.2]
- [Source: _bmad-output/planning-artifacts/architecture.md#CLI trace formatter]
- [Source: _bmad-output/planning-artifacts/architecture.md#Anti-Patterns (Forbidden)]
- [Source: _bmad-output/implementation-artifacts/2-2-build-langgraph-stategraph-with-all-7-nodes-wired-as-stubs.md]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_trace.py -q` -> 5 failed (`concierge.trace` missing, no trace calls in node seams).
- Green phase: added `src/concierge/trace.py` with explicit allowlist/denylist, injectable writer, and denylist/API-key rejection errors.
- Green phase: updated all seven node seam modules to call `trace()` exactly once while preserving one-function/one-return structural contract from Story 2.2.
- Compatibility validation: `pytest tests/unit/test_story_2_2_node_stub_wiring.py -q` -> 6 passed.
- Targeted validation: `pytest tests/unit/test_trace.py -q` -> 5 passed.
- Full regression: `pytest tests -q` -> 79 passed, 2 skipped.

### Completion Notes List

- Implemented centralized CLI trace formatter with deterministic output and explicit field safety controls.
- Added comprehensive unit coverage for output format, denylist rejection, allowlist contract, and node seam trace-call discipline.
- Integrated trace behavior into node seams without breaking prior Story 2.2 structural and runtime contracts.

### File List

- _bmad-output/implementation-artifacts/3-2-implement-centralized-trace-function-with-field-allowlist-denylist.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- tests/unit/test_trace.py (created)
- src/concierge/trace.py (created)
- src/concierge/nodes/dispatcher_node.py (modified)
- src/concierge/nodes/rag_node.py (modified)
- src/concierge/nodes/research_node.py (modified)
- src/concierge/nodes/booking_node.py (modified)
- src/concierge/nodes/guardrail_node.py (modified)
- src/concierge/nodes/synthesis_node.py (modified)
- src/concierge/nodes/followup_node.py (modified)

## Change Log

- 2026-02-25: Story file initialized and marked ready-for-dev.
- 2026-02-25: Implemented centralized `trace()` with allowlist/denylist and wired node seam trace calls; moved status to review after full suite pass.
