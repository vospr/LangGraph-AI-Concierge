from __future__ import annotations

from typing import Any, NotRequired

from typing_extensions import TypedDict


class ConciergeState(TypedDict):
    user_id: str
    session_id: str
    turn_id: int
    # Intentional deviation from CLAUDE_langgraph.md §3 (add_messages reducer):
    # This project uses plain dicts ({"role", "content"}) not LangChain BaseMessage objects.
    # The dispatcher owns and rebuilds this list each turn, preventing accidental overwrites.
    conversation_history: list[dict[str, Any]]
    current_input: str
    current_response: str
    intent: str | None
    confidence: float | None
    route: str | None
    rag_results: list[dict[str, Any]] | None
    research_results: list[dict[str, Any]] | None
    source_attribution: list[str]
    memory_profile: dict[str, Any] | None
    degradation_label: str | None
    guardrail_passed: bool
    proactive_suggestion: str | None
    clarification_needed: bool
    clarification_question: str | None
    human_handoff: bool
    error: str | None
    # Internal graph-tracking field used by tests to verify node execution order.
    _executed_nodes: NotRequired[list[str]]
    max_clarifications: NotRequired[int]


class StateUpdate(TypedDict, total=False):
    """A node's partial update: any subset of ConciergeState fields.

    `current_response` is Any because the booking agent hands a response object to
    synthesis, which turns it into text.
    """

    user_id: str
    session_id: str
    turn_id: int
    conversation_history: list[dict[str, Any]]
    current_input: str
    current_response: Any
    intent: str | None
    confidence: float | None
    route: str | None
    rag_results: list[dict[str, Any]] | None
    research_results: list[dict[str, Any]] | None
    source_attribution: list[str]
    memory_profile: dict[str, Any] | None
    degradation_label: str | None
    guardrail_passed: bool
    proactive_suggestion: str | None
    clarification_needed: bool
    clarification_question: str | None
    human_handoff: bool
    error: str | None
    _executed_nodes: list[str]
    max_clarifications: int


class TurnResetUpdate(TypedDict):
    intent: None
    confidence: None
    route: None
    rag_results: None
    research_results: None
    source_attribution: list[str]
    degradation_label: None
    guardrail_passed: bool
    proactive_suggestion: None
    clarification_needed: bool
    clarification_question: None
    human_handoff: bool
    error: None


class NodeName:
    DISPATCHER = "dispatcher"
    RAG = "rag"
    RESEARCH = "research"
    SYNTHESIS = "synthesis"
    GUARDRAIL = "guardrail"
    FOLLOWUP = "followup"
    BOOKING = "booking_stub"


def initialize_state(
    user_id: str,
    session_id: str,
    current_input: str = "",
    turn_id: int = 0,
) -> ConciergeState:
    return ConciergeState(
        user_id=user_id,
        session_id=session_id,
        turn_id=turn_id,
        conversation_history=[],
        current_input=current_input,
        current_response="",
        intent=None,
        confidence=None,
        route=None,
        rag_results=None,
        research_results=None,
        source_attribution=[],
        memory_profile=None,
        degradation_label=None,
        guardrail_passed=True,
        proactive_suggestion=None,
        clarification_needed=False,
        clarification_question=None,
        human_handoff=False,
        error=None,
    )
