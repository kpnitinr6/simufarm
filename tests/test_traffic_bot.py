import importlib.util
import shutil
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import call, patch

import pytest

SPEC = importlib.util.spec_from_file_location(
    "traffic", Path(__file__).parents[1] / "scripts/run_traffic_bot.py"
)
bot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bot)


REAL_MEMORY_HYGIENE = bot.memory_hygiene


@pytest.fixture(autouse=True)
def prevent_host_cache_changes(monkeypatch):
    monkeypatch.setattr(bot, "memory_hygiene", lambda **kwargs: {"status": "mocked"})


def test_proxy_rejects_credentials_before_docker(tmp_path):
    proxies = tmp_path / "proxies.txt"
    proxies.write_text("http://secret:password@127.0.0.1:8080\n")
    with patch.object(bot, "command") as command:
        assert bot.main(["--url", "https://example.com", "--proxy-file", str(proxies)]) == 1
        command.assert_not_called()
    assert bot.proxy_address("http://127.0.0.1:8080") == "127.0.0.1:8080"


def test_dry_run_all_csv_without_resources():
    with patch.object(bot, "command") as command:
        assert bot.main(["--url", "https://example.com", "--dry-run"]) == 0
        command.assert_not_called()
    assert len(bot.load_profiles(bot.ROOT / "data/devices.csv")) == 932


def test_remote_url_is_quoted():
    device = bot.Device("image", {"id": "test"}, 5575)
    with patch.object(bot, "command") as command:
        device.shell("am", "start", "-d", "https://example.com/?a=1&b=$(id)")
        assert "'https://example.com/?a=1&b=$(id)'" in command.call_args.args[-1]


def test_visit_failure_cleans_before_next_and_no_last_delay(tmp_path):
    events = []

    class FakeDevice:
        def __init__(self, image, row, port):
            self.row = row

        def start(self):
            events.append("start-" + self.row["id"])

        def shell(self, *args):
            return "14"

        def close(self):
            events.append("close-" + self.row["id"])

    args = SimpleNamespace(
        results=tmp_path, image="image", adb_port=5575, delay_min=60, delay_max=120
    )
    with (
        patch.object(bot, "Device", FakeDevice),
        patch.object(bot, "visit", side_effect=RuntimeError("failed")),
        patch.object(bot.time, "sleep") as sleep,
    ):
        assert bot.execute(args, [{"id": "a"}, {"id": "b"}], []) == 1
        assert events == ["start-a", "close-a", "start-b", "close-b"]
        sleep.assert_called_once()
        assert 60 <= sleep.call_args.args[0] <= 120
    assert len((tmp_path / "runs.jsonl").read_text().splitlines()) == 2


def test_cleanup_failure_aborts_batch(tmp_path):
    args = SimpleNamespace(
        results=tmp_path, image="image", adb_port=5575, delay_min=60, delay_max=120
    )
    with patch.object(bot, "Device") as device, patch.object(bot, "visit", return_value=3):
        device.return_value.shell.return_value = "14"
        device.return_value.close.side_effect = RuntimeError("cleanup failed")
        with pytest.raises(RuntimeError, match="cleanup failed"):
            bot.execute(args, [{"id": "a"}, {"id": "b"}], [])
        assert device.call_count == 1


def test_success_screenshot_and_swipe_count(tmp_path):
    device = bot.Device("image", {"id": "test", "width_px": 1080, "height_px": 2400}, 5575)

    def response(*args):
        if args[:2] == ("settings", "get"):
            return ":0"
        if args[0] == "cat":
            return bot.CHROME_FLAGS
        if args[:2] == ("am", "start"):
            return "Status: ok\nActivity: com.android.chrome/.Main"
        return ""

    png = b"\x89PNG\r\n\x1a\n" + b"test"
    args = SimpleNamespace(apk=None, url="https://example.com", results=tmp_path)
    with (
        patch.object(device, "shell", side_effect=response) as shell,
        patch.object(bot, "command", return_value=png),
        patch.object(bot.time, "sleep"),
    ):
        count = bot.visit(device, args, None, bot.random.Random(1))
    assert next(call.args for call in shell.call_args_list if call.args[:2] == ("am", "start")) == (
        "am",
        "start",
        "-W",
        "-n",
        "com.android.chrome/com.google.android.apps.chrome.Main",
        "-d",
        "https://example.com",
    )
    assert count == 3
    assert (tmp_path / "test.png").read_bytes() == png


