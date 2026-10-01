"""
Root conftest.py — shared state factories and tmp path helpers.
Network and API key are blocked for every test by the autouse `_offline` fixture.
"""
from collections.abc import Callable
from pathlib import Path

import pytest

from concierge.agents.dispatcher import DispatcherAgent
from concierge.state import initialize_state

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def _offline(monkeypatch: pytest.MonkeyPatch) -> None:
    """No live web search and no real Anthropic key in any test.

    Tests that need either stub it themselves (their monkeypatch runs after this one).
    """
    from concierge.agents import research_agent

    def _blocked(query: str, max_results: int = 5) -> list[dict[str, object]]:
        raise RuntimeError("network disabled in tests")

    monkeypatch.setattr(research_agent, "search_duckduckgo", _blocked)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


@pytest.fixture
def repo_root() -> Path:
    """Returns the absolute path to the repository root."""
    return REPO_ROOT


@pytest.fixture
def tmp_memory_dir(tmp_path: Path) -> Path:
    """Creates a temporary memory directory structure for tests."""
    profiles = tmp_path / "memory" / "profiles"
    sessions = tmp_path / "memory" / "sessions"
    profiles.mkdir(parents=True)
    sessions.mkdir(parents=True)
    (sessions / ".gitkeep").touch()
    return tmp_path / "memory"


@pytest.fixture
def fresh_concierge_state() -> dict[str, object]:
    """Fresh state fixture with session id and optional outputs initialized."""
    return dict(
        initialize_state(
            user_id="alex",
            session_id="session-test-state-reset",
            current_input="",
            turn_id=0,
        )
    )


@pytest.fixture
def force_route(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    """Make the dispatcher pick a given route, to test graph topology in isolation.

    The dispatcher re-evaluates the route every turn, so a test can no longer
    pre-set state["route"] to steer the graph.
    """

    def _force(route: str) -> None:
        monkeypatch.setattr(
            DispatcherAgent,
            "_evaluate_stage1",
            lambda self, text: ("forced", 1.0, route),
        )

    return _force
