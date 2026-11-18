import base64
import io
import os
import tempfile

# The suite predates the own-Chrome default and asserts attach-to-local-Chrome behaviour.
# Opt out before any test module imports wine_view.
os.environ.setdefault("WV_CDP_WS", "")
# Keep test log lines out of the real wine-view home: a live daemon's log tail there
# drives the Chrome approval flow of whoever is waiting on it.
os.environ.setdefault("WV_HOME", tempfile.mkdtemp(prefix="wv-tests-"))

import pytest
from PIL import Image


def make_png(width, height):
    buf = io.BytesIO()
    Image.new("RGB", (width, height), "white").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


@pytest.fixture
def fake_png():
    return make_png


@pytest.fixture(autouse=True)
def _no_auto_approve(monkeypatch):
    monkeypatch.delenv("WV_AUTO_APPROVE", raising=False)