def test_setup_error_cleans_and_aborts(tmp_path):
    args = SimpleNamespace(
        results=tmp_path, image="image", adb_port=5575, delay_min=60, delay_max=120
    )
    with (
        patch.object(bot, "Device") as device,
        patch.object(bot, "visit", side_effect=bot.SetupError("no browser")),
    ):
        device.return_value.shell.return_value = "14"
        with pytest.raises(bot.SetupError, match="no browser"):
            bot.execute(args, [{"id": "a"}, {"id": "b"}], [])
        device.return_value.close.assert_called_once()
        assert device.call_count == 1


@pytest.mark.parametrize("split", [False, True])
@pytest.mark.parametrize("install_timeout", [300, 1200])
def test_apk_install_mode_and_boot_order(tmp_path, split, install_timeout, caplog):
    base = tmp_path / "base.apk"
    base.touch()
    extra = tmp_path / "split_config.arm64_v8a.apk"
    if split:
        extra.touch()
    events = []
    device = bot.Device("image", {"id": "test"}, 5575)

    def command(*args, **kwargs):
        events.append(args)
        if args[0] == "adb" and args[3] in ("install", "install-multiple"):
            assert kwargs["timeout"] == install_timeout
            assert (
                "Installing APK bundle (this can take a few minutes on nested VMs)..."
                in caplog.text
            )
            assert f"timeout={install_timeout}s" in caplog.text
        if args[0] == "aapt":
            return "package: name='com.android.chrome' versionCode='1'"
        return "Success"

    with (
        patch.object(bot, "command", side_effect=command),
        patch.object(device, "shell", return_value="1") as shell,
        patch.object(bot.time, "sleep", side_effect=lambda t: events.append(("sleep", t))),
        caplog.at_level("INFO", logger="traffic"),
    ):
        assert (
            bot.install_apk(device, tmp_path if split else base, install_timeout)
            == "com.android.chrome"
        )
    assert events[0] == ("adb", "-s", device.serial, "wait-for-device")
    assert events[1] == ("sleep", 2)
    shell.assert_called_once_with("getprop", "sys.boot_completed", timeout=10)
    assert events[2] == ("aapt", "dump", "badging", str(base))
    expected = (
        "adb",
        "-s",
        device.serial,
        "install-multiple" if split else "install",
        "-r",
        str(base),
    )
    assert events[3] == expected + ((str(extra),) if split else ())


def test_empty_split_folder_rejected_before_docker(tmp_path):
    with patch.object(bot, "command") as command:
        assert bot.main(["--url", "https://example.com", "--apk", str(tmp_path)]) == 1
        command.assert_not_called()


def test_incomplete_boot_prevents_install(tmp_path):
    apk = tmp_path / "base.apk"
    apk.touch()
    device = bot.Device("image", {"id": "test"}, 5575)
    with (
        patch.object(bot, "command") as command,
        patch.object(device, "shell", return_value="0") as shell,
        patch.object(bot.time, "sleep") as sleep,
        pytest.raises(bot.InstallTimeout, match="boot is incomplete"),
    ):
        bot.install_apk(device, apk)
    assert shell.call_count == 3
    assert sleep.call_args_list == [call(10), call(10)]
    command.assert_called_once_with("adb", "-s", device.serial, "wait-for-device", timeout=30)


@pytest.mark.parametrize("csv_mode", [False, True])
def test_proxy_inputs_normalize_and_dry_run(tmp_path, csv_mode):
    path = tmp_path / ("proxies.csv" if csv_mode else "proxies.txt")
    path.write_text(
        'proxy,description\n"192.0.2.1:8080","quoted, field"\nhttp://192.0.2.2:3128,test\n'
        if csv_mode
        else "# test\n192.0.2.1:8080\nhttp://192.0.2.2:3128\n"
    )
    assert bot.load_proxies(path) == ["http://192.0.2.1:8080", "http://192.0.2.2:3128"]
    with patch.object(bot, "command") as command:
        assert (
            bot.main(["--url", "https://example.com", "--proxy-file", str(path), "--dry-run"]) == 0
        )
        command.assert_not_called()


