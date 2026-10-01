# Story 5.3: Implement Research Agent with DuckDuckGo Web Search

Status: review

## Story

As a **developer**,
I want the Research Agent to call DuckDuckGo search API, parse results, and return them as `state["research_results"]`,
so that live web search augments KB-only answers.

## Acceptance Criteria

1. **Given** user query `latest travel trends to Southeast Asia`, **When** Research Agent runs, **Then** it calls DuckDuckGo search with the query
2. **Given** DuckDuckGo results, **When** they're returned, **Then** the agent parses them into a list with fields: `title`, `link`, `snippet`
3. **Given** the Research Agent, **When** it completes, **Then** `state["research_results"]` is populated and `trace("research_agent", event="search_complete", results_count=N)` is called
4. **Given** the Research Agent, **When** it receives state, **Then** it operates on scoped context only (current query + last 3 turns max, not full conversation history) - FR14
5. **Given** the Research Agent, **When** results are returned, **Then** per-agent `max_tokens` is enforced before LLM-based result ranking/synthesis
6. **Given** DuckDuckGo success, **When** results are available, **Then** at least 3 results are returned (or fewer if search returns fewer)

## Tasks / Subtasks

- [x] Task 1: Add Story 5.3 tests (AC: 1, 2, 3, 4, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_5_3_research_agent_web_search.py`
  - [x] 1.2: Add DuckDuckGo query-call + parsed-fields test
  - [x] 1.3: Add scoped-context test for current query + last 3 turns only
  - [x] 1.4: Add `search_complete` trace emission test with `results_count`
  - [x] 1.5: Add result-count behavior tests for `>=3` when available and fewer when fewer returned
  - [x] 1.6: Add LLM-ranking-path max_tokens enforcement test using research policy

- [x] Task 2: Implement Research Agent web retrieval behavior (AC: all)
  - [x] 2.1: Implement DuckDuckGo search call helper and result parsing contract
  - [x] 2.2: Implement scoped query construction from current input + last 3 turns
  - [x] 2.3: Populate `research_results` and emit completion trace
  - [x] 2.4: Implement optional LLM-ranking path with policy `max_tokens` enforcement

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 5.3 and impacted research/graph tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep Story 5.3 scoped to successful web-search path and parsing (graceful degradation/error labeling belongs to Story 5.4).
- Keep FR14 context scoping explicit and testable.
- Do not regress existing graph/node boundary behavior.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.3]
- [Source: src/concierge/agents/research_agent.py]
- [Source: prompts/research_agent/policy.yaml]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_3_research_agent_web_search.py -q`
  - Result: 4 failed (expected before implementation)
- Story 5.3 validation:
  - `pytest tests/unit/test_story_5_3_research_agent_web_search.py -q`
  - Result: 4 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_5_1_mock_knowledge_base.py tests/unit/test_story_5_2_rag_retrieval.py tests/unit/test_story_5_3_research_agent_web_search.py tests/unit/test_trace.py -q`
  - Result: 38 passed
- Full regression:
  - `pytest tests -q`
  - Result: 141 passed, 2 skipped

### Completion Notes List

- Implemented DuckDuckGo search integration seam (`search_duckduckgo`) and normalized result parsing into `title`, `link`, `snippet`.
- Implemented FR14-scoped query construction using `current_input` plus at most the last 3 conversation turns.
- Implemented `ResearchAgent.run()` to populate `research_results` and emit `trace("research_agent", event="search_complete", results_count=N)`.
- Implemented optional LLM ranking path guarded by `RESEARCH_AGENT_LLM_RANKING=1`, enforcing `max_tokens` from `prompts/research_agent/policy.yaml`.
- Kept 5.3 scoped to successful search path; degradation/error-label behavior remains for Story 5.4.

### File List

- _bmad-output/implementation-artifacts/5-3-implement-research-agent-with-duckduckgo-web-search.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/research_agent.py (modified)
- tests/unit/test_story_5_3_research_agent_web_search.py (created)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented Research Agent DuckDuckGo retrieval, scoped context, parsing, trace output, and optional ranking token-limit enforcement; validated targeted and full regression; set status to review.
