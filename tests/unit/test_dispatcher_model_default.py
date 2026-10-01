"""The router defaults to Haiku 4.5; Opus stays selectable through the policy file."""
from __future__ import annotations

from pathlib import Path

import yaml

from concierge.agents.dispatcher import DispatcherAgent
from evals import routing_eval as ev

POLICY = Path(__file__).resolve().parents[2] / "prompts" / "dispatcher" / "policy.yaml"


def test_shipped_policy_defaults_to_haiku() -> None:
    assert yaml.safe_load(POLICY.read_text(encoding="utf-8"))["model"] == "claude-haiku-4-5"
    assert DispatcherAgent().dispatcher_model == "claude-haiku-4-5"


def test_opus_is_still_selectable_by_editing_only_the_policy_file(tmp_path: Path) -> None:
    data = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    data["model"] = "claude-opus-4-6"
    alt = tmp_path / "policy.yaml"
    alt.write_text(yaml.safe_dump(data), encoding="utf-8")
    agent = DispatcherAgent(dispatcher_policy_path=alt)
    assert agent.dispatcher_model == "claude-opus-4-6"


def test_both_models_pass_the_config_allowlist_and_have_eval_prices() -> None:
    import validate_config

    allowed = set(validate_config.ALLOWED_MODEL_PREFIXES)
    assert {"claude-haiku-4-5", "claude-opus-4-6"} <= allowed
    assert {"claude-haiku-4-5", "claude-opus-4-6"} <= set(ev.PRICES_PER_MTOK)