def test_missing_proxy_column_rejected(tmp_path):
    path = tmp_path / "proxies.csv"
    path.write_text("host,port\n192.0.2.1,8080\n")
    with pytest.raises(ValueError, match="proxy column"):
        bot.load_proxies(path)


def test_boot_delay_before_adb_connection():
    events = []
    device = bot.Device("image", {"width_px": 1080, "height_px": 2400, "dpi": 400}, 5575)
    with (
        patch.object(bot, "command", side_effect=lambda *a, **kw: events.append(a) or ""),
        patch.object(bot.Path, "read_text", return_value="MemAvailable: 8000000 kB"),
        patch.object(bot.socket, "socket"),
        patch.object(device, "shell", return_value="1"),
        patch.object(bot.time, "sleep", side_effect=lambda t: events.append(("sleep", t))),
    ):
        device.start()
    started = next(i for i, item in enumerate(events) if item[:2] == ("docker", "run"))
    assert events[started + 1] == ("sleep", 15)
    assert events[started + 2] == ("adb", "connect", device.serial)


def test_cleanup_reset_failure_still_stops_and_removes():
    device = bot.Device("image", {"id": "test"}, 5575)
    device.created = True
    with (
        patch.object(device, "shell", side_effect=RuntimeError("offline")) as shell,
        patch.object(bot, "command") as command,
    ):
        device.close()
    shell.assert_called_once_with("settings", "put", "global", "http_proxy", ":0", timeout=10)
    assert command.call_args_list[0].args[:2] == ("docker", "stop")
    assert command.call_args_list[1].args == ("docker", "rm", "-f", "-v", device.name)
    assert device.created is False


def test_docker_stderr_is_actionable_and_redacted(capsys):
    result = SimpleNamespace(
        returncode=125,
        stdout="",
        stderr="invalid pid mode: private; https://user:secret@registry.example/image",
    )
    with (
        patch.object(bot.subprocess, "run", return_value=result),
        pytest.raises(bot.DockerCommandError) as caught,
    ):
        bot.command("docker", "create", "image")
    message = str(caught.value)
    assert "docker create failed (exit 125)" in message
    assert "invalid pid mode: private" in message
    assert "secret" not in message
    assert "[redacted]" in message
    printed = capsys.readouterr().err
    assert "invalid pid mode: private" in printed
    assert "secret" not in printed


def test_dynamic_port_and_clean_slate_without_invalid_pid_flag():
    events = []
    device = bot.Device("image", {"width_px": 1080, "height_px": 2400, "dpi": 400}, 0)

    def command(*args, **kwargs):
        events.append(args)
        return "127.0.0.1:49153" if args[:2] == ("docker", "port") else ""

    with (
        patch.object(bot, "command", side_effect=command),
        patch.object(bot.Path, "read_text", return_value="MemAvailable: 8000000 kB"),
        patch.object(device, "shell", return_value="1"),
        patch.object(bot.time, "sleep"),
    ):
        device.start()
    create = next(item for item in events if item[:2] == ("docker", "run"))
    assert "--pid=private" not in create
    assert create[2] == "-d"
    assert "--privileged" in create
    assert "--mount" not in create
    assert create[create.index("-v") + 1] == "/data"
    assert "127.0.0.1::5555" in create
    assert events.index(("docker", "rm", "-f", "-v", device.name)) < events.index(create)
    assert device.serial == "127.0.0.1:49153"
    assert ("adb", "connect", device.serial) in events


def test_fixed_port_in_use_has_clear_message():
    device = bot.Device("image", {"width_px": 1080, "height_px": 2400, "dpi": 400}, 5575)
    with (
        patch.object(bot, "command", return_value="") as command,
        patch.object(bot.Path, "read_text", return_value="MemAvailable: 8000000 kB"),
        patch.object(bot.socket, "socket") as sock,
    ):
        sock.return_value.__enter__.return_value.bind.side_effect = OSError("in use")
        with pytest.raises(bot.SetupError, match="omit --adb-port"):
            device.start()
        assert all(call.args[:2] != ("docker", "run") for call in command.call_args_list)


