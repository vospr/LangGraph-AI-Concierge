# Story 5.6: Enforce Per-Agent `max_tokens` Output Limit Before Each LLM Call

Status: review

## Story

As a **developer**,
I want the system to enforce per-agent `max_tokens` from `AgentPolicy` before any LLM call,
so that token budgets are predictable and Dispatcher's 128-token cap is honored.

## Acceptance Criteria

1. **Given** `prompts/dispatcher/policy.yaml` with `max_tokens: 128`, **When** Dispatcher is invoked, **Then** the LLM call includes `max_tokens=128`
2. **Given** `prompts/rag_agent/policy.yaml` with `max_tokens: 512`, **When** RAG Agent runs and LLM ranking is enabled, **Then** `max_tokens=512` is enforced
3. **Given** `prompts/research_agent/policy.yaml` with `max_tokens: 1024`, **When** Research Agent ranking runs, **Then** `max_tokens=1024` is used
4. **Given** LLM-calling agents, **When** inspected, **Then** Anthropic calls read policy-driven `max_tokens`
5. **Given** misconfigured `max_tokens`, **When** `validate_config.py` runs, **Then** it flags invalid/missing configuration before runtime
6. **And** Dispatcher's exact 128 cap is explicitly validated in `validate_config.py`

## Tasks / Subtasks

- [x] Task 1: Add Story 5.6 tests (AC: 1, 2, 3, 5, 6)
  - [x] 1.1: Create `tests/unit/test_story_5_6_max_tokens_enforcement.py`
  - [x] 1.2: Add RAG optional-ranking test asserting policy `max_tokens=512` on Anthropic call
  - [x] 1.3: Add validate-config test for missing `max_tokens`
  - [x] 1.4: Add validate-config test for dispatcher cap mismatch (`256` -> explicit error)

- [x] Task 2: Implement policy-driven max-token enforcement in remaining agent path (AC: 2, 4)
  - [x] 2.1: Extend `RAGAgent` to load `prompts/rag_agent/policy.yaml`
  - [x] 2.2: Add optional LLM ranking path guarded by `RAG_AGENT_LLM_RANKING=1`
  - [x] 2.3: Enforce `max_tokens=self._rag_max_tokens` in Anthropic `messages.create(...)`
  - [x] 2.4: Keep deterministic retrieval behavior unchanged when ranking disabled

- [x] Task 3: Validate and finalize (AC: all)
  - [x] 3.1: Run Story 5.6 + RAG regression tests
  - [x] 3.2: Run impacted dispatcher/research/config/policy regression
  - [x] 3.3: Run full suite `pytest tests -q`
  - [x] 3.4: Update sprint status to review

## Dev Notes

### Guardrails

- Dispatcher and Research max-token paths were already present and retained.
- RAG ranking remains opt-in and non-blocking; no Anthropic dependency on default deterministic path.
- `validate_config.py` behavior remains authoritative for misconfigured policy fields and dispatcher cap.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 5.6]
- [Source: src/concierge/agents/dispatcher.py]
- [Source: src/concierge/agents/research_agent.py]
- [Source: src/concierge/agents/rag_agent.py]
- [Source: validate_config.py]

## Dev Agent Record

### Agent Model Used

gpt-5-codex

### Debug Log References

- Red phase:
  - `pytest tests/unit/test_story_5_6_max_tokens_enforcement.py -q`
  - Result: 1 failed, 2 passed (`RAGAgent` did not yet call Anthropic ranking path)
- Story 5.6 validation:
  - `pytest tests/unit/test_story_5_6_max_tokens_enforcement.py tests/unit/test_story_5_2_rag_retrieval.py -q`
  - Result: 7 passed
- Targeted impacted validation:
  - `pytest tests/unit/test_story_5_6_max_tokens_enforcement.py tests/unit/test_story_3_4_stage2_llm_escalation.py tests/unit/test_story_5_3_research_agent_web_search.py tests/unit/test_prompt_policy_contract.py tests/unit/test_validate_config.py tests/unit/test_story_5_2_rag_retrieval.py -q`
  - Result: 23 passed, 1 skipped
- Full regression:
  - `pytest tests -q`
  - Result: 153 passed, 2 skipped

### Completion Notes List

- Implemented policy/prompt loading in `RAGAgent` and added optional Anthropic-based ranking path.
- Enforced `max_tokens` from `prompts/rag_agent/policy.yaml` on RAG ranking calls.
- Added Story 5.6 tests to verify RAG enforcement and validate-config early failure behavior for missing/incorrect `max_tokens`.
- Preserved existing Story 5.2 deterministic retrieval semantics when ranking is disabled.
- Confirmed existing Dispatcher (`128`) and Research (`1024`) max-token enforcement remains green.

### File List

- _bmad-output/implementation-artifacts/5-6-enforce-per-agent-max-tokens-output-limit-before-each-llm-call.md (created)
- _bmad-output/implementation-artifacts/sprint-status.yaml (modified)
- src/concierge/agents/rag_agent.py (modified)
- tests/unit/test_story_5_6_max_tokens_enforcement.py (created)

## Change Log

- 2026-02-25: Story file initialized and implementation started.
- 2026-02-25: Added RAG optional ranking max-token enforcement and Story 5.6 tests; validated targeted and full regression; moved status to review.
