"""Telemetry is removed in wine-view: nothing is collected or sent.

The functions remain only so callers keep working.
"""

import json


def is_enabled() -> bool:
    return False


def capture_cli_event(*args, **kwargs) -> None:
    return None


def run_telemetry_cli(argv: list[str]) -> int:
    print(json.dumps({"enabled": False, "note": "telemetry is removed in wine-view"}, indent=2))
    return 0
