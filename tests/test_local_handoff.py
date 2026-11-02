import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_poweroff_never_targets_the_host_pid_namespace():
    stop = load("local_redroid_stop")
    info = {"HostConfig": {"PidMode": ""}, "State": {"Pid": 123}}
    assert stop.private_namespace(info, "pid:[host]", "pid:[private]")
    assert not stop.private_namespace(info, "pid:[host]", "pid:[host]")
    info["HostConfig"]["PidMode"] = "host"
    assert not stop.private_namespace(info, "pid:[host]", "pid:[private]")


def test_stop_rejects_unowned_container_before_docker(monkeypatch):
    stop = load("local_redroid_stop")

    def unexpected(*args, **kwargs):
        raise AssertionError("No Docker call allowed")

    monkeypatch.setattr(stop.subprocess, "check_output", unexpected)
    with pytest.raises(ValueError):
        stop.stop("unrelated-database")


def test_plugin_management_does_not_receive_server_flags():
    wrapper = load("local_appium_wrapper")
    assert wrapper.server_args(["plugin", "list", "--json"], Path("test.log")) == [
        "plugin",
        "list",
        "--json",
    ]
    args = wrapper.server_args(["--use-plugin=gads", "-p", "1234"], Path("test.log"))
    assert "--use-plugins=gads" in args
    assert args[-4:] == ["--address", "127.0.0.1", "--log", "test.log"]


def test_quickstart_plan_never_starts_vm_or_ssh(monkeypatch, tmp_path):
    start = load("local_quickstart")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "quickstart",
            "--vm-id",
            "f28bdef7-5053-4b12-a98d-a33831b72167",
            "--identity",
            str(tmp_path / "key"),
            "--known-hosts",
            str(tmp_path / "hosts"),
            "--magisk-apk",
            str(tmp_path / "magisk.apk"),
        ],
    )

    def unexpected(*args, **kwargs):
        raise AssertionError("Plan cannot invoke external commands")

    monkeypatch.setattr(start.subprocess, "run", unexpected)
    monkeypatch.setattr(start.subprocess, "check_output", unexpected)
    start.main()
