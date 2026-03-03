# Story 1.1: Initialize Repo with Git Discipline and Dependency Manifest

Status: review

## Story

As a **developer**,
I want the repo initialized with `.gitignore` committed as the first commit and all dependencies exact-pinned in `requirements.txt`,
so that sensitive files never appear in git history and the demo is reproducible on any machine.

## Acceptance Criteria

1. **Given** a fresh `git clone`, **When** I run `git log --oneline`, **Then** the first commit is `.gitignore` with no `.py` files in `agents/`, `nodes/`, or `graph/` present
2. **Given** `requirements.txt`, **When** I inspect it, **Then** all dependencies use `==` (not `>=`) and include `langgraph`, `anthropic`, `pydantic`, `duckduckgo-search`, and `pytest`
3. **Given** `memory/sessions/` directory, **When** I check `.gitignore`, **Then** `memory/sessions/` is listed and only `.gitkeep` is tracked
4. **Given** `.env.example`, **When** I read it, **Then** it documents `ANTHROPIC_API_KEY` without a value and no `.env` file exists in the repo

## Tasks / Subtasks

- [x] Task 1: Initialize git repository with .gitignore as first commit (AC: 1, 3)
  - [x] 1.1: Run `git init` in project root
  - [x] 1.2: Create `.gitignore` with required entries: `memory/sessions/*.json`, `!memory/sessions/.gitkeep`, `.env`, `__pycache__/`, `.venv/`, `*.pyc`, `*.pyo`, `dist/`, `build/`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
  - [x] 1.3: Stage and commit `.gitignore` ONLY as first commit: `git add .gitignore && git commit -m "chore: gitignore before any runtime files"`
  - [x] 1.4: Verify `memory/sessions/` is NOT in git after first commit (only `.gitkeep` tracked)
  - [x] 1.5: Write unit test `tests/unit/test_gitignore_coverage.py` verifying `.gitignore` contains required entries

- [x] Task 2: Create pyproject.toml and set up uv virtual environment (AC: 2)
  - [x] 2.1: Create `pyproject.toml` as the single source of truth for dependencies and tool config (see Dev Notes §pyproject.toml template)
  - [x] 2.2: Run `uv venv .venv && uv sync` to create virtual environment and lock file
  - [x] 2.3: Verify `uv.lock` is created — commit it alongside `pyproject.toml`
  - [x] 2.4: Write unit test `tests/unit/test_dependencies.py` verifying that `pyproject.toml` exists and is valid TOML

- [x] Task 3: Generate requirements.txt with exact pins (AC: 2)
  - [x] 3.1: Run `uv export --format requirements-txt > requirements.txt` to generate from `uv.lock`
  - [x] 3.2: Verify ALL dependencies use `==` operator (no `>=`, `~=`, `>`, `<`)
  - [x] 3.3: Verify required packages present: `langgraph`, `anthropic`, `pydantic`, `duckduckgo-search`, `pytest`
  - [x] 3.4: Write unit test `tests/unit/test_requirements_pins.py` that parses `requirements.txt` and asserts all deps use `==`

- [x] Task 4: Create .env.example with no values committed (AC: 4)
  - [x] 4.1: Create `.env.example` documenting `ANTHROPIC_API_KEY=` (no value — empty right side)
  - [x] 4.2: Verify no `.env` file exists in the repo (it must not be committed)
  - [x] 4.3: Write unit test `tests/unit/test_env_hygiene.py` asserting `.env.example` exists, `.env` does not exist, and `ANTHROPIC_API_KEY` is referenced in `.env.example`

