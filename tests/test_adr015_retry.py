import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "adr015_retry", ROOT / "scripts/stage_d_adr015_retry.py"
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


@pytest.mark.parametrize(
    "code,status,message",
    [
        ("LimitExceeded", 400, "Out of host capacity"),
        ("NotAuthenticated", 401, "Out of host capacity"),
        ("NotAuthorizedOrNotFound", 404, "Out of host capacity"),
        ("TooManyRequests", 429, "Rate limit"),
        ("InternalError", 500, "Other service failure"),
    ],
)
def test_only_exact_capacity_failures_retry(code, status, message):
    assert not runner.capacity_error(runner.OCIError(status, {"code": code, "message": message}))


@pytest.mark.parametrize(
    "shape,ocpus,memory",
    [
        ("VM.Standard.E2.1.Micro", 2, 12),
        ("VM.Standard.A1.Flex", 4, 12),
        ("VM.Standard.A1.Flex", 2, 24),
    ],
)
def test_wrong_shape_or_size_is_p0(shape, ocpus, memory):
    with pytest.raises(RuntimeError, match="P0"):
        runner.validate_instance(
            {"shape": shape, "shapeConfig": {"ocpus": ocpus, "memoryInGBs": memory}}, "ad"
        )


def setup_run(tmp_path, monkeypatch, error):
    monkeypatch.setattr(runner, "oracle_enabled", lambda: True)
    proof = {
        "home_region": "ap-mumbai-1",
        "ad": "PeUh:AP-MUMBAI-1-AD-1",
        "compartment_id": "t",
        "zero_spend_confirmed": True,
        "billing_nonfree_observed": False,
        "existing_instances": [],
        "existing_storage_gb": 0,
        "subnet_id": "s",
        "image_id": "i",
        "ssh_public_key_file": str(tmp_path / "key.pub"),
        "capacity": "OUT_OF_HOST_CAPACITY",
    }
    (tmp_path / "key.pub").write_text("ssh-ed25519 test-public-key")
    (tmp_path / "proof.json").write_text(json.dumps(proof))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "runner",
            "--preflight",
            str(tmp_path / "proof.json"),
            "--state-dir",
            str(tmp_path / "run"),
            "--evidence",
            str(tmp_path / "evidence.json"),
            "--pin",
            "abc",
            "--execute",
        ],
    )
    monkeypatch.setattr(runner.oci_rest, "configure", lambda: ({"tenancy": "t"}, "ap-mumbai-1"))

    def check(cmd, **kwargs):
        if "rev-parse" in cmd:
            return "abc"
        return (ROOT / cmd[-1].split(":", 1)[1]).read_bytes()

    monkeypatch.setattr(runner.subprocess, "check_output", check)

    def get(service, path):
        if "regionSubscriptions" in path:
            return [{"isHomeRegion": True, "regionName": "ap-mumbai-1"}]
        if "/subnets/" in path:
            return {"lifecycleState": "AVAILABLE"}
        return {
            "lifecycleState": "AVAILABLE",
            "displayName": "Ubuntu-aarch64",
            "operatingSystem": "Canonical Ubuntu",
        }

    monkeypatch.setattr(runner, "get", get)
    monkeypatch.setattr(runner, "listing", lambda *args: [])
    count = []

    def call(*args, **kwargs):
        count.append(args)
        raise error

    monkeypatch.setattr(runner, "call", call)
    sleeps = []
    monkeypatch.setattr(runner.time, "sleep", sleeps.append)
    return count, sleeps


def test_exactly_500_capacity_attempts_499_backoffs(tmp_path, monkeypatch):
    count, sleeps = setup_run(
        tmp_path,
        monkeypatch,
        runner.OCIError(500, {"code": "InternalError", "message": "Out of host capacity."}),
    )
    runner.main()
    assert len(count) == 500 and sleeps == [60] * 499
    assert len((tmp_path / "run/attempts.jsonl").read_text().splitlines()) == 500
    assert json.loads((tmp_path / "run/state.json").read_text())["status"] == "bounds_exhausted"


def test_auth_failure_stops_after_one_attempt(tmp_path, monkeypatch):
    count, sleeps = setup_run(
        tmp_path,
        monkeypatch,
        runner.OCIError(401, {"code": "NotAuthenticated", "message": "Signature failed"}),
    )
    with pytest.raises(runner.OCIError):
        runner.main()
    assert len(count) == 1 and sleeps == []
    assert json.loads((tmp_path / "run/state.json").read_text())["status"] == "halted"


def test_24_hour_wall_deadline_prevents_attempts_after_sleep(tmp_path, monkeypatch):
    count, sleeps = setup_run(
        tmp_path,
        monkeypatch,
        runner.OCIError(500, {"code": "InternalError", "message": "Out of host capacity"}),
    )
    times = iter([0, 86401])
    monkeypatch.setattr(runner.time, "time", lambda: next(times))
    runner.main()
    assert count == [] and sleeps == []


def test_pivot_disables_oracle_before_loading_credentials(monkeypatch, tmp_path):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "runner",
            "--preflight",
            str(tmp_path / "missing"),
            "--state-dir",
            str(tmp_path / "run"),
            "--evidence",
            str(tmp_path / "evidence"),
            "--pin",
            "unused",
            "--execute",
        ],
    )
    with pytest.raises(SystemExit, match="Oracle disabled"):
        runner.main()
