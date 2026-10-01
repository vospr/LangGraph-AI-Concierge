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
# USD per million tokens (input, output), Anthropic list prices as of 2026-09.
PRICES_PER_MTOK = {
    "claude-opus-4-6": (5.0, 25.0),
    "claude-haiku-4-5": (1.0, 5.0),
}


class LlmUnavailable(RuntimeError):
    """The rules+LLM arm needs ANTHROPIC_API_KEY; it is never silently skipped."""


def load_env(path: Path = ROOT / ".env") -> None:
    """Load the gitignored .env into this process only; never echoes values."""
    from dotenv import load_dotenv

    load_dotenv(path, override=False)


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


def run_arm(rows: list[Row], *, use_llm: bool, model: str | None = None) -> dict[str, Any]:
    if use_llm and not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        raise LlmUnavailable("ANTHROPIC_API_KEY is not set; cannot run the rules+LLM arm")

    agent = DispatcherAgent()
    if model is not None:
        agent._dispatcher_model = model
    llm_calls = 0
    real_stage2 = agent._evaluate_stage2

    def counting_stage2(text: str) -> tuple[str | None, float | None, str | None]:
        nonlocal llm_calls
        llm_calls += 1
        return real_stage2(text)

    setattr(agent, "_evaluate_stage2", counting_stage2)

    tokens = {"input_tokens": 0, "output_tokens": 0}
    real_extract = agent._extract_llm_text

    def metering_extract(response: Any) -> str:
        usage = getattr(response, "usage", None)
        tokens["input_tokens"] += int(getattr(usage, "input_tokens", 0) or 0)
        tokens["output_tokens"] += int(getattr(usage, "output_tokens", 0) or 0)
        return real_extract(response)

    setattr(agent, "_extract_llm_text", metering_extract)

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
    if use_llm:
        in_price, out_price = PRICES_PER_MTOK[agent.dispatcher_model]
        cost = (tokens["input_tokens"] * in_price + tokens["output_tokens"] * out_price) / 1e6
        result["usage"] = {**tokens, "cost_usd": round(cost, 6)}
    return result


def merge_results(path: Path, new: dict[str, Any]) -> None:
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    old.update(new)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(old, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _table(results: dict[str, dict[str, Any]]) -> str:
    order = ("rules_only", "rules_plus_llm", "rules_plus_llm_haiku")
    arms = [a for a in order if a in results] or list(results)
    lines = ["route".ljust(14) + "".join(a.ljust(22) for a in arms)]
    for route in (*ROUTES, "overall"):
        cells = []
        for a in arms:
            r = results[a]
            if route == "overall":
                cells.append(f"{r['overall_accuracy']:.0%} ({r['n']})")
            else:
                pr = r["per_route"][route]
                cells.append(f"{pr['accuracy']:.0%} ({pr['correct']}/{pr['n']})")
        lines.append(route.ljust(14) + "".join(c.ljust(22) for c in cells))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--llm", action="store_true", help="also run the rules+LLM arm")
    parser.add_argument(
        "--only-model",
        metavar="MODEL",
        help="run just one extra rules+LLM arm with MODEL (e.g. claude-haiku-4-5); "
        "with --write it is merged into the existing results file",
    )
    parser.add_argument(
        "--write", action="store_true", help="write evals/results/routing_eval.json"
    )
    args = parser.parse_args(argv)

    if args.llm or args.only_model:
        load_env()
    rows = load_labels()
    new: dict[str, dict[str, Any]] = {}
    if args.only_model:
        arm = "rules_plus_llm_haiku" if "haiku" in args.only_model else "rules_plus_llm_other"
        new[arm] = run_arm(rows, use_llm=True, model=args.only_model)
    else:
        new["rules_only"] = run_arm(rows, use_llm=False)
        if args.llm:
            new["rules_plus_llm"] = run_arm(rows, use_llm=True)
    if args.write:
        merge_results(RESULT_PATH, new)
    results = json.loads(RESULT_PATH.read_text(encoding="utf-8")) if args.write else new
    print(_table(results))
    for arm, r in results.items():
        if "usage" in r:
            u = r["usage"]
            print(
                f"\n{arm}: model={r['model']} calls={r['llm_calls']} "
                f"input_tokens={u['input_tokens']} output_tokens={u['output_tokens']} "
                f"cost=${u['cost_usd']:.4f}"
            )
    first = next(iter(results.values()))
    print(f"\nstage-1 decided {first['stage1_decided']}/{first['n']} rows without an LLM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
