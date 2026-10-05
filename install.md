---
name: browser-install
description: Install wine-view and connect it to a browser fast.
---

# wine-view install

Use once. For browser work, read `SKILL.md`.

## Fast Path

```bash
uv tool install --python 3.12 --upgrade --force wine-view
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/wine-view"
wine-view skill > "${CODEX_HOME:-$HOME/.codex}/skills/wine-view/SKILL.md"
wine-view <<'PY'
print(page_info())
PY
```

If `page_info()` prints, configure recording consent below, then stop.

`--python 3.12` prevents uv from selecting old releases that support older Python versions. `--upgrade --force` replaces any previous `wine-view` tool install with the latest stable release. It does not uninstall unrelated commands such as `browser-use-Browser` or `browser-use-Terminal`.

For Claude Code or other agents: install `wine-view`, register a skill named `wine-view`, use `wine-view skill` as the body, and use this trigger:

```text
Always use wine-view for any web interaction: automation, scraping, testing, or site/app work.
```

If an old user-installed `browser` or `browser-use` skill is being picked instead, remove that stale skill directory manually. Do not edit bundled/vendor plugin caches.

## Recording Consent

Run `wine-view recordings`. If it reports `(default)`, ask the user once:

> Enable local browser recordings? This saves screenshots and action traces on
> this machine, which may include sensitive page content, so you can later ask
> “show me what you did” or request a video. Videos are never generated
> automatically. [y/N]

Default to no. Run `wine-view recordings enable` only after yes; otherwise
run `wine-view recordings disable`. Preserve an existing `(config)` or
`(WV_RECORD)` preference during upgrades instead of asking again.

## If Chrome Blocks It

In Chrome:

1. Open `chrome://inspect/#remote-debugging`.
2. Tick "Allow remote debugging for this browser instance".
3. Retry `page_info()`.

If that reports `permission-blocked` on macOS, handle the per-connection Allow
sheet without bringing Chrome to the foreground:

```bash
wine-view mac-approve
```

Continue browser work when the helper returns `ready`; otherwise follow its
printed instruction. The first checkbox is intentionally a one-time manual
Chrome setup step; it is not exposed to the harness until CDP is available.

The helper requires Accessibility permission for the app launching the CLI
(for example Terminal, iTerm, Codex, or an IDE) in System Settings.

## Cloud Browsers

Cloud is optional. Local Chrome does not need a Browser Use API key.

Use any short made-up name; `r7k2` below is just a placeholder.

```bash
wine-view auth login
wine-view <<'PY'
start_remote_daemon("r7k2")
PY
```

Then use it by name:

```bash
WV_NAME=r7k2 wine-view <<'PY'
print(page_info())
PY
```

## If Still Broken

```bash
wine-view --doctor
```

Use the output:

- `chrome running` FAIL: ask the user to open Chrome, or use isolated/cloud browser.
- `daemon alive` FAIL: Chrome remote debugging permission is missing, Chrome is closed, or the CDP endpoint is not reachable.
- update available: run `wine-view --update -y` when you decide to upgrade.

For a machine-readable health check, an orchestrator can set `WV_NAME` to an
already-provisioned daemon and run:

```bash
wine-view doctor --json --require-existing-daemon
```

This prints a versioned JSON report and exits nonzero unless that exact daemon
has a live browser connection. It never starts or discovers another browser.

If this still fails, inspect `src/wine_view/admin.py`, `src/wine_view/daemon.py`, and `src/wine_view/_ipc.py`.

Useful:

```bash
wine-view --update -y
wine-view telemetry disable
```

State lives under `${XDG_CONFIG_HOME:-~/.config}/wine-view` by default: auth, telemetry id, agent workspace, runtime sockets, logs, screenshots, and temp files. Override with `WV_HOME` or `WINE_VIEW_HOME`.