def test_missing_container_cleanup_does_not_hide_real_docker_errors():
    result = SimpleNamespace(
        returncode=1, stdout="", stderr="Error response from daemon: No such container: test"
    )
    with patch.object(bot.subprocess, "run", return_value=result):
        assert bot.command("docker", "rm", "-f", "test", missing_ok=True) == ""
        result.stderr = "permission denied while connecting to the Docker daemon"
        with pytest.raises(bot.DockerCommandError, match="permission denied"):
            bot.command("docker", "rm", "-f", "test", missing_ok=True)


def test_failed_create_cleanup_preserves_original_error(tmp_path):
    args = SimpleNamespace(results=tmp_path, image="image", adb_port=0, delay_min=60, delay_max=120)
    with patch.object(bot, "Device") as device:
        device.return_value.start.side_effect = bot.DockerCommandError("invalid pid mode")
        with pytest.raises(bot.DockerCommandError, match="invalid pid mode"):
            bot.execute(args, [{"id": "a"}], [])
        device.return_value.close.assert_called_once()
    assert "invalid pid mode" in (tmp_path / "runs.jsonl").read_text()


def test_explicit_binderfs_mount_not_apk_folder(tmp_path):
    events = []
    device = bot.Device(
        "redroid/redroid:14.0.0_64only-latest",
        {"width_px": 1080, "height_px": 2400, "dpi": 400},
        5575,
    )
    device.binderfs = tmp_path
    with (
        patch.object(bot, "command", side_effect=lambda *a, **kw: events.append(a) or ""),
        patch.object(bot.Path, "read_text", return_value="MemAvailable: 8000000 kB"),
        patch.object(bot.socket, "socket"),
        patch.object(device, "shell", return_value="1"),
        patch.object(bot.time, "sleep"),
    ):
        device.start()
    run = next(item for item in events if item[:2] == ("docker", "run"))
    assert f"type=bind,src={tmp_path},dst=/dev/binderfs" in run
    assert "redroid/redroid:14.0.0_64only-latest" in run
    assert all("chrome" not in item for item in run)


def test_missing_binderfs_path_rejected_without_docker(tmp_path):
    with patch.object(bot, "command") as command:
        assert (
            bot.main(
                [
                    "--url",
                    "https://example.com",
                    "--binderfs",
                    str(tmp_path / "missing"),
                    "--dry-run",
                ]
            )
            == 1
        )
        command.assert_not_called()


def test_version_marker_without_url_or_docker(capsys):
    with patch.object(bot, "command") as command:
        with pytest.raises(SystemExit) as caught:
            bot.main(["--version"])
        assert caught.value.code == 0
        command.assert_not_called()
    assert "teardown-recovery-v8" in capsys.readouterr().out


def test_docker_stdout_fallback_printed_immediately(capsys):
    result = SimpleNamespace(returncode=125, stdout="invalid argument from wrapper", stderr="")
    with (
        patch.object(bot.subprocess, "run", return_value=result),
        pytest.raises(bot.DockerCommandError),
    ):
        bot.command("docker", "run", "-d", "image")
    assert "invalid argument from wrapper" in capsys.readouterr().err


def test_complete_browser_flow_installs_and_sets_flags_before_url(tmp_path):
    events = []

    class FakeDevice:
        serial = "127.0.0.1:5555"

        def __init__(self, image, row, port):
            self.row = row

        def start(self):
            events.append("boot")

        def close(self):
            events.append("teardown")

        def shell(self, *args):
            if args[:2] == ("settings", "put"):
                events.append("proxy")
            elif args[:2] == ("settings", "get"):
                return ":0"
            elif args[:2] == ("sh", "-c"):
                assert "chrome --disable-fre --no-default-browser-check --no-first-run" in args[2]
                assert "/data/local/tmp/chrome-command-line" in args[2]
                events.append("flags")
            elif args[0] == "cat":
                return bot.CHROME_FLAGS
            elif args[:2] == ("am", "start"):
                events.append("url")
                return "Activity: com.android.chrome/.Main"
            elif args[:2] == ("input", "swipe"):
                events.append("swipe")
            return "14"

    def install(*args):
        assert args[2] == 1200
        events.append("install")
        return "com.android.chrome"

    def command(*args, **kwargs):
        events.append("screenshot")
        return b"\x89PNG\r\n\x1a\n" + b"test"

    args = SimpleNamespace(
        results=tmp_path,
        image="image",
        adb_port=0,
        delay_min=0,
        delay_max=0,
        install_timeout=1200,
        apk=Path("chrome"),
        url="https://example.com",
    )
    with (
        patch.object(bot, "Device", FakeDevice),
        patch.object(bot, "install_apk", side_effect=install),
        patch.object(bot, "command", side_effect=command),
        patch.object(bot.time, "sleep"),
    ):
        assert bot.execute(args, [{"id": "test", "width_px": 1080, "height_px": 2400}], []) == 0
    assert events[:5] == ["boot", "proxy", "install", "flags", "url"]
    assert all(event == "swipe" for event in events[5:-2])
    assert len(events[5:-2]) in (3, 4)
    assert events[-2:] == ["screenshot", "teardown"]


