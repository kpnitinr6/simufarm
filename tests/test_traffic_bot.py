import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

SPEC = importlib.util.spec_from_file_location(
    "traffic", Path(__file__).parents[1] / "scripts/run_traffic_bot.py"
)
bot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bot)


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
    with patch.object(bot, "Device") as device, patch.object(bot, "visit"):
        device.return_value.shell.return_value = "14"
        device.return_value.close.side_effect = RuntimeError("cleanup failed")
        with pytest.raises(RuntimeError, match="cleanup failed"):
            bot.execute(args, [{"id": "a"}, {"id": "b"}], [])
        assert device.call_count == 1


def test_success_screenshot_and_swipe_count(tmp_path):
    device = bot.Device("image", {"id": "test", "width_px": 1080, "height_px": 2400}, 5575)
    responses = iter(["", ":0", "Status: ok\nActivity: test/.Browser", "", "", ""])
    png = b"\x89PNG\r\n\x1a\n" + b"test"
    args = SimpleNamespace(apk=None, url="https://example.com", results=tmp_path)
    with (
        patch.object(device, "shell", side_effect=lambda *a: next(responses)),
        patch.object(bot, "command", return_value=png),
        patch.object(bot.time, "sleep"),
    ):
        count = bot.visit(device, args, None, bot.random.Random(1))
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
def test_apk_install_mode_and_boot_order(tmp_path, split):
    base = tmp_path / "base.apk"
    base.touch()
    extra = tmp_path / "split_config.arm64_v8a.apk"
    if split:
        extra.touch()
    events = []
    device = bot.Device("image", {"id": "test"}, 5575)

    def command(*args, **kwargs):
        events.append(args)
        if args[0] == "aapt":
            return "package: name='com.android.chrome' versionCode='1'"
        return "Success"

    with (
        patch.object(bot, "command", side_effect=command),
        patch.object(device, "shell", return_value="1") as shell,
        patch.object(bot.time, "sleep", side_effect=lambda t: events.append(("sleep", t))),
    ):
        assert bot.install_apk(device, tmp_path if split else base) == "com.android.chrome"
    assert events[0] == ("adb", "-s", device.serial, "wait-for-device")
    assert events[1] == ("sleep", 2)
    shell.assert_called_once_with("getprop", "sys.boot_completed")
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
    with patch.object(bot, "command") as command, patch.object(device, "shell", return_value="0"):
        with pytest.raises(bot.SetupError, match="boot is incomplete"):
            bot.install_apk(device, apk)
        command.assert_called_once_with("adb", "-s", device.serial, "wait-for-device", timeout=30)
