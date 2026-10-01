# Story 5.4: Implement Graceful Degradation When Web Search Unavailable

Status: review

## Story

As a **developer**,
I want the system to degrade gracefully when DuckDuckGo is unavailable or rate-limited, falling back to KB-only results with a visible label,
so that the demo doesn't fail on network issues.

## Acceptance Criteria

1. **Given** DuckDuckGo timeout or rate limit, **When** Research Agent catches the error, **Then** it sets `state["research_results"] = []` and `state["degradation_label"] = "[WEB SEARCH UNAVAILABLE — serving from internal KB only]"`
2. **Given** degradation, **When** it occurs, **Then** the error is caught at the Research Agent node boundary - no exception escapes to graph routing
3. **Given** `state["degradation_label"]` set, **When** Response Synthesis runs, **Then** it includes the label in the final response if only KB results are being cited
4. **And** `trace("research_agent", event="search_unavailable", reason="timeout")` is called
5. **Given** graceful degradation, **When** the user sees the response, **Then** they understand why only internal KB results are shown - the label is clear and helpful

## Tasks / Subtasks

- [x] Task 1: Add Story 5.4 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_5_4_research_degradation.py`
  - [x] 1.2: Add timeout degradation test for `research_results=[]`, `degradation_label`, and `search_unavailable` trace
  - [x] 1.3: Add rate-limit degradation test for reason mapping and no exception propagation
  - [x] 1.4: Add graph/node boundary test proving no exception escapes research route
  - [x] 1.5: Add response-synthesis label inclusion test for KB-only degraded output

- [x] Task 2: Implement graceful degradation behavior (AC: all)
  - [x] 2.1: Handle DuckDuckGo availability failures inside Research Agent and return degraded update
  - [x] 2.2: Emit `search_unavailable` trace with outcome reason
  - [x] 2.3: Ensure degraded state is user-visible through Response Synthesis labeling when only KB results are present

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 5.4 and impacted research/synthesis tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep degradation behavior non-crashing and explicit; avoid silent fallback.
- Keep successful search path behavior from Story 5.3 unchanged.
- Keep label logic scoped: apply when web search unavailable and KB-only path is active.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.4]
- [Source: src/concierge/agents/research_agent.py]
- [Source: src/concierge/agents/response_synthesis.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_4_research_degradation.py -q`
  - Result: 3 failed, 1 passed (expected before implementation)
- Story 5.4 validation:
  - `pytest tests/unit/test_story_5_4_research_degradation.py -q`
  - Result: 4 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_5_4_research_degradation.py tests/unit/test_story_5_3_research_agent_web_search.py tests/unit/test_state_reset.py tests/unit/test_story_2_1_graph_init_contract.py tests/unit/test_validate_config.py tests/unit/test_trace.py -q`
  - Result: 26 passed, 1 skipped
- Full regression:
  - `pytest tests -q`
  - Result: 145 passed, 2 skipped

### Completion Notes List

- Implemented graceful degradation in `ResearchAgent.run()` for DuckDuckGo failures: returns `research_results=[]`, sets user-visible degradation label, and avoids exception propagation.
- Added reason-aware degradation tracing: `search_unavailable` with `reason` (`timeout`, `rate_limit`, or `unavailable`).
- Added `degradation_label` to state initialization and turn-reset contract to prevent stale degradation labels across turns.
- Updated response synthesis to include degradation label for KB-only degraded paths when web results are unavailable.
- Updated an early stub-era graph test to allow evolved research-agent behavior while preserving core state contract checks.

### File List

- _bmad-output/implementation-artifacts/5-4-implement-graceful-degradation-when-web-search-unavailable.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/research_agent.py (modified)
- src/concierge/agents/response_synthesis.py (modified)
- src/concierge/agents/dispatcher.py (modified)
- src/concierge/state.py (modified)
- tests/unit/test_story_5_4_research_degradation.py (created)
- tests/unit/test_state_reset.py (modified)
- tests/unit/test_story_2_1_graph_init_contract.py (modified)
- tests/unit/test_story_2_2_node_stub_wiring.py (modified)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented web-search graceful degradation labeling and tracing with synthesis integration; validated targeted and full regression; set status to review.
