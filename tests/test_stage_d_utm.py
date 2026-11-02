import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("utm_d", ROOT / "scripts/stage_d_utm.py")
utm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utm)


def test_plan_never_connects_or_invokes_guest_agent(monkeypatch, tmp_path):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "utm",
            "--vm-id",
            "f28bdef7-5053-4b12-a98d-a33831b72167",
            "--identity",
            str(tmp_path / "absent-key"),
            "--known-hosts",
            str(tmp_path / "absent-hosts"),
        ],
    )

    def unexpected(*args, **kwargs):
        raise AssertionError("Plan must not connect, invoke UTM, or change guest permissions")

    monkeypatch.setattr(utm.subprocess, "run", unexpected)
    utm.main()


def test_invalid_vm_identity_rejected_before_guest_action(monkeypatch, tmp_path):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "utm",
            "--vm-id",
            "another machine; bad",
            "--identity",
            str(tmp_path / "key"),
            "--known-hosts",
            str(tmp_path / "hosts"),
            "--execute",
        ],
    )

    def unexpected(*args, **kwargs):
        raise AssertionError("Invalid VM id must not trigger a guest action")

    monkeypatch.setattr(utm.subprocess, "run", unexpected)
    with pytest.raises(SystemExit):
        utm.main()


def test_missing_completion_marker_has_a_hard_timeout(monkeypatch):
    times = iter([0, 2])
    monkeypatch.setattr(utm.time, "monotonic", lambda: next(times))
    with pytest.raises(TimeoutError, match="no success claimed"):
        utm.wait_json(["ssh"], "/missing-marker", 1)