def test_failed_chrome_flag_write_verification_prevents_url(tmp_path):
    device = bot.Device("image", {"id": "test"}, 5575)
    args = SimpleNamespace(apk=None, url="https://example.com", results=tmp_path)

    def response(*args):
        return ":0" if args[:2] == ("settings", "get") else ""

    with (
        patch.object(device, "shell", side_effect=response) as shell,
        pytest.raises(bot.SetupError, match="flags did not persist"),
    ):
        bot.visit(device, args, None, bot.random.Random(1))
    assert all(call.args[:2] != ("am", "start") for call in shell.call_args_list)


@pytest.mark.parametrize("seconds", ["0", "-1"])
def test_invalid_install_timeout_rejected_before_resources(seconds):
    with patch.object(bot, "command") as command:
        assert (
            bot.main(["--url", "https://example.com", "--install-timeout", seconds, "--dry-run"])
            == 1
        )
        command.assert_not_called()


def test_install_timeout_reports_specific_deadline(tmp_path):
    apk = tmp_path / "base.apk"
    apk.touch()
    device = bot.Device("image", {"id": "test"}, 5575)

    def command(*args, **kwargs):
        if args[0] == "aapt":
            return "package: name='com.android.chrome'"
        if "install" in args:
            raise bot.subprocess.TimeoutExpired(args, kwargs["timeout"])
        return ""

    with (
        patch.object(bot, "command", side_effect=command),
        patch.object(device, "shell", return_value="1"),
        patch.object(bot.time, "sleep"),
        pytest.raises(bot.InstallTimeout, match="APK installation timed out after 300s"),
    ):
        bot.install_apk(device, apk)


def test_install_boot_checks_retry_then_install(tmp_path):
    apk = tmp_path / "base.apk"
    apk.touch()
    device = bot.Device("image", {"id": "test"}, 5575)

    def command(*args, **kwargs):
        return "package: name='com.android.chrome'" if args[0] == "aapt" else "Success"

    with (
        patch.object(bot, "command", side_effect=command),
        patch.object(device, "shell", side_effect=["0", "0", "1"]) as shell,
        patch.object(bot.time, "sleep") as sleep,
    ):
        assert bot.install_apk(device, apk) == "com.android.chrome"
    assert shell.call_count == 3
    assert sleep.call_args_list == [call(10), call(10), call(2)]


def test_hung_kill_server_cannot_prevent_forced_removal():
    device = bot.Device("image", {"id": "test"}, 5575)
    device.created = True
    events = []

    def command(*args, **kwargs):
        events.append((args, kwargs))
        if args == ("adb", "kill-server"):
            raise bot.subprocess.TimeoutExpired(args, kwargs["timeout"])
        return ""

    with patch.object(bot, "command", side_effect=command):
        recovery = device.recover_install_timeout()
        device.close()
    assert events[0] == (("adb", "kill-server"), {"timeout": 10, "check": False})
    assert events[1] == (
        ("docker", "rm", "-f", "-v", device.name),
        {"timeout": 30, "missing_ok": True},
    )
    assert len(events) == 2
    assert device.serial is None and device.created is False
    assert recovery["forced_container_removal"] is True


