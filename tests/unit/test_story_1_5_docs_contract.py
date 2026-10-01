from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPO_ROOT / "README.md"
MEMORY_README_PATH = REPO_ROOT / "memory" / "README.md"
ALEX_PROFILE_PATH = REPO_ROOT / "memory" / "profiles" / "alex.json"
ADR_DIR = REPO_ROOT / "docs" / "adr"
EXPECTED_ADRS = [
    "001-context-window-ownership.md",
    "002-multi-model-strategy.md",
    "003-anthropic-only-mvp.md",
    "004-file-based-memory.md",
    "005-langgraph-framework-selection.md",
]


def _readme_lines() -> list[str]:
    return README_PATH.read_text(encoding="utf-8").splitlines()


def _find_readme_line(lines: list[str], prefix: str) -> int:
    for idx, line in enumerate(lines):
        if line.strip() == prefix:
            return idx
    raise AssertionError(f"README is missing required line: {prefix!r}")


def test_readme_top_has_mermaid() -> None:
    lines = _readme_lines()
    first_screen = "\n".join(lines[:90])
    assert "```mermaid" in first_screen, "README top section must include Mermaid topology"


def test_alex_profile_demonstrates_full_userprofile_schema() -> None:
    data = json.loads(ALEX_PROFILE_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "alex.json must contain a JSON object"

    assert isinstance(data.get("user_id"), str) and data["user_id"], "user_id is required"
    assert isinstance(data.get("past_trips"), list) and data["past_trips"], (
        "past_trips list is required"
    )
    assert isinstance(data.get("preferences"), dict) and data["preferences"], (
        "preferences object is required"
    )
    assert isinstance(data.get("cached_research"), dict), (
        "cached_research session context is required"
    )
    assert isinstance(data.get("_demo_notes"), dict) and data["_demo_notes"], (
        "_demo_notes is required"
    )


def test_memory_readme_is_3_to_5_lines_and_explains_read_write_model() -> None:
    lines = [
        line.strip()
        for line in MEMORY_README_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert 3 <= len(lines) <= 5, "memory/README.md must be 3-5 non-empty lines"

    normalized = " ".join(lines).lower()
    for required_term in ("profile", "session", "read", "write"):
        assert required_term in normalized, f"memory/README.md must mention '{required_term}'"
