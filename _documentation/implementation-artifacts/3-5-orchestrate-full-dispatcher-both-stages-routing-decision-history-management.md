# Story 3.5: Orchestrate Full Dispatcher - Both Stages, Routing Decision, History Management

Status: review

## Story

As a **developer**,
I want the Dispatcher to own full conversation history, execute Stage 1 then Stage 2 routing in order, emit one structured routing decision, and never generate user-facing text,
so the routing layer remains the architectural source of truth.

## Acceptance Criteria

1. **Given** `dispatcher.run(state)`, **When** called, **Then** it resets turn-scoped fields, appends user input to `conversation_history`, evaluates Stage 1, escalates to Stage 2 when needed, and sets route plus `current_response=None`
2. **Given** multi-turn flow, **When** Dispatcher handles successive turns, **Then** `conversation_history` preserves all previous turns verbatim and appends current user input before routing
3. **Given** an already-routed state (graph prepopulation path), **When** Dispatcher runs, **Then** it preserves route-prepopulated behavior used by existing graph stub tests
4. **Given** Dispatcher completion, **When** trace output is inspected, **Then** exactly one dispatcher routing trace is emitted with `intent`, `confidence`, and `route`
5. **Given** Stage 1 confidence above threshold, **When** Dispatcher runs, **Then** it routes directly and skips Stage 2
6. **Given** Stage 1 no-route, **When** Stage 2 returns high confidence, **Then** Dispatcher routes to specialist agent; otherwise fallback route is used
7. **And** Dispatcher respects policy `max_tokens=128` for Stage 2 LLM classification path

## Tasks / Subtasks

- [x] Task 1: Add orchestration-first tests (AC: 1, 2, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_3_5_dispatcher_orchestration.py`
  - [x] 1.2: Add test for reset payload + appended history + Stage 1 direct route + single trace
  - [x] 1.3: Add test for Stage 1 then Stage 2 call order and Stage 2 route result
  - [x] 1.4: Add multi-turn history ownership test proving verbatim carry-forward

- [x] Task 2: Implement full dispatcher orchestration (AC: 1, 2, 4, 5, 6)
  - [x] 2.1: Refactor `DispatcherAgent.run(...)` to construct update from `reset_turn_state(...)`
  - [x] 2.2: Append current user message to copied `conversation_history` before routing
  - [x] 2.3: Keep Stage 1 -> Stage 2 routing sequence and preserve prepopulated-route early return
  - [x] 2.4: Set `current_response` to `None` on every dispatcher turn
  - [x] 2.5: Emit one routing trace at run completion (stage marker preserved)

- [x] Task 3: Regression validation and finalize (AC: all)
  - [x] 3.1: Run targeted story tests for 3.3, 3.4, 3.5
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record, file list, and sprint status

## Dev Notes

### Implementation Guardrails

- Dispatcher returns update payload only; graph runtime applies state merge.
- Conversation history update is copy-based, preserving immutable input contract from graph tests.
- Routing trace emission moved to `run()` to guarantee single routing decision trace per turn.
- Stage 1/2 internals still provide deterministic route computation used by prior stories.

### Previous Story Intelligence

- Story 3.1 established reset contract (`reset_turn_state`) and stale-state prevention.
- Story 3.3 added Stage 1 deterministic rule-based pre-filter.
- Story 3.4 added Stage 2 LLM escalation and policy/prompt loading.

### Testing Notes

- New Story 3.5 tests use monkeypatched Stage 1/2 evaluators to isolate orchestration behavior.
- Existing Story 3.3 and 3.4 tests were rerun unchanged to validate backward compatibility.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.5]
- [Source: _bmad-output/planning-artifacts/architecture.md#Dispatcher Hybrid Routing Architecture]
- [Source: src/concierge/agents/dispatcher.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase: `pytest tests/unit/test_story_3_5_dispatcher_orchestration.py -q` -> 3 failed (`current_response` and `conversation_history` orchestration missing).
- Green phase: refactored `DispatcherAgent.run(...)` to:
  - apply `reset_turn_state(...)` payload
  - append current user input to `conversation_history`
  - preserve Stage 1/Stage 2 routing sequence
  - set `current_response=None`
  - emit exactly one dispatcher routing trace per turn
- Targeted validation: `pytest tests/unit/test_story_3_3_stage1_prefilter.py tests/unit/test_story_3_4_stage2_llm_escalation.py tests/unit/test_story_3_5_dispatcher_orchestration.py -q` -> 9 passed.
- Full regression: `pytest tests -q` -> 88 passed, 2 skipped.

### Completion Notes List

- Implemented Story 3.5 orchestration layer in Dispatcher, combining reset, history ownership, and staged routing decisions.
- Preserved existing graph stub route-prepopulation behavior and previous story contracts.
- Added focused unit coverage for sequencing and single-trace routing emission.

### File List

- _bmad-output/implementation-artifacts/3-5-orchestrate-full-dispatcher-both-stages-routing-decision-history-management.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/dispatcher.py (modified)
- tests/unit/test_story_3_5_dispatcher_orchestration.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Implemented dispatcher orchestration for reset/history/stage sequencing with single routing trace; validated with full regression; moved status to review.
