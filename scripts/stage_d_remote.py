#!/usr/bin/env python3
"""Run on the authorized local Linux server; collect actuals without identity spoofing."""

import argparse
import hashlib
import json
import platform
import re
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

IMAGE = "redroid/redroid@sha256:c815ac1b1d5bd0a099b74c3e3e0eeea3b32bed8d7ab1f788c20fb74e35891716"


def run(*args, check=True):
    return subprocess.run(
        args, text=True, capture_output=True, check=check, timeout=180
    ).stdout.strip()


def identity_checks(containers):
    if len(containers) != 2:
        return {key: False for key in ("android_id", "imei", "serial", "adb_serial")}
    checks = {}
    for field in ("android_id", "imei", "serial", "adb_serial"):
        values = [item.get(field) for item in containers]
        checks[field] = (
            all(v and v not in ("null", "unknown", "0") for v in values) and len(set(values)) == 2
        )
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--apk", type=Path, required=True)
    parser.add_argument("--apk-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--image", default=IMAGE, help="Verified immutable Redroid image for host architecture"
    )
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        parser.error("Explicit --execute is required on the authorized remote host")
    architectures = {"aarch64": "arm64", "arm64": "arm64", "x86_64": "amd64", "amd64": "amd64"}
    arch = architectures.get(platform.machine())
    if platform.system() != "Linux" or arch is None:
        raise SystemExit("Requires authorized Linux ARM64 or x86_64 server")
    if not re.fullmatch(r"redroid/redroid@sha256:[0-9a-f]{64}", args.image):
        raise SystemExit("A verified immutable Redroid image digest is required")
    if arch == "amd64" and args.image == IMAGE:
        raise SystemExit("ARM image cannot run on x86_64; supply verified amd64 digest")
    profile = json.loads(args.profile.read_text())
    if profile["id"] != "vivo-x100" or profile["brand"] != "vivo":
        raise SystemExit("Stage D authorizes the existing vivo-x100 profile only")
    if hashlib.sha256(args.apk.read_bytes()).hexdigest() != args.apk_sha256:
        raise SystemExit("APK SHA256 mismatch")
    args.output.mkdir(parents=True, exist_ok=False)
    report = {
        "observed_at": datetime.now(UTC).isoformat(),
        "image": args.image,
        "host_architecture": arch,
        "deployment_target": "local-linux-meshnet",
        "profile_id": profile["id"],
        "profile_build_applied": False,
        "profile_build_ignored_for_diagnostic": profile.get("build") is not None,
        "profile_runtime_eligible": profile.get("runtime_eligible", False),
        "diagnostic_only": True,
        "kvm_present": Path("/dev/kvm").exists(),
        "kernel": platform.release(),
        "apk_sha256": args.apk_sha256,
        "containers": [],
        "passed": False,
    }
    report_path = args.output / "observations.json"

    def save():
        report_path.write_text(json.dumps(report, indent=2) + "\n")

    save()
    try:
        # Redroid does not require KVM; local hardware may legitimately expose it.
        # Deliberately fail rather than install unreviewed kernel packages or reboot.
        run("sudo", "-n", "modprobe", "binder_linux", "devices=binder,hwbinder,vndbinder")
        run("sudo", "-n", "modprobe", "ashmem_linux")
        report["lsmod"] = run("lsmod")
        run("docker", "pull", "--platform", f"linux/{arch}", args.image)
        report["image_inspect"] = json.loads(run("docker", "image", "inspect", args.image))[0]
        if report["image_inspect"]["Architecture"] != arch:
            raise RuntimeError("Pulled image architecture differs from host")
        for index, port in enumerate((5555, 5556), 1):
            name = f"simufarm-stage-d-{args.output.name}-{index}"
            volume = name + "-data"
            # Neither docker volume create nor docker run may reuse earlier state.
            if (
                subprocess.run(
                    ["docker", "volume", "inspect", volume],
                    capture_output=True,
                    check=False,
                    timeout=30,
                ).returncode
                == 0
            ):
                raise RuntimeError("Existing volume: refuse state reuse")
            run("docker", "volume", "create", volume)
            serial = f"127.0.0.1:{port}"
            started = time.monotonic()
            run(
                "docker",
                "run",
                "-d",
                "--name",
                name,
                "--privileged",
                "--platform",
                f"linux/{arch}",
                "-v",
                volume + ":/data",
                "-p",
                f"127.0.0.1:{port}:5555",
                args.image,
                f"androidboot.redroid_width={profile['screen']['width_px']}",
                f"androidboot.redroid_height={profile['screen']['height_px']}",
                f"androidboot.redroid_dpi={profile['screen']['dpi']}",
                "androidboot.redroid_gpu_mode=guest",
            )
            item = {"name": name, "volume": volume, "adb_serial": serial}
            report["containers"].append(item)
            save()
            while time.monotonic() - started < 300:
                run("adb", "connect", serial, check=False)
                if (
                    run("adb", "-s", serial, "shell", "getprop", "sys.boot_completed", check=False)
                    == "1"
                ):
                    break
                time.sleep(2)
            else:
                raise RuntimeError(f"{name}: boot timeout")
            item["boot_seconds"] = round(time.monotonic() - started, 3)
            item["adb_state"] = run("adb", "-s", serial, "get-state")
            item["apk_install_output"] = run("adb", "-s", serial, "install", "-r", str(args.apk))
            if item["adb_state"] != "device" or "Success" not in item["apk_install_output"]:
                raise RuntimeError("ADB or APK install verification failed")
            item["android_id"] = run(
                "adb", "-s", serial, "shell", "settings", "get", "secure", "android_id"
            )
            item["serial"] = run("adb", "-s", serial, "shell", "getprop", "ro.serialno")
            item["build_properties"] = run("adb", "-s", serial, "shell", "getprop")
            raw = run(
                "adb",
                "-s",
                serial,
                "shell",
                "service",
                "call",
                "iphonesubinfo",
                "1",
                "s16",
                "com.android.shell",
                check=False,
            )
            item["imei_raw"] = raw
            # Parse only the string column of Android Parcel output; never invent missing IMEI.
            text = "".join(re.findall(r"'([^']*)'", raw)).replace(".", "").replace(" ", "")
            item["imei"] = text if re.fullmatch(r"\d{15}", text) else None
            save()
        # Sample both containers together after the second has booted.
        for item in report["containers"]:
            item["docker_memory_usage"] = run(
                "docker", "stats", "--no-stream", "--format", "{{.MemUsage}}", item["name"]
            )
            pid = run("docker", "inspect", "--format", "{{.State.Pid}}", item["name"])
            cgroups = Path(f"/proc/{pid}/cgroup").read_text().splitlines()
            unified = next(
                (line.split(":", 2)[2] for line in cgroups if line.startswith("0::")), None
            )
            item["cgroup_memory_current_bytes"] = None
            if unified:
                item["cgroup_memory_current_bytes"] = int(
                    (Path("/sys/fs/cgroup") / unified.lstrip("/") / "memory.current").read_text()
                )
        checks = identity_checks(report["containers"])
        report["identity_uniqueness"] = checks
        report["passed"] = all(checks.values())
        if not report["passed"]:
            raise RuntimeError(
                "Missing or shared identity values: Stage D FAIL; no spoofed replacements"
            )
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        save()
        print(f"Observed evidence: {report_path}; passed={report['passed']}")
        print(
            "Containers/volumes retained for inspection; remove explicitly after collecting evidence."
        )


if __name__ == "__main__":
    main()
