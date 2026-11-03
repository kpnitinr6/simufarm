#!/usr/bin/env python3
"""Sequential, screen-geometry traffic scenarios on stock Redroid (no identity promotion)."""

import argparse
import csv
import fcntl
import hashlib
import itertools
import json
import logging
import random
import re
import shlex
import signal
import socket
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LOG = logging.getLogger("traffic")
VERSION = "docker-run-diagnostics-v2"


class SetupError(RuntimeError):
    """An invariant setup failure that should stop the batch after cleanup."""


class DockerCommandError(SetupError):
    """Docker setup failures abort the batch with actionable daemon diagnostics."""


def redact_diagnostic(value):
    value = re.sub(r"(https?://)[^\s/@]+@", r"\1[redacted]@", value)
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", value).strip()[:8192]


def command(*args, timeout=60, binary=False, check=True, missing_ok=False):
    result = subprocess.run(
        args, check=False, capture_output=True, text=not binary, timeout=timeout
    )
    if check and result.returncode:
        if args[0] == "docker":
            error = result.stderr.decode(errors="replace") if binary else result.stderr
            if missing_ok and args[1] == "rm" and "no such container" in error.lower():
                return b"" if binary else ""
            output = result.stdout.decode(errors="replace") if binary else result.stdout
            error = redact_diagnostic(error or output or "(empty stdout/stderr)")
            # Emit immediately, before callers/cleanup can replace the original exception.
            print(
                f"Docker {args[1]} stderr (exit {result.returncode}):\n{error}",
                file=sys.stderr,
                flush=True,
            )
            raise DockerCommandError(f"docker {args[1]} failed (exit {result.returncode}): {error}")
        raise RuntimeError(f"{args[0]} command failed (exit {result.returncode})")
    return result.stdout if binary else result.stdout.strip()


def proxy_address(raw):
    """Android's global HTTP proxy supports a host/port, not URL credentials."""
    p = urlsplit(raw if "://" in raw else "http://" + raw)
    if p.username is not None or p.password is not None:
        raise ValueError(
            "Authenticated proxies need a separate local relay; credentials unsupported"
        )
    if p.scheme != "http" or not p.hostname or not p.port or p.path not in ("", "/"):
        raise ValueError("Proxy must be http://host:port (without credentials or a path)")
    if p.query or p.fragment or not re.fullmatch(r"[A-Za-z0-9.:-]+", p.hostname):
        raise ValueError("Invalid proxy host")
    host = f"[{p.hostname}]" if ":" in p.hostname else p.hostname
    return f"{host}:{p.port}"


