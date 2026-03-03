# Story 5.2: Implement RAG Agent to Retrieve from Mock JSON KB

Status: review

## Story

As a **developer**,
I want the RAG Agent to load the JSON KB, keyword-match the user query, and return relevant entries as `state["rag_results"]`,
so that Knowledge Retrieval routing produces structured, inspectable results.

## Acceptance Criteria

1. **Given** user query `Best beach destinations in Southeast Asia`, **When** RAG Agent runs, **Then** it queries the KB and returns entries where `region="Southeast Asia"` and amenities include `beach`
2. **Given** the RAG Agent, **When** `agents/rag_agent.py` is implemented, **Then** it receives only the current user query (FR14: scoped context, not full conversation history)
3. **Given** the RAG Agent, **When** it completes, **Then** `state["rag_results"]` is populated with a list of KB entries and `trace("rag_agent", event="retrieval_complete", results_count=N)` is called
4. **Given** the RAG Agent, **When** it queries the KB, **Then** per-agent `max_tokens` is enforced before any LLM call (if RAG uses LLM ranking)
5. **Given** no matching KB entries, **When** it occurs, **Then** `state["rag_results"] = []` (empty list, not `None`) and a fallback message is prepared

## Tasks / Subtasks

- [x] Task 1: Add Story 5.2 tests (AC: 1, 2, 3, 5)
  - [x] 1.1: Create `tests/unit/test_story_5_2_rag_retrieval.py`
  - [x] 1.2: Add southeast-asia beach retrieval test
  - [x] 1.3: Add scoped-context test proving only `current_input` is used
  - [x] 1.4: Add retrieval-complete trace test with `results_count`
  - [x] 1.5: Add no-match fallback test for empty list and prepared fallback message

- [x] Task 2: Implement RAG retrieval behavior from mock KB (AC: 1, 2, 3, 5)
  - [x] 2.1: Implement RAGAgent retrieval flow using current query only
  - [x] 2.2: Implement keyword-matching constraints for domain-relevant filtering
  - [x] 2.3: Emit retrieval trace with result count
  - [x] 2.4: Ensure no-match behavior returns empty list and fallback message

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 5.2 and impacted RAG tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep implementation scoped to mock KB retrieval only (no web and no synthesis behavior).
- Keep FR14 scoped-context guarantee explicit: use `current_input`, not full history.
- RAG in Story 5.2 performs deterministic retrieval only; no LLM ranking path required.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.2]
- [Source: src/concierge/agents/rag_agent.py]
- [Source: src/concierge/agents/mock_knowledge_base.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_2_rag_retrieval.py -q`
  - Result: 4 failed (expected before implementation)
- Story 5.2 validation:
  - `pytest tests/unit/test_story_5_2_rag_retrieval.py -q`
  - Result: 4 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_5_1_mock_knowledge_base.py tests/unit/test_story_5_2_rag_retrieval.py tests/unit/test_trace.py -q`
  - Result: 34 passed
- Full regression:
  - `pytest tests -q`
  - Result: 137 passed, 2 skipped

### Completion Notes List

- Implemented `RAGAgent.run()` to retrieve from mock KB using only `state["current_input"]` (FR14 scoped context).
- Added domain-relevant filtering constraints for `southeast asia`, `beach`, and `city` queries, with token-overlap filtering for other terms.
- Added retrieval trace emission: `trace("rag_agent", event="retrieval_complete", results_count=N)`.
- Implemented no-match fallback behavior: `rag_results=[]` and prepared fallback message `No matching internal KB destinations found.`.
- Kept Story 5.2 deterministic and non-LLM; per-agent `max_tokens` does not apply until/if LLM ranking is introduced in later stories.

### File List

- _bmad-output/implementation-artifacts/5-2-implement-rag-agent-to-retrieve-from-mock-json-kb.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/rag_agent.py (modified)
- tests/unit/test_story_5_2_rag_retrieval.py (created)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented RAG retrieval from mock KB with scoped input, trace emission, and no-match fallback; validated targeted and full regression; set status to review.
