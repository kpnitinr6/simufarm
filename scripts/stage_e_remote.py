#!/usr/bin/env python3
"""Isolated user-authorized China X100 property test; never promotes runtime profiles."""

# ruff: noqa: UP017
# Guest Ubuntu 22.04 uses Python 3.10; timezone.utc is intentional.
import argparse
import hashlib
import json
import re
import secrets
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

CEILING = 5
RESERVE = 2 * 1024**3
BUDGET = 1200 * 1024**2
KEYS = ("ro.product.brand", "ro.product.model", "ro.product.device", "ro.build.fingerprint")


def run(*cmd, check=True, timeout=120):
    p = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=timeout)
    if check and p.returncode:
        raise RuntimeError(f"{cmd[0]} failed ({p.returncode}): {p.stdout}\n{p.stderr}")
    return p.stdout.strip()


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def imei():
    # Reserved-looking synthetic test namespace, never a claimed allocated handset TAC.
    body = "00000000" + "".join(str(secrets.randbelow(10)) for _ in range(6))
    total = sum(
        (int(x) * 2 // 10 + int(x) * 2 % 10) if i % 2 else int(x) for i, x in enumerate(body)
    )
    return body + str((-total) % 10)


def properties(profile):
    b = profile.get("build") or {}
    if profile.get("id") != "vivo-x100-china" or profile.get("runtime_eligible") is not False:
        raise ValueError("Only the explicit experimental China profile is authorized here")
    if any(not isinstance(b.get(k), str) or not b[k] for k in KEYS):
        raise ValueError("Complete sourced build block required")
    if not b.get("sources") or not b.get("source_type"):
        raise ValueError("Build provenance required")
    if (b["ro.product.brand"], b["ro.product.model"], b["ro.product.device"]) != (
        "vivo",
        "V2309A",
        "PD2309",
    ) or not b["ro.build.fingerprint"].startswith("vivo/PD2309/PD2309:"):
        raise ValueError("China identity must not mix India firmware/model fields")
    if any(not re.fullmatch(r"[A-Za-z0-9_./:+-]+", b[k]) for k in KEYS):
        raise ValueError("Unsafe property value")
    release = profile.get("os_version")
    if release != "14" or ":14/" not in b["ro.build.fingerprint"]:
        raise ValueError("Firmware fingerprint and actual Android14 runtime must agree")
    return {**{k: b[k] for k in KEYS}, "ro.build.version.release": release}


def capacity(active, available, additional=1):
    if active + additional > CEILING:
        raise RuntimeError("Five-container planning ceiling would be exceeded")
    if available - BUDGET * additional < RESERVE:
        raise RuntimeError("Two GiB Ubuntu host reserve would be breached")


def available_memory():
    return (
        int(
            next(
                x.split()[1]
                for x in Path("/proc/meminfo").read_text().splitlines()
                if x.startswith("MemAvailable:")
            )
        )
        * 1024
    )


def observe(name, serial, props):
    values = {k: run("adb", "-s", serial, "shell", "getprop", k) for k in props}
    return {
        "properties": values,
        "all_match": values == props,
        "android_id": run("adb", "-s", serial, "shell", "settings", "get", "secure", "android_id"),
        "adb_serial": serial,
        "identity_hook_ready": run(
            "adb", "-s", serial, "shell", "getprop", "sys.simufarm.identity.ready"
        ),
        "actual_sdk": run("adb", "-s", serial, "shell", "getprop", "ro.build.version.sdk"),
        "actual_android_release": run(
            "adb", "-s", serial, "shell", "getprop", "ro.build.version.release"
        ),
        "telephony_imei_raw": run(
            "adb", "-s", serial, "shell", "service", "call", "iphonesubinfo", "1", check=False
        ),
        "docker_memory": run("docker", "stats", "--no-stream", "--format", "{{.MemUsage}}", name),
    }


def boot(name, serial, command):
    start = time.monotonic()
    run(*command, timeout=180)
    deadline = start + 180
    while time.monotonic() < deadline:
        try:
            remaining = max(1, int(deadline - time.monotonic()))
            run("adb", "connect", serial, check=False, timeout=min(10, remaining))
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                break
            completed = run(
                "adb",
                "-s",
                serial,
                "shell",
                "getprop",
                "sys.boot_completed",
                check=False,
                timeout=min(20, remaining),
            )
            if completed == "1":
                return round(time.monotonic() - start, 3)
        except subprocess.TimeoutExpired:
            # ADB may accept a connection before its early-boot shell is responsive.
            # Keep the original global deadline; never turn readiness retries into a new boot.
            pass
        time.sleep(min(2, max(0, deadline - time.monotonic())))
    raise TimeoutError(f"{name} did not boot within 180 seconds")


def execute(root):
    tool = json.loads((root / "context/toolchain.json").read_text())
    profile = json.loads((root / "profile.json").read_text())
    base = properties(profile)
    if checksum(root / "context/magisk") != tool["binary_sha256"]:
        raise ValueError("Magisk binary digest mismatch")
    if tool["base_image"] not in (root / "context/Dockerfile").read_text():
        raise ValueError("Pinned base image mismatch")
    inspection = "simufarm-stage-e-base-" + root.name[:12]
    run("docker", "create", "--name", inspection, tool["base_image"])
    try:
        run("docker", "cp", inspection + ":/system/build.prop", str(root / "base-build.prop"))
    finally:
        run("docker", "rm", inspection)
    (root / "base-build.prop").chmod(0o644)
    raw = (root / "base-build.prop").read_text()
    if "ro.build.version.release=14\n" not in raw or "ro.build.version.sdk=34\n" not in raw:
        raise ValueError("Pinned base must really be Android14/SDK34 before release injection")
    active = run("docker", "ps", "-q").splitlines()
    capacity(len(active), available_memory(), 2)
    # Legacy Docker builder preserves COPY source modes; no Android shell RUN required.
    for filename in ("magisk", "simufarm-identity.sh"):
        (root / "context" / filename).chmod(0o755)
    (root / "context/init.rc").chmod(0o644)
    tag = "simufarm-stage-e:" + root.name
    run("docker", "build", "--network=none", "-t", tag, str(root / "context"), timeout=300)
    image_id = run("docker", "image", "inspect", "--format", "{{.Id}}", tag)
    report = {
        "stage": "E",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile["id"],
        "test_only": True,
        "human_promoted": False,
        "synthetic_identifiers": True,
        "image_id": image_id,
        "toolchain": tool,
        "ceiling": CEILING,
        "host_reserve_bytes": RESERVE,
        "oracle_api_calls": 0,
        "paid_resources_created": 0,
        "instances": [],
    }
    evidence = root / "observations.json"
    used_serials, used_imeis = set(), set()
    try:
        for i in range(2):
            capacity(len(run("docker", "ps", "-q").splitlines()), available_memory())
            name = f"simufarm-stage-e-{root.name[:12]}-{i + 1}"
            serial = f"127.0.0.1:{5561 + i}"
            sn, im = "SFTEST" + secrets.token_hex(6).upper(), imei()
            while sn in used_serials or im in used_imeis:
                sn, im = "SFTEST" + secrets.token_hex(6).upper(), imei()
            used_serials.add(sn)
            used_imeis.add(im)
            props = dict(base, **{"ro.serialno": sn, "persist.radio.imei": im})
            propfile = root / f"instance-{i + 1}.prop"
            propfile.write_text("".join(f"{k}={v}\n" for k, v in props.items()))
            propfile.chmod(0o444)
            cmd = [
                "docker",
                "run",
                "-d",
                "--privileged",
                "--platform",
                "linux/arm64",
                "--name",
                name,
                "--memory",
                "1200m",
                "--memory-swap",
                "1200m",
                "-v",
                name + "-data:/data",
                "--mount",
                f"type=bind,src={propfile},dst=/simufarm/identity.prop,readonly",
                "-p",
                f"127.0.0.1:{5561 + i}:5555",
                image_id,
                "androidboot.redroid_width=1260",
                "androidboot.redroid_height=2800",
                "androidboot.redroid_dpi=452",
                "androidboot.redroid_gpu_mode=guest",
            ]
            item = {"container": name, "requested": props}
            report["instances"].append(item)
            item["boot_seconds"] = boot(name, serial, cmd)
            item["first_boot"] = observe(name, serial, props)
            evidence.write_text(json.dumps(report, indent=2) + "\n")
            if (
                not item["first_boot"]["all_match"]
                or item["first_boot"]["identity_hook_ready"] != "1"
            ):
                raise RuntimeError("Boot identity verification failed")
        for i, item in enumerate(report["instances"]):
            serial = f"127.0.0.1:{5561 + i}"
            run("docker", "stop", item["container"])
            run("adb", "disconnect", serial, check=False)
            item["restart_seconds"] = boot(
                item["container"], serial, ["docker", "start", item["container"]]
            )
            item["after_restart"] = observe(item["container"], serial, item["requested"])
            if not item["after_restart"]["all_match"]:
                raise RuntimeError("Identity lost on restart")
        report["distinct"] = {
            k: len({x["after_restart"]["properties"][k] for x in report["instances"]}) == 2
            for k in ("ro.serialno", "persist.radio.imei")
        }
        report["android_id_distinct"] = (
            len({x["after_restart"]["android_id"] for x in report["instances"]}) == 2
        )
        report["property_gate_passed"] = all(report["distinct"].values())
        report["host_mem_available_bytes_after"] = available_memory()
        if report["host_mem_available_bytes_after"] < RESERVE:
            raise RuntimeError("Host reserve below two GiB after boot")
    except Exception as exc:
        report["error"] = str(exc)
        report["property_gate_passed"] = False
        raise
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        evidence.write_text(json.dumps(report, indent=2) + "\n")
        for item in report["instances"]:
            log = run("docker", "logs", "--tail", "200", item["container"], check=False)
            (root / (item["container"] + ".log")).write_text(log)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workspace", required=True, type=Path)
    p.add_argument("--execute-test", action="store_true")
    args = p.parse_args()
    if args.execute_test:
        execute(args.workspace.resolve())
    else:
        print("Plan only: two isolated experimental property tests, no runtime promotion.")