def test_install_stall_recovers_before_booting_next_device(tmp_path):
    events = []

    class FakeDevice:
        def __init__(self, image, row, port):
            self.row = row

        def start(self):
            events.append("start-" + self.row["id"])

        def shell(self, *args):
            return "14"

        def recover_install_timeout(self):
            events.append("recover-" + self.row["id"])
            return {"forced_container_removal": True}

        def close(self):
            events.append("close-" + self.row["id"])

    args = SimpleNamespace(results=tmp_path, image="image", adb_port=0, delay_min=0, delay_max=0)
    with (
        patch.object(bot, "Device", FakeDevice),
        patch.object(bot, "visit", side_effect=[bot.InstallTimeout("APK stalled"), 3]),
        patch.object(bot.time, "sleep"),
    ):
        assert bot.execute(args, [{"id": "a"}, {"id": "b"}], []) == 1
    assert events == ["start-a", "recover-a", "close-a", "start-b", "close-b"]
    records = [bot.json.loads(line) for line in (tmp_path / "runs.jsonl").read_text().splitlines()]
    assert records[0]["status"] == "failed"
    assert records[0]["recovery"]["forced_container_removal"] is True
    assert records[1]["status"] == "passed"


def test_failed_force_removal_aborts_without_overlapping_devices(tmp_path):
    args = SimpleNamespace(results=tmp_path, image="image", adb_port=0, delay_min=0, delay_max=0)
    with (
        patch.object(bot, "Device") as device,
        patch.object(bot, "visit", side_effect=bot.InstallTimeout("stalled")),
        pytest.raises(bot.DockerCommandError, match="remove failed"),
    ):
        device.return_value.shell.return_value = "14"
        device.return_value.recover_install_timeout.side_effect = bot.DockerCommandError(
            "remove failed"
        )
        bot.execute(args, [{"id": "a"}, {"id": "b"}], [])
    assert device.call_count == 1


def test_low_memory_waits_then_recovers():
    with (
        patch.object(
            bot, "memory_snapshot", side_effect=[{"MemAvailable": 2400}, {"MemAvailable": 4000}]
        ),
        patch.object(bot, "memory_hygiene") as cleanup,
        patch.object(bot.time, "sleep") as sleep,
    ):
        bot.wait_for_memory()
    cleanup.assert_called_once_with(enabled=True)
    sleep.assert_called_once_with(30)


def test_persistent_low_memory_stops_after_bounded_retries():
    with (
        patch.object(bot, "memory_snapshot", return_value={"MemAvailable": 2000}) as measure,
        patch.object(bot.time, "sleep") as sleep,
        pytest.raises(bot.SetupError, match="stopping batch instead of skipping"),
    ):
        bot.wait_for_memory(retries=3)
    assert measure.call_count == 4
    assert sleep.call_args_list == [call(30)] * 3


@pytest.mark.parametrize(
    "outcome", [3, RuntimeError("failed visit"), bot.InstallTimeout("stalled")]
)
def test_memory_cleanup_runs_after_every_device_teardown(tmp_path, outcome):
    events = []
    args = SimpleNamespace(results=tmp_path, image="image", adb_port=0, delay_min=0, delay_max=0)

    def cleanup(**kwargs):
        events.append("memory")
        return {"status": "completed"}

    with (
        patch.object(bot, "Device") as device,
        patch.object(bot, "visit", side_effect=[outcome]),
        patch.object(bot, "memory_hygiene", side_effect=cleanup),
    ):
        device.return_value.shell.return_value = "14"
        device.return_value.close.side_effect = lambda: events.append("close")
        device.return_value.recover_install_timeout.return_value = {}
        assert bot.execute(args, [{"id": "a"}], []) == int(isinstance(outcome, Exception))
    assert events == ["close", "memory"]
    record = bot.json.loads((tmp_path / "runs.jsonl").read_text())
    assert record["memory_cleanup"]["status"] == "completed"


def test_root_cleanup_is_bounded_and_measures_memory():
    with (
        patch.object(bot.os, "geteuid", return_value=0),
        patch.object(
            bot, "memory_snapshot", side_effect=[{"MemAvailable": 3200}, {"MemAvailable": 3900}]
        ),
        patch.object(bot, "command") as command,
    ):
        result = REAL_MEMORY_HYGIENE()
    assert command.call_count == 2
    assert command.call_args_list[0].args[3:] == ("/usr/bin/sync",)
    assert command.call_args_list[1].args[3:] == (
        "/bin/sh",
        "-c",
        "echo 1 > /proc/sys/vm/drop_caches",
    )
    assert all(item.kwargs["timeout"] == 40 for item in command.call_args_list)
    assert result["status"] == "completed"
    assert result["after_mib"]["MemAvailable"] == 3900


