#!/usr/bin/env python3
"""Plan, inspect or deploy Stage D on a local Ubuntu server over Meshnet SSH."""

import argparse
import hashlib
import ipaddress
import json
import re
import shlex
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESHNET = ipaddress.ip_network("100.64.0.0/10")
PROBE = r"""
import json,platform,shutil,subprocess
from pathlib import Path
osinfo=dict(line.split('=',1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
def check(*args):
 try:
  p=subprocess.run(args,capture_output=True,text=True,timeout=20)
  return {'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
 except (OSError,subprocess.TimeoutExpired) as e:return {'error':str(e)}
memory=next(x for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemTotal:'))
print(json.dumps({'system':platform.system(),'architecture':platform.machine(),'os_id':osinfo.get('ID','').strip('"'),'os_version':osinfo.get('VERSION_ID','').strip('"'),'kernel':platform.release(),'memory':memory,'free_disk_bytes':shutil.disk_usage(Path.home()).free,'kvm_present':Path('/dev/kvm').exists(),'docker':check('docker','info','--format','{{.Architecture}}'),'adb':check('adb','version'),'sudo':check('sudo','-n','true'),'binder_module':check('modinfo','binder_linux'),'ashmem_module':check('modinfo','ashmem_linux')}))
"""


def endpoint(host, user):
    address = ipaddress.ip_address(host)
    if address.version != 4 or address not in MESHNET:
        raise ValueError("Expected Meshnet IPv4 in 100.64.0.0/10")
    if not re.fullmatch(r"[a-z_][a-z0-9_-]*", user):
        raise ValueError("Invalid SSH username")
    return f"{user}@{address}"


def ssh_args(host, user, key=None):
    args = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=yes",
        "-o",
        "ConnectTimeout=15",
    ]
    if key:
        args += ["-i", str(key)]
    return args + [endpoint(host, user)]


def require_host(report):
    if (report["system"], report["os_id"], report["os_version"]) != ("Linux", "ubuntu", "22.04"):
        raise ValueError("This deployment requires Ubuntu 22.04")
    if report["architecture"] not in ("x86_64", "amd64", "aarch64", "arm64"):
        raise ValueError("Unsupported CPU architecture")
    for name in ("docker", "adb", "sudo", "binder_module", "ashmem_module"):
        if report[name].get("returncode") != 0:
            raise ValueError(
                f"{name} prerequisite failed; inspect preflight, do not install kernels blindly"
            )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--host", required=True)
    p.add_argument("--user", required=True)
    p.add_argument("--identity", type=Path)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--execute", action="store_true")
    p.add_argument("--profile", type=Path, default=ROOT / "profiles/vivo/vivo-x100.json")
    p.add_argument("--apk", type=Path)
    p.add_argument("--apk-sha256")
    p.add_argument("--image")
    p.add_argument("--output", type=Path, default=ROOT / "data/runtime/local")
    a = p.parse_args()
    ssh = ssh_args(a.host, a.user, a.identity)
    plan = {
        "target": endpoint(a.host, a.user),
        "transport": "SSH over Meshnet",
        "execute": a.execute,
        "oracle_api_calls": 0,
        "adb_bind": "remote loopback only",
    }
    print(json.dumps(plan, indent=2))
    if not (a.preflight or a.execute):
        return
    result = subprocess.run(
        ssh + ["python3 -"], input=PROBE, text=True, capture_output=True, check=True, timeout=90
    )
    report = json.loads(result.stdout)
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "host-preflight.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not a.execute:
        return
    require_host(report)
    if (
        not a.apk
        or not a.apk_sha256
        or hashlib.sha256(a.apk.read_bytes()).hexdigest() != a.apk_sha256
    ):
        p.error("Existing local APK and matching --apk-sha256 required")
    if not a.image or not re.fullmatch(r"redroid/redroid@sha256:[0-9a-f]{64}", a.image):
        p.error("Supply a verified immutable --image matching the observed server architecture")
    profile = json.loads(a.profile.read_text())
    if profile.get("id") != "vivo-x100":
        p.error("Stage D diagnostic profile must be vivo-x100")
    run = "simufarm-stage-d/" + uuid.uuid4().hex
    subprocess.run(ssh + [shlex.join(["mkdir", "-p", run])], check=True, timeout=30)
    scp = ["scp", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=yes"]
    if a.identity:
        scp += ["-i", str(a.identity)]
    for source, name in [
        (ROOT / "scripts/stage_d_remote.py", "collector.py"),
        (a.profile, "profile.json"),
        (a.apk, "sample.apk"),
    ]:
        subprocess.run(
            scp + [str(source), endpoint(a.host, a.user) + ":" + run + "/" + name],
            check=True,
            timeout=180,
        )
    command = [
        "python3",
        run + "/collector.py",
        "--profile",
        run + "/profile.json",
        "--apk",
        run + "/sample.apk",
        "--apk-sha256",
        a.apk_sha256,
        "--image",
        a.image,
        "--output",
        run + "/evidence",
        "--execute",
    ]
    # Copy diagnostics back even when boot, kernel or identity validation fails.
    observed = subprocess.run(ssh + [shlex.join(command)], check=False, timeout=2400)
    copied = subprocess.run(
        scp
        + [
            "-r",
            endpoint(a.host, a.user) + ":" + run + "/evidence",
            str(a.output / Path(run).name),
        ],
        check=False,
        timeout=180,
    )
    if observed.returncode or copied.returncode:
        raise SystemExit("Stage D incomplete/failed; inspect fetched evidence; no success claimed")


if __name__ == "__main__":
    main()
