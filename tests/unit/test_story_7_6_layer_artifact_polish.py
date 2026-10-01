from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_alex_profile_has_demo_notes_with_scenario() -> None:
    profile = json.loads((REPO_ROOT / "memory" / "profiles" / "alex.json").read_text(encoding="utf-8"))

    assert "_demo_notes" in profile
    demo_notes = profile["_demo_notes"]
    assert isinstance(demo_notes, dict)
    assert str(demo_notes.get("demo_scenario") or "").strip()


def test_memory_readme_explains_profile_vs_session_model_in_3_to_5_lines() -> None:
    text = (REPO_ROOT / "memory" / "README.md").read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    assert 3 <= len(lines) <= 5
    combined = " ".join(lines).lower()
    assert "profiles" in combined
    assert "sessions" in combined
