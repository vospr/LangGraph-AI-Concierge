"""Acceptance checks for the routing eval (labelled set + harness + committed result)."""
from __future__ import annotations

import json
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest

from evals import routing_eval as ev

ROUTES = {"rag", "research", "booking_stub", "fallback"}


def test_labelled_set_has_about_40_rows_covering_every_route() -> None:
    rows = ev.load_labels()
    assert len(rows) >= 40
    assert len({r.text.lower() for r in rows}) == len(rows), "duplicate utterances"
    assert {r.route for r in rows} == ROUTES
    for route in ROUTES:
        assert sum(r.route == route for r in rows) >= 8, f"too few rows for {route}"


def test_score_reports_accuracy_per_route_and_confusion() -> None:
    rows = [
        ev.Row("a", "rag"),
        ev.Row("b", "rag"),
        ev.Row("c", "booking_stub"),
        ev.Row("d", "fallback"),
    ]
    result = ev.score(rows, ["rag", "fallback", "booking_stub", "booking_stub"])
    assert result["n"] == 4
    assert result["overall_accuracy"] == 0.5
    assert result["per_route"]["rag"] == {"n": 2, "correct": 1, "accuracy": 0.5}
    assert result["per_route"]["booking_stub"]["accuracy"] == 1.0
    assert result["per_route"]["fallback"]["accuracy"] == 0.0
    assert result["confusion"]["rag"]["fallback"] == 1
    assert result["confusion"]["fallback"]["booking_stub"] == 1


def test_rules_only_arm_makes_no_llm_call_even_if_a_key_is_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy")
    boom = ModuleType("anthropic")
    boom.Anthropic = lambda *a, **k: (_ for _ in ()).throw(AssertionError("LLM called"))  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "anthropic", boom)
    result = ev.run_arm(ev.load_labels(), use_llm=False)
    assert result["arm"] == "rules_only"
    assert result["llm_calls"] == 0


def test_committed_rules_only_result_matches_a_fresh_run() -> None:
    """The numbers quoted in the README must be reproducible from the repo."""
    committed = json.loads(ev.RESULT_PATH.read_text(encoding="utf-8"))
    fresh = ev.run_arm(ev.load_labels(), use_llm=False)
    assert committed["rules_only"] == fresh


def test_llm_arm_refuses_to_run_without_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ev.LlmUnavailable):
        ev.run_arm(ev.load_labels(), use_llm=True)


def test_llm_arm_calls_the_llm_only_for_rows_the_rules_do_not_decide(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Plumbing check with a fake client. The accuracy it yields is NOT a result."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy")
    calls: list[str] = []

    class _Messages:
        def create(self, **kwargs: Any) -> Any:
            calls.append(kwargs["messages"][0]["content"])
            block = SimpleNamespace(text='{"intent":"out_of_domain","confidence":0.9}')
            return SimpleNamespace(content=[block])

    fake = ModuleType("anthropic")
    fake.Anthropic = lambda *a, **k: SimpleNamespace(messages=_Messages())  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "anthropic", fake)

    rows = ev.load_labels()
    result = ev.run_arm(rows, use_llm=True)
    rules = ev.run_arm(rows, use_llm=False)

    assert result["arm"] == "rules_plus_llm"
    assert len(calls) == result["llm_calls"] == result["n"] - rules["stage1_decided"]
    assert result["stage1_decided"] == rules["stage1_decided"]
