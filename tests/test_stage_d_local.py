import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("local_d", ROOT / "scripts/stage_d_local.py")
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


@pytest.mark.parametrize(
    "host,user",
    [
        ("8.8.8.8", "ubuntu"),
        ("100.2.3.4", "ubuntu"),
        ("100.64.0.2", "ubuntu;id"),
        ("::1", "ubuntu"),
    ],
)
def test_no_public_or_injected_endpoint(host, user):
    with pytest.raises(ValueError):
        local.endpoint(host, user)


def test_meshnet_ssh_requires_known_host_key():
    args = local.ssh_args("100.64.0.2", "ubuntu")
    assert args[-1] == "ubuntu@100.64.0.2"
    assert "StrictHostKeyChecking=yes" in args and "BatchMode=yes" in args


@pytest.mark.parametrize("arch", ["x86_64", "aarch64"])
def test_local_hardware_allows_kvm_and_both_architectures(arch):
    report = {
        "system": "Linux",
        "os_id": "ubuntu",
        "os_version": "22.04",
        "architecture": arch,
        "kvm_present": True,
    }
    report.update(
        {x: {"returncode": 0} for x in ["docker", "adb", "sudo", "binder_module", "ashmem_module"]}
    )
    local.require_host(report)
    report["binder_module"] = {"returncode": 1}
    with pytest.raises(ValueError, match="binder_module"):
        local.require_host(report)
