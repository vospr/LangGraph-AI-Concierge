# Story 5.1: Create Mock JSON Knowledge Base with Production Swap-Point Comments

Status: review

## Story

As a **developer**,
I want a mock JSON Knowledge Base containing 5-10 travel destinations with production swap-point comments,
so that RAG Agent has structured data to retrieve from and future developers see exactly where to swap in AWS Bedrock.

## Acceptance Criteria

1. **Given** `agents/kb/knowledge_base.json`, **When** I parse it, **Then** it contains an array of destination objects with fields: `id`, `name`, `region`, `description`, `amenities`, `pricing`
2. **Given** the KB, **When** I read it, **Then** it includes >=5 real destinations (e.g., Bali, Phuket, Koh Samui, Tokyo, Bangkok) with substantive descriptions (>=3 sentences each)
3. **Given** the KB, **When** I search for `Production swap point`, **Then** a comment exists: `# Production swap point: replace MockKnowledgeBase with BedrockKnowledgeBase(kb_id=os.getenv("BEDROCK_KB_ID"))`
4. **Given** the mock KB, **When** RAG Agent queries it, **Then** keyword matching works: `beach` returns Bali/Phuket, `city` returns Tokyo/Bangkok
5. **And** the KB structure is self-documenting: a new developer can add a destination by copying an existing entry without reading code

## Tasks / Subtasks

- [x] Task 1: Add Story 5.1 tests (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Create `tests/unit/test_story_5_1_mock_knowledge_base.py`
  - [x] 1.2: Add KB parse/schema test for required destination fields
  - [x] 1.3: Add destination coverage test for >=5 real entries and >=3 sentence descriptions
  - [x] 1.4: Add production swap-point comment existence test
  - [x] 1.5: Add keyword-matching tests (`beach` -> Bali/Phuket, `city` -> Tokyo/Bangkok)
  - [x] 1.6: Add self-documenting structure consistency test across entries

- [x] Task 2: Implement mock KB asset and loader/query support (AC: all)
  - [x] 2.1: Add `agents/kb/knowledge_base.json` with structured destination records
  - [x] 2.2: Add mock KB utility with production swap-point comment and JSON load/query helpers
  - [x] 2.3: Expose minimal RAG-side query seam for Story 5.1 keyword matching validation

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run targeted Story 5.1 tests
  - [x] 3.2: Run full suite `pytest tests -q`
  - [x] 3.3: Update story record and sprint status to review

## Dev Notes

### Guardrails

- Keep 5.1 scoped to mock KB data + retrieval seam only; avoid full RAG orchestration behavior from Story 5.2.
- Keep KB shape easy to extend by copy-pasting one destination object.
- Keep swap-point guidance explicit and easy to find.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.1]
- [Source: src/concierge/agents/rag_agent.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_1_mock_knowledge_base.py -q`
  - Result: 5 failed (expected before implementation)
- Story 5.1 validation:
  - `pytest tests/unit/test_story_5_1_mock_knowledge_base.py -q`
  - Result: 5 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_2_2_node_stub_wiring.py tests/unit/test_story_3_7_per_turn_freshness_and_history_ownership.py tests/unit/test_story_5_1_mock_knowledge_base.py -q`
  - Result: 15 passed
- Full regression:
  - `pytest tests -q`
  - Result: 133 passed, 2 skipped

### Completion Notes List

- Added a structured mock travel KB at `agents/kb/knowledge_base.json` with six destination entries and consistent, copy-friendly schema.
- Added `MockKnowledgeBase` loader/query utility with explicit production swap-point comment for Bedrock-based KB replacement guidance.
- Added minimal RAG query seam (`query_mock_knowledge_base`) for keyword matching validation without implementing full Story 5.2 retrieval orchestration.
- Added Story 5.1 tests validating schema, destination coverage, swap-point guidance, keyword matching, and self-documenting entry consistency.

### File List

- _bmad-output/implementation-artifacts/5-1-create-mock-json-knowledge-base-with-production-swap-point-comments.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- agents/kb/knowledge_base.json (created)
- src/concierge/agents/mock_knowledge_base.py (created)
- src/concierge/agents/rag_agent.py (modified)
- tests/unit/test_story_5_1_mock_knowledge_base.py (created)

## Change Log

- 2026-02-25: Story file initialized and set to in-progress for implementation.
- 2026-02-25: Implemented mock KB data + production swap-point guidance + keyword query seam; validated targeted and full regression; set status to review.
