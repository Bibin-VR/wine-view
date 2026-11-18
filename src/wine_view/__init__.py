"""Wine View core package."""
import os
import sys

# Default browser on macOS: this agent session's own Chrome on a throwaway profile, driven
# over a private pipe (daemon._ChromePipe). No debugging port, nothing shared between
# sessions. An explicit endpoint in the environment opts out; WV_CDP_WS= (empty) attaches
# to the user's running Chrome instead. Elsewhere it is opt-in with WV_CDP_WS=pipe.
if sys.platform == "darwin" and not {"WV_CDP_WS", "WV_CDP_URL", "WV_BROWSER_ID"} & os.environ.keys():
    os.environ["WV_CDP_WS"] = "pipe"
if os.environ.get("WV_CDP_WS") == "pipe" and os.environ.get("CLAUDE_CODE_SESSION_ID"):
    os.environ.setdefault("WV_NAME", os.environ["CLAUDE_CODE_SESSION_ID"])