def test_nonroot_sudo_failure_has_visible_setup_instruction(caplog):
    with (
        patch.object(bot.os, "geteuid", return_value=1000),
        patch.object(bot, "memory_snapshot", return_value={"MemAvailable": 4000}),
        patch.object(bot, "command", side_effect=RuntimeError("permission denied")) as command,
    ):
        result = REAL_MEMORY_HYGIENE()
    assert result["status"] == "unavailable"
    assert command.call_args.args[3:] == ("/usr/bin/sudo", "-n", "/usr/bin/sync")
    assert (
        "CRITICAL: Sudo permissions missing. Please run 'sudo bash scripts/setup_vm_memory.sh' inside the VM once."
        in caplog.text
    )


def test_helper_rejects_arguments_without_dropping_host_caches():
    helper = bot.ROOT / "scripts/simufarm-drop-caches"
    result = bot.subprocess.run(
        ["/bin/sh", str(helper), "unexpected"], capture_output=True, check=False
    )
    assert result.returncode == 64


def test_memory_reporting_uses_available_not_free():
    with patch.object(
        bot.Path,
        "read_text",
        return_value="MemAvailable: 4096000 kB\nMemFree: 1024 kB\nCached: 2048000 kB\nSUnreclaim: 102400 kB\n",
    ):
        values = bot.memory_snapshot()
    assert values == {"MemAvailable": 4000, "MemFree": 1, "Cached": 2000, "SUnreclaim": 100}


def test_persistent_memory_pressure_does_not_skip_through_batch(tmp_path):
    args = SimpleNamespace(
        results=tmp_path, image="image", adb_port=0, memory_wait_retries=0, delay_min=0, delay_max=0
    )
    with (
        patch.object(bot, "Device", wraps=bot.Device) as device,
        patch.object(bot, "memory_snapshot", return_value={"MemAvailable": 2000}),
        patch.object(bot, "command") as command,
        pytest.raises(bot.SetupError, match="Memory stayed low"),
    ):
        command.return_value = ""
        bot.execute(args, [{"id": "a"}, {"id": "b"}], [])
    assert device.call_count == 1
    assert all(item.args[:2] != ("docker", "run") for item in command.call_args_list)


def test_nonroot_cleanup_uses_noninteractive_sudo_sync_and_pagecache_only():
    with (
        patch.object(bot.os, "geteuid", return_value=1000),
        patch.object(bot.Path, "is_file", return_value=True),
        patch.object(bot, "memory_snapshot", return_value={"MemAvailable": 4000}),
        patch.object(bot, "command") as command,
    ):
        result = REAL_MEMORY_HYGIENE()
    assert command.call_args_list[0].args[3:] == ("/usr/bin/sudo", "-n", "/usr/bin/sync")
    assert command.call_args_list[1].args[3:] == (
        "/usr/bin/sudo",
        "-n",
        "/bin/sh",
        "-c",
        "echo 1 > /proc/sys/vm/drop_caches",
    )
    assert result["status"] == "completed"


