wine-view is a thin layer that connects agents to browsers via an editable CDP harness.

# Code priorities
- Clarity
- Precision
- Low verbosity
- Versatility

# Overview
Core code lives in `src/wine_view/`:
- `admin.py` — daemon lifecycle, diagnostics, updates, profile management
- `daemon.py` — the long-lived middleman process between the browser and the agent
- `helpers.py` — CDP wrapper and core browser primitives auto-imported into the scripts the CLI reads from stdin
- `run.py` — the `wine-view` CLI

`SKILL.md` tells agents how to use the harness and CLI.
`install.md` tells agents how to install it, attach a browser, and troubleshoot.

An agent operating the harness only edits inside `agent-workspace/`:
- `agent_helpers.py` — task-specific browser helpers the agent adds
- `domain-skills/` — skills the agent writes and reads

Package/CLI name = `wine-view`. Skill identity (`name` + trigger) = `wine-view`.

# Commands

From a **git checkout** (no global install required for local testing):

```bash
# doctor — install/daemon/browser state
./wine-view --doctor

# smoke — CDP attach + page_info (Chrome remote debugging must be allowed)
./wine-view <<'PY'
print(page_info())
PY

# unit tests (no live browser)
uv run --with pytest python -m pytest tests/unit -q

# after core/src edits: reload daemon so next call picks up code
./wine-view --reload
```

Notes:
- `./wine-view` = local tree launcher. Agents/docs outside this repo use the installed `wine-view` command.
- Integration tests under `tests/integration/` may need a live browser/CDP — prefer unit + doctor for routine PR gates.
- First-time install / blocked Chrome: follow `install.md` (`chrome://inspect/#remote-debugging`).

# Security
- Do not commit secrets, Browser Use Cloud tokens, or session cookies.
- Prefer the smallest change that fixes the bug; do not expand CDP surface without need.

# Contributing
Consider what is really needed. Prefer the smallest diff that fixes the bug.
Domain skills under `agent-workspace/domain-skills/` are agent-generated when possible — hand-author only when necessary.
