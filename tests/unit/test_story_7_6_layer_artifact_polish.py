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


def test_layer2_swap_points_are_explicit_design_statements() -> None:
    mock_kb = (REPO_ROOT / "src" / "concierge" / "agents" / "mock_knowledge_base.py").read_text(
        encoding="utf-8"
    )
    booking = (REPO_ROOT / "src" / "concierge" / "agents" / "booking_agent.py").read_text(
        encoding="utf-8"
    )
    token_budget = (
        REPO_ROOT / "src" / "concierge" / "agents" / "token_budget_manager.py"
    ).read_text(encoding="utf-8")

    assert "Production swap point:" in mock_kb
    assert "Replace with BedrockBookingAPI(region=X, api_key=...)" in booking
    assert (
        "In production, summarize when token count exceeds 6000 "
        "(leaving 2000 for output). Activation threshold: 80% of model context window."
        in token_budget
    )
