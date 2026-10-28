"""Stage D guards; these tests make no OCI or Docker calls."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("remote_d", ROOT / "scripts/stage_d_remote.py")
remote = importlib.util.module_from_spec(spec)
spec.loader.exec_module(remote)


def pair():
    # Fictional test data only; never recorded as runtime observations.
    keys = ("android_id", "imei", "serial", "adb_serial")
    return [{k: f"synthetic-a-{k}" for k in keys}, {k: f"synthetic-b-{k}" for k in keys}]


def test_all_four_fields_must_be_different():
    data = pair()
    assert all(remote.identity_checks(data).values())
    data[1]["serial"] = data[0]["serial"]
    assert remote.identity_checks(data)["serial"] is False


def test_missing_imei_does_not_become_a_unique_value():
    data = pair()
    data[1]["imei"] = None
    assert remote.identity_checks(data)["imei"] is False


def test_one_successful_boot_cannot_pass_two_container_gate():
    assert not any(remote.identity_checks(pair()[:1]).values())
