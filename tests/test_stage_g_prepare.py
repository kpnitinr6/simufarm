import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "stage_g_smoke", ROOT / "scripts/stage_g_appium_smoke.py"
)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


@pytest.mark.parametrize(
    "url",
    [
        "http://cloud.example:14723",
        "http://127.0.0.1:2222",
        "http://user:secret@localhost:14723",
        "http://localhost:14723/path",
    ],
)
def test_ssh_is_not_an_appium_endpoint_and_cloud_is_rejected(url):
    with pytest.raises(ValueError):
        smoke.local_endpoint(url)


def test_local_topology_has_no_cloud_or_automatic_schedule():
    topology = json.loads((ROOT / "infra/local-automation/topology.json").read_text())
    assert topology["cloud_endpoints"] == []
    assert topology["nightly_enabled"] is False
    assert topology["ssh"]["port"] == 2222
    assert topology["container_ceiling"] == 5
    assert smoke.local_endpoint("http://127.0.0.1:14723") == "http://127.0.0.1:14723"


def test_failed_smoke_deletes_created_session_and_records_failure(monkeypatch, tmp_path):
    calls = []

    def response(endpoint, method, path, data=None):
        calls.append((method, path))
        if path == "/status":
            return {"value": {"ready": True}}
        if path == "/session":
            return {"value": {"sessionId": "test-session"}}
        if method == "DELETE":
            return {"value": None}
        raise RuntimeError("synthetic source failure")

    monkeypatch.setattr(smoke, "request", response)
    with pytest.raises(RuntimeError, match="synthetic"):
        smoke.smoke("http://127.0.0.1:14723", {}, tmp_path / "result")
    assert calls[-1] == ("DELETE", "/session/test-session")
    report = json.loads((tmp_path / "result/result.json").read_text())
    assert report["passed"] is False and report["session_deleted"] is True
