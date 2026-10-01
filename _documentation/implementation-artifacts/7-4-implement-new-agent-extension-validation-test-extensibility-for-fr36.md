# Story 7.4: Implement New Agent Extension Validation Test (Extensibility for FR36)

Status: review

## Story

As a **developer**,
I want a mocked integration test that validates a new agent can be added with zero Dispatcher changes,
so that extensibility is proven and future contributors trust the architecture.

## Acceptance Criteria

1. **Given** `tests/test_new_agent_extension.py`, **When** I run it, **Then** a mocked test adds a hypothetical `hotel_agent` to the graph
2. **Given** the extension test, **When** it adds the agent, **Then** it: (1) creates `prompts/hotel_agent/policy.yaml`, (2) creates a mock `agents/hotel_agent.py` class, (3) wires one `add_node` in graph, (4) routes to it via Dispatcher
3. **Given** the routing, **When** user query matches `hotel`, **Then** Dispatcher routes to `hotel_agent` without any Dispatcher code changes
4. **Given** the test, **When** it passes, **Then** it proves FR36: adding a new agent requires new YAML + new node only, no Dispatcher rewrite
5. **And** the test is documented with a comment: `# This test proves extensibility. In production, follow these exact steps to add a new agent.`

## Tasks / Subtasks

- [x] Task 1: Add Story 7.4 extensibility test (AC: 1-5)
  - [x] 1.1: Create `tests/test_new_agent_extension.py`
  - [x] 1.2: Add required extensibility proof comment
  - [x] 1.3: In test flow, create temporary `prompts/hotel_agent/policy.yaml` and `agents/hotel_agent.py`
  - [x] 1.4: Wire one graph node for `hotel_agent` and assert execution path includes it
  - [x] 1.5: Verify Dispatcher routes hotel query to `hotel_agent` using configuration only

- [x] Task 2: Validate and finalize
  - [x] 2.1: Run Story 7.4 targeted test
  - [x] 2.2: Run full suite `pytest tests -q`
  - [x] 2.3: Update sprint status to review

## Dev Notes

### Guardrails

- Test uses temporary filesystem artifacts and graph monkeypatching to validate extension mechanics without mutating production source files.
- Dispatcher behavior is validated through configurable routing rules, not code edits.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 7.4]
- [Source: src/concierge/agents/dispatcher.py]
- [Source: src/concierge/graph/__init__.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Story 7.4 targeted validation:
  - `pytest tests/test_new_agent_extension.py tests/unit/test_story_7_3_demo_script.py tests/unit/test_story_3_3_stage1_prefilter.py -q`
  - Result: 8 passed
- Full regression:
  - `pytest tests -q`
  - Result: 182 passed, 2 skipped

### Completion Notes List

- Added `tests/test_new_agent_extension.py` that creates temporary `prompts/hotel_agent/policy.yaml` and `agents/hotel_agent.py` artifacts, then validates routing + graph execution for `hotel_agent`.
- Verified Dispatcher routes a hotel query via configuration-only Stage-1 rule, with no Dispatcher source edits required.
- Verified fallback graph executes `dispatcher -> hotel_agent -> guardrail -> synthesis` after wiring one new node and dispatcher conditional mapping in test setup.

### File List

- _bmad-output/implementation-artifacts/7-4-implement-new-agent-extension-validation-test-extensibility-for-fr36.md (created)
- tests/test_new_agent_extension.py (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)

## Change Log

- 2026-02-25: Story file initialized; extensibility test implemented.
- 2026-02-25: Story 7.4 validations passed; status moved to review.
