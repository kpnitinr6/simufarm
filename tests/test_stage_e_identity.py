import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest
from simufarm_schema.models import DeviceProfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("stage_e_test", ROOT / "scripts/stage_e_remote.py")
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


def profile():
    return json.loads((ROOT / "data/runtime-test-profiles/vivo-x100-china.json").read_text())


def test_china_source_packet_is_complete_but_not_human_promoted():
    data = profile()
    DeviceProfile.model_validate(data)
    assert data["verified_by"] is None
    assert data["runtime_eligible"] is False
    assert runtime.properties(data)["ro.product.model"] == "V2309A"
    metadata = (ROOT / "data/research/stage-e-x100-china/ota-metadata.txt").read_text()
    assert "post-build=" + data["build"]["ro.build.fingerprint"] + "\n" in metadata
    assert "pre-device=" + data["build"]["ro.product.device"] + "\n" in metadata
    packet = json.loads((ROOT / "data/research/stage-e-x100-china/provenance.json").read_text())
    assert packet["actual_runtime_android"] == 13
    assert packet["fingerprint_firmware_android"] == 16


@pytest.mark.parametrize("change", ["india", "missing", "newline", "promoted"])
def test_reject_unknown_mixed_or_unapproved_scope(change):
    data = copy.deepcopy(profile())
    if change == "india":
        data["build"]["ro.build.fingerprint"] = "vivo/V2308/V2308:14/India"
    elif change == "missing":
        data["build"]["ro.product.model"] = None
    elif change == "newline":
        data["build"]["ro.build.fingerprint"] += "\npersist.evil=1"
    else:
        data["runtime_eligible"] = True
    with pytest.raises(ValueError):
        runtime.properties(data)


def test_synthetic_imei_namespace_and_checksum():
    for _ in range(30):
        value = runtime.imei()
        assert value.startswith("00000000") and len(value) == 15 and value.isdigit()
        total = sum(
            (int(x) * 2 // 10 + int(x) * 2 % 10) if i % 2 else int(x) for i, x in enumerate(value)
        )
        assert total % 10 == 0


def test_capacity_enforces_concurrency_and_host_memory_reserve():
    runtime.capacity(3, runtime.RESERVE + runtime.BUDGET * 2, 2)
    with pytest.raises(RuntimeError, match="ceiling"):
        runtime.capacity(4, 100 * 1024**3, 2)
    with pytest.raises(RuntimeError, match="reserve"):
        runtime.capacity(0, runtime.RESERVE + runtime.BUDGET - 1)


def test_boot_hook_runs_synchronously_after_persist_before_zygote():
    init = (ROOT / "infra/redroid-identity/init.rc").read_text()
    hook = "    exec -- /system/bin/sh /system/bin/simufarm-identity.sh"
    assert init.count(hook) == 1
    assert init.index("    load_persist_props\n") < init.index(hook)
    assert init.index(hook) < init.index("    start zygote\n")


def test_plan_performs_no_external_action(monkeypatch, tmp_path):
    import stage_e_utm

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "stage-e",
            "--vm-id",
            "f28bdef7-5053-4b12-a98d-a33831b72167",
            "--identity",
            str(tmp_path / "none"),
            "--known-hosts",
            str(tmp_path / "none"),
        ],
    )

    def unexpected(*args, **kwargs):
        raise AssertionError("Plan must perform no process or network call")

    monkeypatch.setattr(stage_e_utm.subprocess, "run", unexpected)
    stage_e_utm.main()
