#!/usr/bin/env python3
"""Stage E host adapter: explicit UTM guest-agent test, with strict local SSH trust."""

import argparse
import hashlib
import json
import shlex
import subprocess
import uuid
import zipfile
from pathlib import Path

from stage_d_local import ROOT, ssh_args
from stage_d_utm import qga, wait_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vm-id", required=True, type=uuid.UUID)
    p.add_argument("--identity", required=True, type=Path)
    p.add_argument("--known-hosts", required=True, type=Path)
    p.add_argument("--magisk-apk", type=Path)
    p.add_argument("--output", type=Path, default=ROOT / "data/runtime/local/stage-e")
    p.add_argument("--execute-test", action="store_true")
    a = p.parse_args()
    if not a.execute_test:
        print("Plan only. No Oracle API, SSH or Docker calls. Five-container ceiling.")
        return
    tool = json.loads((ROOT / "infra/redroid-identity/toolchain.json").read_text())
    if (
        not a.magisk_apk
        or hashlib.sha256(a.magisk_apk.read_bytes()).hexdigest() != tool["apk_sha256"]
    ):
        p.error("Official pinned Magisk APK digest required")
    run_id = uuid.uuid4().hex
    remote = "/home/simufarm/stage-e/" + run_id
    local = a.output / run_id
    local.mkdir(parents=True, exist_ok=False)
    ssh = ssh_args("127.0.0.1", "simufarm", a.identity, "utm", 2222, a.known_hosts)
    subprocess.run(ssh + [shlex.join(["mkdir", "-p", remote + "/context"])], check=True)
    scp = [
        "scp",
        "-P",
        "2222",
        "-i",
        str(a.identity),
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=yes",
        "-o",
        f"UserKnownHostsFile={a.known_hosts}",
    ]

    def upload(path, name):
        subprocess.run(
            scp + [str(path), "simufarm@127.0.0.1:" + remote + "/" + name], check=True, timeout=180
        )

    with zipfile.ZipFile(a.magisk_apk) as archive:
        binary = archive.read(tool["binary_entry"])
    if hashlib.sha256(binary).hexdigest() != tool["binary_sha256"]:
        p.error("Extracted ARM64 tool digest mismatch")
    (local / "magisk").write_bytes(binary)
    upload(local / "magisk", "context/magisk")
    for name in [
        "Dockerfile",
        "simufarm-identity.sh",
        "init.rc",
        "toolchain.json",
        ".dockerignore",
    ]:
        upload(ROOT / "infra/redroid-identity" / name, "context/" + name)
    upload(ROOT / "data/runtime-test-profiles/vivo-x100-china.json", "profile.json")
    upload(ROOT / "scripts/stage_e_remote.py", "collector.py")
    wrapper = local / "run.py"
    wrapper.write_text(
        "import json,subprocess\nfrom pathlib import Path\nwith open("
        + repr(remote + "/run.log")
        + ',"w") as log:\n p=subprocess.run('
        + repr(
            ["/usr/bin/python3", remote + "/collector.py", "--workspace", remote, "--execute-test"]
        )
        + ",stdout=log,stderr=log)\nPath("
        + repr(remote + "/result.json")
        + ').write_text(json.dumps({"returncode":p.returncode}))\n'
    )
    upload(wrapper, "run.py")
    qga(str(a.vm_id).upper(), remote + "/run.py")
    print(json.dumps({"guest_workspace": remote, "local_output": str(local)}), flush=True)
    result = wait_json(ssh, remote + "/result.json", 1200)
    subprocess.run(
        scp + ["-r", "simufarm@127.0.0.1:" + remote + "/.", str(local)], check=True, timeout=180
    )
    print(json.dumps(result))
    if result["returncode"]:
        raise SystemExit("Stage E test failed; raw evidence retained")


if __name__ == "__main__":
    main()
