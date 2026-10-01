"""Drives main.main() through 3 mixed turns and asserts on stdout.

Guards two defects that earlier tests missed because they never ran main.py:
the answer was never printed, and the route from turn 1 stuck on later turns.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

import main as cli
from concierge.agents import research_agent


def _fake_search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    return [
        {"title": "Thailand travel trends", "href": "https://example.test/th", "body": "Trend body."}
    ]


def _scripted(lines: list[str]) -> Any:
    feed: Iterator[str] = iter(lines)

    def _read(_prompt: str) -> str:
        try:
            return next(feed)
        except StopIteration:
            raise EOFError from None

    return _read


@pytest.fixture
def offline(monkeypatch: pytest.MonkeyPatch, tmp_path: Any) -> None:
    # validate_config requires a key to be present; SKIP_API_PROBE skips the live check.
    # All three inputs are stage-1 rule hits, so no LLM call is made.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy-not-used")
    monkeypatch.setenv("SKIP_API_PROBE", "1")
    monkeypatch.setattr(research_agent, "search_duckduckgo", _fake_search)
    monkeypatch.setattr(cli, "_persist_session_state", lambda *_a, **_k: None)


def test_three_mixed_turns_print_an_answer_each_and_route_per_turn(
    offline: None, capsys: pytest.CaptureFixture[str]
) -> None:
    code = cli.main(
        ["--user", "nobody"],
        input_reader=_scripted(
            [
                "what resort in bali has a spa",
                "book me a room",
                "latest travel trends in thailand",
            ]
        ),
    )
    out = capsys.readouterr().out

    assert code == 0
    # turn 2 must be routed to booking, not stay on the turn-1 RAG route
    assert "Booking is not available" in out
    # turn 3 must be routed to research
    assert "Thailand travel trends" in out
    # turn 1 answer (RAG) is printed, and comes before the booking answer
    assert "[RAG]" in out
    assert out.index("[RAG]") < out.index("Booking is not available")
