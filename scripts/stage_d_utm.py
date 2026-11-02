#!/usr/bin/env python3
"""Run specific Stage D diagnostics through the existing UTM guest agent, not sudoers."""

import argparse
import hashlib
import json
import shlex
import subprocess
import textwrap
import time
import uuid
from pathlib import Path

from stage_d_local import PROBE, ROOT, endpoint, require_host, ssh_args


def qga(vm, program):
    subprocess.run(
        ["utmctl", "exec", vm, "--cmd", "/usr/bin/python3", program], check=True, timeout=60
    )


def wait_json(ssh, path, timeout):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        p = subprocess.run(
            ssh + [shlex.join(["cat", path])],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if p.returncode == 0:
            return json.loads(p.stdout)
        time.sleep(2)
    raise TimeoutError("Guest diagnostic completion marker not observed; no success claimed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vm-id", required=True, type=uuid.UUID)
    p.add_argument("--user", default="simufarm")
    p.add_argument("--port", type=int, default=2222)
    p.add_argument("--identity", required=True, type=Path)
    p.add_argument("--known-hosts", required=True, type=Path)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    p.add_argument("--apk", type=Path)
    p.add_argument("--apk-sha256")
    p.add_argument("--image")
    p.add_argument("--output", type=Path, default=ROOT / "data/runtime/local")
    a = p.parse_args()
    target = endpoint("127.0.0.1", a.user, "utm")
    vm = str(a.vm_id).upper()
    ssh = ssh_args("127.0.0.1", a.user, a.identity, "utm", a.port, a.known_hosts)
    print(
        json.dumps(
            {
                "vm_id": vm,
                "ssh": target,
                "port": a.port,
                "privilege_context": "existing UTM guest agent",
                "sudoers_modified": False,
                "execute": a.execute,
            }
        )
    )
    if not (a.preflight or a.execute):
        return
    if a.execute:
        if not a.apk or hashlib.sha256(a.apk.read_bytes()).hexdigest() != a.apk_sha256:
            p.error("Verified APK required")
        import re

        if not a.image or not re.fullmatch(r"redroid/redroid@sha256:[0-9a-f]{64}", a.image):
            p.error("Verified immutable Redroid image required")
    run = "simufarm-stage-d/" + uuid.uuid4().hex
    remote = "/home/" + a.user + "/" + run
    subprocess.run(ssh + [shlex.join(["mkdir", "-p", run])], check=True, timeout=30)
    scp = [
        "scp",
        "-P",
        str(a.port),
        "-i",
        str(a.identity),
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=yes",
        "-o",
        f"UserKnownHostsFile={a.known_hosts}",
    ]
    local = a.output / Path(run).name
    local.mkdir(parents=True, exist_ok=False)

    def upload(source, name):
        subprocess.run(
            scp + [str(source), target + ":" + remote + "/" + name], check=True, timeout=180
        )

    probe = local / "probe.py"
    probe.write_text(
        "import contextlib,io\nwith contextlib.redirect_stdout(io.StringIO()) as capture:\n"
        + textwrap.indent(PROBE, " ")
        + "\nPath("
        + repr(remote + "/preflight.json")
        + ").write_text(capture.getvalue())\n"
    )
    upload(probe, "probe.py")
    qga(vm, remote + "/probe.py")
    report = wait_json(ssh, remote + "/preflight.json", 90)
    report["privilege_context"] = "UTM guest agent root; ordinary SSH user permissions unchanged"
    (local / "host-preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not a.execute:
        return
    require_host(report)
    for source, name in [
        (ROOT / "scripts/stage_d_remote.py", "collector.py"),
        (ROOT / "profiles/vivo/vivo-x100.json", "profile.json"),
        (a.apk, "sample.apk"),
    ]:
        upload(source, name)
    command = [
        "/usr/bin/python3",
        remote + "/collector.py",
        "--profile",
        remote + "/profile.json",
        "--apk",
        remote + "/sample.apk",
        "--apk-sha256",
        a.apk_sha256,
        "--image",
        a.image,
        "--output",
        remote + "/evidence",
        "--execute",
    ]
    wrapper = local / "run.py"
    wrapper.write_text(
        "import json,subprocess\nfrom pathlib import Path\nwith open("
        + repr(remote + "/collector.log")
        + ',"w") as log:\n result=subprocess.run('
        + repr(command)
        + ",stdout=log,stderr=log)\nPath("
        + repr(remote + "/result.json")
        + ').write_text(json.dumps({"returncode":result.returncode}))\n'
    )
    upload(wrapper, "run.py")
    qga(vm, remote + "/run.py")
    result = wait_json(ssh, remote + "/result.json", 2400)
    subprocess.run(
        scp + ["-r", target + ":" + remote + "/evidence", str(local)], check=True, timeout=180
    )
    subprocess.run(
        scp + [target + ":" + remote + "/collector.log", str(local / "collector.log")],
        check=True,
        timeout=60,
    )
    print(json.dumps({"local_evidence": str(local), "returncode": result["returncode"]}))
    if result["returncode"]:
        raise SystemExit("Stage D diagnostic failed; observed evidence preserved")


if __name__ == "__main__":
    main()
