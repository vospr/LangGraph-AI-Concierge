"""The suite must not reach the network or a real Anthropic key (CI has neither)."""
from __future__ import annotations

import os

import pytest

from concierge.agents import research_agent


def test_web_search_is_blocked_unless_a_test_stubs_it() -> None:
    with pytest.raises(RuntimeError, match="network disabled in tests"):
        research_agent.search_duckduckgo("bali")


def test_no_anthropic_key_leaks_in_from_the_environment() -> None:
    assert "ANTHROPIC_API_KEY" not in os.environ
