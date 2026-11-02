#!/usr/bin/env python3
"""Warm local UTM startup and bounded two-container identity rehearsal. Plan-only by default."""

import argparse
import hashlib
import json
import subprocess
import sys
import time
import uuid
from pathlib import Path

from simufarm_schema import DeviceProfile
from stage_d_local import ROOT, ssh_args


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vm-id", type=uuid.UUID, required=True)
    p.add_argument("--identity", type=Path, required=True)
    p.add_argument("--known-hosts", type=Path, required=True)
    p.add_argument("--magisk-apk", type=Path, required=True)
    p.add_argument("--output", type=Path, default=ROOT / "data/runtime/local/quickstart")
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    vm = str(a.vm_id).upper()
    print(
        json.dumps(
            {
                "execute": a.execute,
                "vm_id": vm,
                "host": "127.0.0.1",
                "ssh_port": 2222,
                "containers": 2,
                "container_ceiling": 5,
                "paid_resources": False,
            }
        ),
        flush=True,
    )
    if not a.execute:
        return
    profile = DeviceProfile.model_validate_json(
        (ROOT / "profiles/runtime/vivo-x100.json").read_text()
    )
    if not profile.runtime_eligible or profile.verified_by != "human":
        p.error("Reviewed runtime profile required before local boot")
    tool = json.loads((ROOT / "infra/redroid-identity/toolchain.json").read_text())
    if (
        not a.identity.is_file()
        or not a.known_hosts.is_file()
        or not a.magisk_apk.is_file()
        or hashlib.sha256(a.magisk_apk.read_bytes()).hexdigest() != tool["apk_sha256"]
    ):
        p.error("Local SSH key, verified known_hosts and pinned official Magisk APK required")
    started = time.monotonic()
    state = subprocess.check_output(["utmctl", "status", vm], text=True, timeout=30).strip()
    if state == "stopped":
        subprocess.run(["utmctl", "start", vm], check=True, timeout=60)
    elif state != "started":
        raise SystemExit("VM must be stopped or started; inspect its state in UTM")
    ssh = ssh_args("127.0.0.1", "simufarm", a.identity, "utm", 2222, a.known_hosts)
    end = time.monotonic() + 120
    while time.monotonic() < end:
        result = subprocess.run(ssh + ["true"], check=False, capture_output=True, timeout=25)
        if result.returncode == 0:
            break
        time.sleep(2)
    else:
        raise SystemExit("Strict localhost SSH did not become ready within120seconds")
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/stage_e_utm.py"),
            "--vm-id",
            vm,
            "--identity",
            str(a.identity),
            "--known-hosts",
            str(a.known_hosts),
            "--magisk-apk",
            str(a.magisk_apk),
            "--output",
            str(a.output),
            "--execute-test",
        ],
        check=True,
        timeout=1500,
    )
    timing = {
        "success": True,
        "vm_initial_state": state,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "cold_install_excluded": True,
    }
    (a.output / "quickstart-timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)


if __name__ == "__main__":
    main()
