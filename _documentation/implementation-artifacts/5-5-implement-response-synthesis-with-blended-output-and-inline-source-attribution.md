# Story 5.5: Implement Response Synthesis with Blended Output and Inline Source Attribution

Status: review

## Story

As a **developer**,
I want Response Synthesis to merge RAG and Research results, generate a blended answer, and inline source tags (`[RAG]` vs `[Web]`),
so that the hiring manager sees sophisticated result synthesis in action.

## Acceptance Criteria

1. **Given** both `state["rag_results"]` and `state["research_results"]` populated, **When** Response Synthesis runs, **Then** it generates a blended response citing both sources
2. **Given** the blended response, **When** it is generated, **Then** `state["source_attribution"]` is populated with `[RAG]` and `[Web]` entries
3. **Given** `role: system_summary` messages in `conversation_history`, **When** Response Synthesis generates output, **Then** it filters them out before synthesis context building (FR27 complement)
4. **Given** only RAG results available (no web search), **When** Response Synthesis runs, **Then** it still generates a complete response, tagging sources as `[RAG]` only
5. **Given** the final response, **When** reviewed, **Then** sources are consistently tagged and distinguishable: `[RAG]` vs `[Web]`
6. **Given** BookingAgent stub response (Pydantic model), **When** Response Synthesis receives it, **Then** it formats the `message` field for user display without crashing
7. **And** `trace("response_synthesis", event="synthesis_complete", sources_cited=2)` is called for blended outputs

## Tasks / Subtasks

- [x] Task 1: Add Story 5.5 tests (AC: 1, 2, 3, 4, 5, 6, 7)
  - [x] 1.1: Create `tests/unit/test_story_5_5_response_synthesis_blending.py`
  - [x] 1.2: Add blended-output test for inline tags and trace emission
  - [x] 1.3: Add system-summary filtering test
  - [x] 1.4: Add RAG-only synthesis test
  - [x] 1.5: Add BookingAgent Pydantic-message formatting test
  - [x] 1.6: Add degraded KB-only synthesis test with label + `[RAG]`

- [x] Task 2: Implement response synthesis blending behavior (AC: all)
  - [x] 2.1: Refactor success-path orchestration in `ResponseSynthesisAgent`
  - [x] 2.2: Build blended response text with inline `[RAG]` and `[Web]` tags
  - [x] 2.3: Populate `source_attribution` with consistent tagged entries
  - [x] 2.4: Filter `system_summary` turns before response-context assembly
  - [x] 2.5: Handle booking-stub model/dict message extraction without crash
  - [x] 2.6: Preserve error/handoff behavior from Story 3.6

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 5.5 + Story 5.4 synthesis regression tests
  - [x] 3.2: Run broader impacted test slice for research/rag/graph/error/state/trace
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep label handling from Story 5.4 visible in KB-only degraded path.
- Keep node-boundary error/handoff suffix behavior unchanged.
- Keep synthesis deterministic (no LLM dependency required for this story).

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.5]
- [Source: src/concierge/agents/response_synthesis.py]
- [Source: tests/unit/test_story_5_4_research_degradation.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_story_5_4_research_degradation.py -q`
  - Result: 6 failed, 3 passed
- Story 5.5 + 5.4 validation:
  - `pytest tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_story_5_4_research_degradation.py -q`
  - Result: 9 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_5_5_response_synthesis_blending.py tests/unit/test_story_5_4_research_degradation.py tests/unit/test_story_5_3_research_agent_web_search.py tests/unit/test_story_5_2_rag_retrieval.py tests/unit/test_story_3_6_node_boundary_error_handling.py tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_state_reset.py tests/unit/test_trace.py -q`
  - Result: 41 passed
- Full regression:
  - `pytest tests -q`
  - Result: 150 passed, 2 skipped

### Completion Notes List

- Implemented `ResponseSynthesisAgent` success-path orchestration to generate blended, RAG-only, and Web-only responses with inline source tags.
- Added `source_attribution` generation with consistent `[RAG]`/`[Web]` tags.
- Added synthesis trace emission with `sources_cited` count by active source type.
- Added filtering of `system_summary` history entries before synthesis-context construction.
- Added booking-stub response formatting support for string/dict/model message payloads.
- Updated Story 5.4 degradation test expectation to assert label inclusion in full synthesized KB-only response.

### File List

- _bmad-output/implementation-artifacts/5-5-implement-response-synthesis-with-blended-output-and-inline-source-attribution.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/response_synthesis.py (modified)
- tests/unit/test_story_5_5_response_synthesis_blending.py (created)
- tests/unit/test_story_5_4_research_degradation.py (modified)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented response synthesis blending, attribution tags, system-summary filtering, and booking-model formatting; validated targeted and full regression; set status to review.