- [x] Task 5: Scaffold empty directory structure with .gitkeep files (AC: 1, 3)
  - [x] 5.1: Create all top-level directories from the canonical structure: `src/concierge/agents/`, `config/`, `prompts/dispatcher/`, `prompts/rag_agent/`, `prompts/research_agent/`, `prompts/response_synthesis/`, `prompts/guardrail/`, `prompts/followup/`, `memory/profiles/`, `memory/sessions/`, `docs/adr/`, `tests/unit/`, `tests/integration/`
  - [x] 5.2: Add `.gitkeep` to ALL empty directories so they are tracked by git
  - [x] 5.3: Verify `memory/sessions/` contains only `.gitkeep` and the `*.json` pattern in `.gitignore` covers session files
  - [x] 5.4: Commit scaffolded structure: `git add . && git commit -m "chore: scaffold directory structure with gitkeeps"`

- [x] Task 6: Commit spec/concierge-spec.md as second meaningful commit (AC: 1)
  - [x] 6.1: Verify `spec/concierge-spec.md` already exists (it was written pre-implementation)
  - [x] 6.2: Stage and commit the spec: `git add spec/concierge-spec.md && git commit -m "spec: concierge spec before implementation"` — this MUST precede any `.py` files in `agents/`, `nodes/`, or `graph/`
  - [x] 6.3: Write unit test `tests/unit/test_spec_commit_order.py` that checks git log and asserts spec commit precedes any `agents/*.py` or `nodes/*.py` commit (Note: this test only becomes meaningful after agents are implemented — add as a placeholder with a skip marker for now)

- [x] Task 7: Create root conftest.py and tests/__init__.py scaffolding (AC: 2)
  - [x] 7.1: Create `tests/conftest.py` with shared state factory fixtures and tmp path helpers (no API mocking at root level per architecture decision)
  - [x] 7.2: Create `tests/unit/__init__.py` and `tests/integration/__init__.py` as empty files
  - [x] 7.3: Run `pytest tests/ -v` and confirm all new unit tests pass with 0 failures
  - [x] 7.4: Commit: `git add . && git commit -m "test: initial test scaffold and gitignore/requirements tests"`

## Dev Notes

### CRITICAL: Use `uv`, not `pip` directly

The package manager is `uv` (not pip). The workflow is:
```bash
uv venv .venv
source .venv/bin/activate  # Linux/macOS; on Windows: .venv\Scripts\activate
uv add langgraph anthropic pydantic duckduckgo-search python-dotenv
uv add --dev pytest pytest-asyncio ruff mypy pre-commit
uv export --format requirements-txt > requirements.txt
```
`pyproject.toml` is the source of truth. `uv.lock` is committed for reproducibility (exact hashes). `requirements.txt` is generated for pip fallback convenience.

### CRITICAL: Git commit order is enforced by architecture

The spec mandates this exact sequence:
1. `.gitignore` first (before anything runs)
2. `spec/concierge-spec.md` second (before any `.py` file in `agents/`, `nodes/`, `graph/`)
3. `pyproject.toml` + `uv.lock` + directory scaffolding
4. Everything else

Violating commit order is an architectural failure — not just bad practice.

### pyproject.toml template

```toml
[project]
name = "tnl-help"
version = "0.1.0"
description = "LangGraph multi-agent AI Concierge — portfolio demo"
requires-python = ">=3.11"
dependencies = [
    "langgraph>=1.0,<2.0",
    "anthropic>=0.40",
    "pydantic>=2.0",
    "duckduckgo-search>=6.0",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.3",
    "mypy>=1.8",
    "pre-commit>=3.6",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --strict-markers --asyncio-mode=auto"

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true

[tool.ruff]
line-length = 100
target-version = "py311"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Note: `pythonpath = ["src"]` must be in `[tool.pytest.ini_options]` so tests can import from `src/concierge/` without installing the package.

### .gitignore content (Windows-safe)

Per architecture FM7: on Windows, `.gitignore` Unix-prefix paths (`/memory/sessions/`) may not be honored by git for Windows. Use **no leading slash** for directory entries:

```
# Secrets — NEVER commit
.env

