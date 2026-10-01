"""Routing eval: accuracy per route for rules-only vs rules+LLM.

    uv run python -m evals.routing_eval            # rules-only arm, print table
    uv run python -m evals.routing_eval --llm      # also the LLM arm (needs ANTHROPIC_API_KEY)
    uv run python -m evals.routing_eval --write    # store results in evals/results/

The harness drives the real DispatcherAgent.run(), so the fallback behaviour is the
graph's own: a turn no stage decides routes to "fallback".
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
from collections import Counter, defaultdict
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concierge import trace as trace_module  # noqa: E402
from concierge.agents.dispatcher import DispatcherAgent  # noqa: E402
from concierge.state import initialize_state  # noqa: E402

LABELS_PATH = Path(__file__).with_name("routing_labels.yaml")
RESULT_PATH = Path(__file__).parent / "results" / "routing_eval.json"
ROUTES = ("rag", "research", "booking_stub", "fallback")


class LlmUnavailable(RuntimeError):
    """The rules+LLM arm needs ANTHROPIC_API_KEY; it is never silently skipped."""


@dataclass(frozen=True)
class Row:
    text: str
    route: str


def load_labels(path: Path = LABELS_PATH) -> list[Row]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [Row(r["text"], r["route"]) for r in data["rows"]]


def score(rows: list[Row], predicted: list[str]) -> dict[str, Any]:
    per: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    confusion: dict[str, Counter[str]] = defaultdict(Counter)
    for row, pred in zip(rows, predicted, strict=True):
        per[row.route][0] += 1
        per[row.route][1] += row.route == pred
        confusion[row.route][pred] += 1
    correct = sum(c for _, c in per.values())
    return {
        "n": len(rows),
        "overall_accuracy": round(correct / len(rows), 4),
        "per_route": {
            r: {"n": per[r][0], "correct": per[r][1], "accuracy": round(per[r][1] / per[r][0], 4)}
            for r in ROUTES
            if per[r][0]
        },
        "confusion": {t: dict(sorted(c.items())) for t, c in sorted(confusion.items())},
    }


@contextmanager
def _env_key(present: bool) -> Iterator[None]:
    saved = os.environ.get("ANTHROPIC_API_KEY")
    if not present:
        os.environ.pop("ANTHROPIC_API_KEY", None)
    try:
        yield
    finally:
        if saved is None:
            os.environ.pop("ANTHROPIC_API_KEY", None)
        else:
            os.environ["ANTHROPIC_API_KEY"] = saved


@contextmanager
def _quiet_trace() -> Iterator[None]:
    saved = trace_module._trace_writer
    trace_module._trace_writer = io.StringIO()
    try:
        yield
    finally:
        trace_module._trace_writer = saved


def run_arm(rows: list[Row], *, use_llm: bool) -> dict[str, Any]:
    if use_llm and not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        raise LlmUnavailable("ANTHROPIC_API_KEY is not set; cannot run the rules+LLM arm")

    agent = DispatcherAgent()
    llm_calls = 0
    real_stage2 = agent._evaluate_stage2

    def counting_stage2(text: str) -> tuple[str | None, float | None, str | None]:
        nonlocal llm_calls
        llm_calls += 1
        return real_stage2(text)

    agent._evaluate_stage2 = counting_stage2  # type: ignore[method-assign]

    predicted: list[str] = []
    stage1_decided = 0
    with _env_key(use_llm), _quiet_trace():
        for i, row in enumerate(rows):
            stage1_decided += agent._evaluate_stage1(row.text)[2] is not None
            state = initialize_state("eval", f"eval-{i}", row.text, turn_id=1)
            update = agent.run(state)
            predicted.append(str(update.get("route") or "fallback"))
    llm_calls = llm_calls if use_llm else 0

    result = score(rows, predicted)
    result.update(
        arm="rules_plus_llm" if use_llm else "rules_only",
        stage1_decided=stage1_decided,
        llm_calls=llm_calls,
        model=agent.dispatcher_model if use_llm else None,
    )
    return result


def _table(results: dict[str, dict[str, Any]]) -> str:
    arms = list(results)
    lines = ["route".ljust(14) + "".join(a.ljust(18) for a in arms)]
    for route in (*ROUTES, "overall"):
        cells = []
        for a in arms:
            r = results[a]
            if route == "overall":
                cells.append(f"{r['overall_accuracy']:.0%} ({r['n']})")
            else:
                pr = r["per_route"][route]
                cells.append(f"{pr['accuracy']:.0%} ({pr['correct']}/{pr['n']})")
        lines.append(route.ljust(14) + "".join(c.ljust(18) for c in cells))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--llm", action="store_true", help="also run the rules+LLM arm")
    parser.add_argument("--write", action="store_true", help="write evals/results/routing_eval.json")
    args = parser.parse_args(argv)

    rows = load_labels()
    results = {"rules_only": run_arm(rows, use_llm=False)}
    if args.llm:
        results["rules_plus_llm"] = run_arm(rows, use_llm=True)
    print(_table(results))
    r = results["rules_only"]
    print(f"\nstage-1 decided {r['stage1_decided']}/{r['n']} rows without an LLM")
    if args.write:
        RESULT_PATH.parent.mkdir(exist_ok=True)
        RESULT_PATH.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
