"""README numbers that can be checked against the repo are checked here."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from evals import routing_eval as ev

ROOT = Path(__file__).resolve().parents[2]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _collected() -> dict[str, int]:
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-o", "addopts=", "-p", "no:cacheprovider"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    counts: dict[str, int] = {"unit": 0, "e2e": 0, "top": 0}
    for line in out.splitlines():
        if "::" not in line:
            continue
        parts = line.split("::")[0].split("/")
        counts[parts[1] if len(parts) > 2 else "top"] += 1
    return counts


def test_readme_test_counts_match_collection() -> None:
    c = _collected()
    total = sum(c.values())
    assert f"{total} tests collected" in README
    assert f"{c['unit']} in `tests/unit/`" in README
    assert f"{c['e2e']} in `tests/e2e/`" in README
    assert f"{total} tests, offline" in README


def test_readme_eval_table_matches_committed_result() -> None:
    data = json.loads(ev.RESULT_PATH.read_text(encoding="utf-8"))
    for arm, col in (("rules_only", 1), ("rules_plus_llm", 2)):
        for route, r in data[arm]["per_route"].items():
            row = next(line for line in README.splitlines() if line.startswith(f"| `{route}`"))
            cell = row.split("|")[col + 1].strip()
            assert cell == f"{r['accuracy']:.0%} ({r['correct']}/{r['n']})", (arm, route, cell)
        overall = next(line for line in README.splitlines() if line.startswith("| **Overall**"))
        cell = overall.split("|")[col + 1].strip("* ")
        n_ok = round(data[arm]["overall_accuracy"] * data[arm]["n"])
        assert cell == f"{data[arm]['overall_accuracy']:.0%} ({n_ok}/{data[arm]['n']})"
    u = data["rules_plus_llm"]["usage"]
    assert f"{u['input_tokens']:,} input and {u['output_tokens']:,} output tokens" in README
    assert f"{data['rules_plus_llm']['llm_calls']} calls" in README


def test_readme_kb_claim_matches_the_knowledge_base() -> None:
    kb = json.loads((ROOT / "agents" / "kb" / "knowledge_base.json").read_text(encoding="utf-8"))
    m = re.search(r"over (\d+) hand-written destinations", README)
    assert m and int(m.group(1)) == len(kb)


def test_readme_does_not_link_to_files_that_do_not_exist() -> None:
    for target in re.findall(r"\]\(((?!http|#)[^)]+)\)", README):
        assert (ROOT / target.split("#")[0]).exists(), target