def load_proxies(path):
    """Read CSV's proxy column or a plain list, returning canonical HTTP URLs."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        if path.suffix.lower() == ".csv":
            reader = csv.DictReader(stream)
            if not reader.fieldnames or "proxy" not in reader.fieldnames:
                raise ValueError("Proxy CSV must have a proxy column")
            values = [row.get("proxy") or "" for row in reader]
        else:
            values = list(stream)
    proxies = [
        "http://" + proxy_address(value.strip())
        for value in values
        if value.strip() and not value.lstrip().startswith("#")
    ]
    if not proxies:
        raise ValueError("Proxy file has no proxies")
    return proxies


def load_profiles(path):
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    seen = set()
    for row in rows:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,120}", row["id"]) or row["id"] in seen:
            raise ValueError("Invalid or duplicate CSV profile ID")
        seen.add(row["id"])
        for key in ("width_px", "height_px", "dpi"):
            value = float(row[key])
            if not 50 <= value <= 10000:
                raise ValueError(f"Invalid {key} for {row['id']}")
            row[key] = round(value)
    return rows


class Device:
    def __init__(self, image, row, port):
        self.name = "simufarm-traffic-" + uuid.uuid4().hex
        self.serial = f"127.0.0.1:{port}" if port else None
        self.image, self.row, self.port = image, row, port
        self.created = False
        self.binderfs = None

    def shell(self, *args, timeout=30):
        # adb shell joins its arguments remotely: quote once for Android's shell too.
        return command(
            "adb", "-s", self.serial, "shell", shlex.join(map(str, args)), timeout=timeout
        )

    def start(self):
        r = self.row
        # No automatic pulls, privileged daemon changes, host networking or identity injection.
        if command("docker", "ps", "-q"):
            raise RuntimeError("Stop existing containers before this sequential traffic run")
        available = (
            int(
                next(
                    line.split()[1]
                    for line in Path("/proc/meminfo").read_text().splitlines()
                    if line.startswith("MemAvailable:")
                )
            )
            * 1024
        )
        if available < 2 * 1024**3 + 1200 * 1024**2:
            raise RuntimeError("Insufficient memory to retain the 2 GiB host reserve")
        if self.port:
            try:
                with socket.socket() as probe:
                    probe.bind(("127.0.0.1", self.port))
            except OSError as exc:
                raise SetupError(
                    f"ADB port {self.port} is unavailable; omit --adb-port for automatic allocation"
                ) from exc
        # Exact per-run UUID name only; ignore absence, never remove other containers.
        command("docker", "rm", "-f", "-v", self.name, missing_ok=True)
        self.created = True
        docker_args = [
            "docker",
            "run",
            "-d",
            "--pull=never",
            "--name",
            self.name,
            "--label",
            "simufarm.traffic=true",
            "--privileged",
            "--memory",
            "1200m",
            "--memory-swap",
            "1200m",
            "-v",
            "/data",
            "-p",
            f"127.0.0.1:{self.port or ''}:5555",
            *(
                ["--mount", f"type=bind,src={self.binderfs},dst=/dev/binderfs"]
                if self.binderfs
                else []
            ),
            self.image,
            f"androidboot.redroid_width={r['width_px']}",
            f"androidboot.redroid_height={r['height_px']}",
            f"androidboot.redroid_dpi={r['dpi']}",
            "androidboot.redroid_gpu_mode=guest",
        ]
        LOG.info("  Docker command: %s", redact_diagnostic(shlex.join(docker_args)))
        command(*docker_args, timeout=120)
        deadline = time.monotonic() + 180
        time.sleep(15)
        if not self.port:
            mapping = command("docker", "port", self.name, "5555/tcp")
            match = re.fullmatch(r"127\.0\.0\.1:(\d+)", mapping)
            if not match or not 1 <= int(match.group(1)) <= 65535:
                raise SetupError("Docker did not provide a loopback ADB port mapping")
            self.port = int(match.group(1))
            self.serial = mapping
        LOG.info("  ADB endpoint %s", self.serial)
        while time.monotonic() < deadline:
            try:
                command("adb", "connect", self.serial, timeout=5)
                command("adb", "-s", self.serial, "wait-for-device", timeout=5)
                if self.shell("getprop", "sys.boot_completed", timeout=5) == "1":
                    return
            except (RuntimeError, subprocess.TimeoutExpired):
                pass
            time.sleep(2)
        raise TimeoutError("Android boot exceeded 180 seconds")

    def close(self):
        if self.created:
            try:
                if self.serial:
                    self.shell("settings", "put", "global", "http_proxy", ":0", timeout=10)
            except (RuntimeError, OSError, subprocess.TimeoutExpired):
                LOG.warning("  proxy reset unavailable; proceeding with container removal")
            # Only our unique container; volumes removed too. Never kill a shared ADB server.
            try:
                command("docker", "stop", "--time", "30", self.name, timeout=40, check=False)
            finally:
                command("docker", "rm", "-f", "-v", self.name, missing_ok=True)
                self.created = False
        if self.serial:
            command("adb", "disconnect", self.serial, check=False)


def apk_files(path):
    """Return a single APK or a deterministic, base-first split install set."""
    if path.is_dir():
        base = path / "base.apk"
        files = sorted(p for p in path.glob("*.apk") if p.is_file())
        if not files or base not in files:
            raise ValueError("Split APK folder must contain base.apk and its matching APK splits")
        return [base, *(p for p in files if p != base)]
    if not path.is_file() or path.suffix.lower() != ".apk":
        raise ValueError("--apk must be an APK file or a folder containing base.apk")
    return [path]


def install_apk(device, path):
    files = apk_files(path)
    command("adb", "-s", device.serial, "wait-for-device", timeout=30)
    if device.shell("getprop", "sys.boot_completed") != "1":
        raise SetupError("Android boot is incomplete; refusing APK installation")
    time.sleep(2)
    # aapt reads the package from the base, never an arbitrary configuration split.
    badging = command("aapt", "dump", "badging", str(files[0]))
    match = re.search(r"^package: name='([A-Za-z0-9_.]+)'", badging, re.MULTILINE)
    if not match:
        raise SetupError("Unable to read APK package with aapt")
    mode = "install-multiple" if path.is_dir() else "install"
    LOG.info("  installing %d APK file(s)", len(files))
    installed = command(
        "adb", "-s", device.serial, mode, "-r", *(str(p) for p in files), timeout=180
    )
    if "Success" not in installed:
        raise SetupError("APK installation failed")
    return match.group(1)


def visit(device, args, proxy, rng):
    proxy = proxy_address(proxy) if proxy else None
    device.shell("settings", "put", "global", "http_proxy", proxy or ":0")
    if device.shell("settings", "get", "global", "http_proxy") != (proxy or ":0"):
        raise RuntimeError("Android proxy setting did not persist")
    if args.apk and install_apk(device, args.apk) != "com.android.chrome":
        raise SetupError("This browsing pipeline requires the com.android.chrome APK")
    result = device.shell(
        "am",
        "start",
        "-W",
        "-n",
        "com.android.chrome/com.google.android.apps.chrome.Main",
        "-d",
        args.url,
    )
    if "Error:" in result or "Exception" in result or "Activity:" not in result:
        raise SetupError("Chrome launch failed; provide a compatible Chrome APK or split folder")
    time.sleep(5)
    width, height = device.row["width_px"], device.row["height_px"]
    swipes = rng.randint(3, 4)
    for _ in range(swipes):
        x = rng.randint(int(width * 0.35), int(width * 0.65))
        device.shell(
            "input",
            "swipe",
            x,
            int(height * rng.uniform(0.7, 0.85)),
            x,
            int(height * rng.uniform(0.2, 0.35)),
            rng.randint(300, 800),
        )
        time.sleep(rng.uniform(0.5, 1.5))
    time.sleep(10)
    image = command("adb", "-s", device.serial, "exec-out", "screencap", "-p", binary=True)
    if not image.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("ADB did not return a PNG screenshot")
    target = args.results / (device.row["id"] + ".png")
    target.write_bytes(image)
    return swipes


def execute(args, rows, proxies):
    rng = random.Random()
    failures = 0
    proxy_cycle = itertools.cycle(proxies or [None])
    args.results.mkdir(parents=True, exist_ok=True)
    for index, row in enumerate(rows, 1):
        device = Device(args.image, row, args.adb_port)
        device.binderfs = getattr(args, "binderfs", None)
        proxy = next(proxy_cycle)
        started = time.monotonic()
        record = {
            "profile_id": row["id"],
            "scenario": "static_screen_geometry",
            "runtime_eligible": False,
            "identity_injected": False,
            "image": args.image,
            "status": "failed",
        }
        LOG.info("[%d/%d] %s — booting (stock Android, geometry only)", index, len(rows), row["id"])
        try:
            (args.results / (row["id"] + ".png")).unlink(missing_ok=True)
            device.start()
            record["actual_android_release"] = device.shell("getprop", "ro.build.version.release")
            LOG.info("  visiting, scrolling and capturing")
            record["swipes"] = visit(device, args, proxy, rng)
            record["status"] = "passed"
        except SetupError as exc:
            record["error"] = str(exc)
            LOG.error("  %s", exc)
            raise
        except (RuntimeError, subprocess.TimeoutExpired, TimeoutError) as exc:
            failures += 1
            record["error"] = (
                str(exc) if not isinstance(exc, subprocess.TimeoutExpired) else "Command timeout"
            )
            LOG.error("  %s", record["error"])
        finally:
            # Cleanup failure aborts the entire batch: never overlap devices.
            device.close()
            record["elapsed_seconds"] = round(time.monotonic() - started, 3)
            with (args.results / "runs.jsonl").open("a") as stream:
                stream.write(json.dumps(record) + "\n")
        LOG.info("  %s in %.1fs; container removed", record["status"], record["elapsed_seconds"])
        if index < len(rows):
            delay = rng.uniform(args.delay_min, args.delay_max)
            LOG.info("  waiting %.1fs before next scenario", delay)
            time.sleep(delay)
    LOG.info("Finished: %d passed, %d failed", len(rows) - failures, failures)
    return int(bool(failures))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument(
        "--apk", type=Path, help="APK file or folder containing base.apk and splits"
    )
    parser.add_argument("--proxy-file", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--delay-min", type=float, default=60)
    parser.add_argument("--delay-max", type=float, default=120)
    parser.add_argument("--csv", type=Path, default=ROOT / "data/devices.csv")
    parser.add_argument("--results", type=Path, default=ROOT / "results/traffic")
    parser.add_argument(
        "--adb-port", type=int, default=0, help="Host ADB port (default: Docker-assigned)"
    )
    tool = json.loads((ROOT / "infra/redroid-identity/toolchain.json").read_text())
    parser.add_argument(
        "--image",
        default=tool["requested_tag"],
        help="Cached image tag or digest (no automatic pull)",
    )
    parser.add_argument(
        "--binderfs",
        type=Path,
        help="Optional existing host binderfs path to bind at /dev/binderfs",
    )
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument(
        "--dry-run", action="store_true", help="Validate inputs only; no Docker/ADB/network"
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    LOG.info(
        "Traffic bot %s | script=%s | sha256=%s | image=%s",
        VERSION,
        Path(__file__).resolve(),
        hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12],
        redact_diagnostic(args.image),
    )
    try:
        if args.binderfs:
            args.binderfs = args.binderfs.resolve(strict=True)
            if not args.binderfs.is_dir() or any(c in str(args.binderfs) for c in ",\n\r"):
                raise ValueError("--binderfs must be an existing directory without commas/newlines")
        url = urlsplit(args.url)
        if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password:
            raise ValueError("URL must be HTTP(S), without embedded credentials")
        if not 0 <= args.delay_min <= args.delay_max or args.delay_max > 86400:
            raise ValueError("Require 0 <= delay-min <= delay-max <= 86400")
        if args.limit is not None and args.limit < 1:
            raise ValueError("limit must be positive")
        if args.adb_port != 0 and not 1024 <= args.adb_port <= 65535:
            raise ValueError("Invalid ADB port")
        if args.apk:
            args.apk = args.apk.resolve(strict=True)
            apk_files(args.apk)
        proxies = []
        if args.proxy_file:
            proxies = load_proxies(args.proxy_file)
        rows = load_profiles(args.csv)
        if args.limit:
            rows = rows[: args.limit]
        if not rows:
            raise ValueError("CSV has no scenarios")
        LOG.info(
            "%d static geometry scenarios; %d proxies; strictly sequential", len(rows), len(proxies)
        )
        if args.dry_run:
            LOG.info("Validation passed. No resources started or URLs visited.")
            return 0
        # Per-VM rather than per-checkout lock prevents two invocations racing each other.
        with open(Path(tempfile.gettempdir()) / "simufarm-traffic.lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if command("docker", "ps", "-q", "--filter", "label=simufarm.traffic=true"):
                raise RuntimeError("An existing traffic container needs cleanup before continuing")
            if command("docker", "ps", "-q"):
                raise RuntimeError("Stop existing containers before this sequential traffic run")
            command("docker", "image", "inspect", args.image)
            return execute(args, rows, proxies)
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        LOG.error("Stopped: %s", type(exc).__name__ if isinstance(exc, OSError) else exc)
        return 1
    except KeyboardInterrupt:
        LOG.info("Interrupted; cleanup attempted (inspect Docker if cleanup reported an error)")
        return 130


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    raise SystemExit(main())