# Runtime-generated memory files — never commit session files
memory/sessions/*.json
!memory/sessions/.gitkeep

# Python artifacts
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Virtual environment
.venv/
venv/
env/

# Build artifacts
dist/
build/
*.egg-info/

# Test and tool caches
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/

# uv
# uv.lock is COMMITTED — do NOT add it here
```

### Canonical directory structure (from architecture.md)

```
tnl-help/
├── src/
│   └── concierge/
│       ├── __init__.py
│       ├── state.py
│       ├── graph.py
│       ├── nodes.py
│       ├── edges.py
│       ├── trace.py
│       ├── token_budget.py
│       └── agents/
│           ├── __init__.py
│           ├── dispatcher.py
│           ├── rag_agent.py
│           ├── research_agent.py
│           ├── response_synthesis.py
│           ├── guardrail.py
│           ├── followup.py
│           ├── booking_agent.py
│           └── memory_service.py
├── config/
│   └── routing_rules.yaml
├── prompts/
│   ├── dispatcher/
│   │   ├── policy.yaml
│   │   └── v1.yaml
│   ├── rag_agent/     (+ policy.yaml, v1.yaml)
│   ├── research_agent/
│   ├── response_synthesis/
│   ├── guardrail/
│   └── followup/
├── memory/
│   ├── profiles/
│   │   └── alex.json
│   ├── sessions/
│   │   └── .gitkeep
│   └── README.md
├── spec/
│   └── concierge-spec.md   ← already exists
├── docs/
│   └── adr/
│       ├── 001-context-window-ownership.md
│       ├── 002-multi-model-strategy.md
│       ├── 003-anthropic-only-mvp.md
│       ├── 004-file-based-memory.md
│       └── 005-langgraph-framework-selection.md
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── (test files)
│   └── integration/
│       ├── conftest.py
│       └── (test files)
├── main.py
├── validate_config.py
├── pyproject.toml      ← source of truth
├── uv.lock             ← committed
├── requirements.txt    ← generated from uv.lock
├── .env.example
├── .gitignore
├── CLAUDE.md
└── README.md
```

### Existing files to be aware of

The following already exist in the project root before Story 1.1 starts — do NOT delete or overwrite:
- `spec/concierge-spec.md` — THE authoritative spec (already written, must be committed as 2nd commit)
- `memory/profiles/` — contains `alex.json` (pre-seeded demo profile, committed)
- `memory/sessions/` — directory exists but must only have `.gitkeep` tracked
- `docs/` — contains existing reference documents

### Testing standards for this story

All tests in this story are pure unit tests (Tier 1) — no LLM calls, no mocking needed:

```python
# tests/unit/test_requirements_pins.py
from pathlib import Path

def test_all_requirements_use_exact_pins():
    req = Path("requirements.txt").read_text()
    lines = [l.strip() for l in req.splitlines() if l.strip() and not l.startswith("#")]
    for line in lines:
        if "==" not in line:
            # Allow lines like --index-url or -r includes
            if not line.startswith("-"):
                assert False, f"Dependency not exact-pinned: {line}"

def test_required_packages_present():
    req = Path("requirements.txt").read_text()
    for pkg in ["langgraph", "anthropic", "pydantic", "duckduckgo-search", "pytest"]:
        assert pkg in req, f"Required package missing from requirements.txt: {pkg}"
```

```python
# tests/unit/test_env_hygiene.py
from pathlib import Path

def test_env_example_exists():
    assert Path(".env.example").exists()

def test_env_file_not_committed():
    assert not Path(".env").exists(), ".env must never be committed to the repo"

def test_env_example_contains_anthropic_key():
    content = Path(".env.example").read_text()
    assert "ANTHROPIC_API_KEY" in content
```

```python
# tests/unit/test_gitignore_coverage.py
from pathlib import Path

def test_gitignore_exists():
    assert Path(".gitignore").exists()

def test_gitignore_covers_sessions():
    content = Path(".gitignore").read_text()
    assert "memory/sessions" in content or "sessions/*.json" in content

def test_gitignore_covers_env():
    content = Path(".gitignore").read_text()
    assert ".env" in content

def test_gitkeep_present_in_sessions():
    assert Path("memory/sessions/.gitkeep").exists()
```

### Project Structure Notes

- The canonical structure uses `src/concierge/` layout — tests import from `src/` via `pythonpath = ["src"]` in `pyproject.toml`
- `pyproject.toml` is the single source of truth; `requirements.txt` is a generated artifact
- `uv.lock` is committed (exact dependency hashes for reproducibility)
- Windows-specific: use `memory/sessions/*.json` (no leading `/`) in `.gitignore` for cross-platform compatibility

### References

- Architecture directory structure: [Source: _bmad-output/planning-artifacts/architecture.md#Canonical Directory Tree]
- Git commit sequence: [Source: _bmad-output/planning-artifacts/architecture.md#First Implementation Priority]
- gitignore FM7 Windows fix: [Source: _bmad-output/planning-artifacts/architecture.md#FM7]
- AC source: [Source: _bmad-output/planning-artifacts/epics.md#Story 1.1]
- spec contract: [Source: spec/concierge-spec.md]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- Fixed `test_pyproject_has_pytest_config` — TOML parses as `tool.pytest.ini_options`, not `tool.pytest` directly
- Fixed `requirements.txt` — initial `2>&1` redirect leaked uv progress line; used `2>nul` on Windows instead
- Added `[tool.hatch.build.targets.wheel] packages = ["src/concierge"]` to pyproject.toml — hatchling src-layout requires explicit package path

### Completion Notes List

- 21 unit tests passing, 1 skipped (spec commit order — awaits agents/ implementation in later stories)
- All 4 ACs satisfied: first commit is .gitignore; requirements.txt has exact == pins with all 5 required packages; memory/sessions gitignored with .gitkeep; .env.example has ANTHROPIC_API_KEY= with no value
- Git commit order correct: gitignore → spec/concierge-spec.md → pyproject + scaffold (no agents/.py yet)
- `uv` installed via pip (`python -m uv`); `.venv` created with Python 3.11.9; `uv.lock` committed
- `langgraph==1.0.9`, `anthropic==0.84.0`, `pydantic==2.12.5`, `duckduckgo-search==8.1.1`, `pytest==9.0.2`
- Dev tooling (`_bmad/`, `_bmad-output/`, `.agents/`, `.claude/`) re-added to .gitignore — not project code
- `.env` created locally with `ANTHROPIC_API_KEY` (gitignored, not committed)

### File List

- `.gitignore` (modified)
- `.env.example` (created)
- `pyproject.toml` (created)
- `uv.lock` (created)
- `requirements.txt` (created)
- `src/concierge/__init__.py` (created)
- `src/concierge/agents/__init__.py` (created)
- `tests/__init__.py` (created)
- `tests/conftest.py` (created)
- `tests/unit/__init__.py` (created)
- `tests/unit/test_dependencies.py` (created)
- `tests/unit/test_env_hygiene.py` (created)
- `tests/unit/test_gitignore_coverage.py` (created)
- `tests/unit/test_requirements_pins.py` (created)
- `tests/unit/test_spec_commit_order.py` (created)
- `tests/integration/__init__.py` (created)
- `tests/integration/conftest.py` (created)
- `config/.gitkeep` (created)
- `prompts/dispatcher/.gitkeep` (created)
- `prompts/rag_agent/.gitkeep` (created)
- `prompts/research_agent/.gitkeep` (created)
- `prompts/response_synthesis/.gitkeep` (created)
- `prompts/guardrail/.gitkeep` (created)
- `prompts/followup/.gitkeep` (created)
- `docs/adr/.gitkeep` (created)
- `docs/CLAUDE_langgraph.md` (created)
- `memory/sessions/.gitkeep` (created)
- `memory/profiles/alex.json` (created)
- `memory/README.md` (created)
- `spec/concierge-spec.md` (created)