def test_vm_setup_rejects_nonroot_without_mutating_system():
    if bot.os.geteuid() == 0:
        pytest.skip("Root environment cannot exercise nonroot entry guard")
    script = bot.ROOT / "scripts/setup_vm_memory.sh"
    result = bot.subprocess.run(
        ["/bin/bash", str(script)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 1
    assert "Run this setup as root" in result.stderr
    assert "root console/root shell" in result.stderr


def test_declared_sudoers_rule_passes_real_visudo(tmp_path):
    visudo = shutil.which("visudo") or (
        "/usr/sbin/visudo" if Path("/usr/sbin/visudo").exists() else None
    )
    if visudo is None:
        pytest.skip("visudo is not installed on this test host")
    source = (bot.ROOT / "scripts/setup_vm_memory.sh").read_text()
    match = bot.re.search(r"^readonly RULE='([^']+)'$", source, bot.re.MULTILINE)
    assert match
    candidate = tmp_path / "simufarm-cache"
    candidate.write_text(match.group(1) + "\n")
    candidate.chmod(0o440)
    result = bot.subprocess.run(
        [visudo, "-cf", str(candidate)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


def test_vm_setup_bash_syntax():
    result = bot.subprocess.run(
        ["/bin/bash", "-n", str(bot.ROOT / "scripts/setup_vm_memory.sh")],
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0


@pytest.mark.parametrize(
    "failure",
    [
        RuntimeError("sudo denied"),
        bot.subprocess.TimeoutExpired(["sudo"], 30),
        FileNotFoundError("sudo missing"),
    ],
)
def test_pagecache_clear_failure_is_caught_and_visible(failure, caplog):
    with (
        patch.object(bot.os, "geteuid", return_value=1000),
        patch.object(bot, "memory_snapshot", return_value={"MemAvailable": 4000}),
        patch.object(bot, "command", side_effect=["", failure]) as command,
    ):
        result = REAL_MEMORY_HYGIENE()
    assert result["status"] == "unavailable"
    assert command.call_count == 2
    assert "CRITICAL: Sudo permissions missing." in caplog.text
    assert "sudo bash scripts/setup_vm_memory.sh" in caplog.text


def test_stop_timeout_kills_removes_and_returns(caplog):
    device = bot.Device("image", {"id": "test"}, 5575)
    device.created = True
    events = []

    def command(*args, **kwargs):
        events.append((args, kwargs))
        if args[:2] == ("docker", "stop"):
            raise bot.subprocess.TimeoutExpired(args, 40)
        return ""

    with patch.object(device, "shell"), patch.object(bot, "command", side_effect=command):
        device.close()
    assert [event[0][:2] for event in events] == [
        ("docker", "stop"),
        ("docker", "kill"),
        ("docker", "rm"),
        ("adb", "disconnect"),
    ]
    assert events[1][1]["timeout"] == 10
    assert events[2][0] == ("docker", "rm", "-f", "-v", device.name)
    assert events[2][1]["timeout"] == 30
    assert device.created is False and device.serial is None
    assert "Container froze during teardown; forcing kill." in caplog.text


def test_hung_stop_kill_and_disconnect_cannot_abort_after_removal():
    device = bot.Device("image", {"id": "test"}, 5575)
    device.created = True
    events = []

    def command(*args, **kwargs):
        events.append(args[:2])
        if args[:2] != ("docker", "rm"):
            raise bot.subprocess.TimeoutExpired(args, kwargs["timeout"])
        return ""

    with patch.object(device, "shell"), patch.object(bot, "command", side_effect=command):
        device.close()
    assert events == [
        ("docker", "stop"),
        ("docker", "kill"),
        ("docker", "rm"),
        ("adb", "disconnect"),
    ]
    assert device.created is False


def test_teardown_timeout_does_not_block_next_device(tmp_path):
    events = []

    def start(device):
        device.created = True
        events.append(("start", device.row["id"]))

    def command(*args, **kwargs):
        if args[:2] == ("docker", "stop"):
            raise bot.subprocess.TimeoutExpired(args, 40)
        if args[:2] == ("docker", "rm"):
            events.append(("remove", args[-1]))
        return ""

    args = SimpleNamespace(results=tmp_path, image="image", adb_port=5575, delay_min=0, delay_max=0)
    with (
        patch.object(bot.Device, "start", start),
        patch.object(bot.Device, "shell", return_value="14"),
        patch.object(bot, "command", side_effect=command),
        patch.object(bot, "visit", return_value=3),
        patch.object(bot.time, "sleep"),
    ):
        assert bot.execute(args, [{"id": "a"}, {"id": "b"}], []) == 0
    assert events[0] == ("start", "a")
    assert events[1][0] == "remove"
    assert events[2] == ("start", "b")
    assert events[3][0] == "remove"


def test_forced_removal_failure_still_prevents_overlap():
    device = bot.Device("image", {"id": "test"}, 5575)
    device.created = True

    def command(*args, **kwargs):
        if args[:2] == ("docker", "stop"):
            raise bot.subprocess.TimeoutExpired(args, 40)
        if args[:2] == ("docker", "rm"):
            raise bot.DockerCommandError("cannot remove")
        return ""

    with (
        patch.object(device, "shell"),
        patch.object(bot, "command", side_effect=command),
        pytest.raises(bot.DockerCommandError, match="cannot remove"),
    ):
        device.close()
    assert device.created is True
