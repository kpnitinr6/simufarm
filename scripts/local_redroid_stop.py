#!/usr/bin/env python3
"""Stop one owned Redroid instance via Android shutdown in a verified private PID namespace."""

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path


def private_namespace(info, host_namespace, container_namespace):
    return (
        info["HostConfig"].get("PidMode", "") in ("", "private")
        and info["State"]["Pid"] > 1
        and host_namespace != container_namespace
    )


def command(*args):
    return subprocess.run(args, capture_output=True, text=True, check=False, timeout=90)


def stop(name):
    if not re.fullmatch(r"simufarm-stage-e-[a-f0-9]{12}-[12]", name):
        raise ValueError("Only specifically named SimuFarm Stage E containers are supported")
    info = json.loads(subprocess.check_output(["docker", "inspect", name]))[0]
    if not info["State"]["Running"]:
        return {"container": name, "already_stopped": True, "running": False}
    host = os.readlink("/proc/1/ns/pid")
    child = os.readlink(f"/proc/{info['State']['Pid']}/ns/pid")
    if not private_namespace(info, host, child):
        raise RuntimeError("Refuse Android poweroff without a verified private PID namespace")
    command("docker", "exec", name, "/system/bin/sync")
    request = command(
        "docker", "exec", name, "/system/bin/setprop", "sys.powerctl", "shutdown,userrequested"
    )
    start = time.monotonic()
    fallback = False
    while time.monotonic() - start < 40:
        info = json.loads(subprocess.check_output(["docker", "inspect", name]))[0]
        if not info["State"]["Running"]:
            break
        time.sleep(1)
    else:
        fallback = True
        command("docker", "stop", "--time", "30", name)
        info = json.loads(subprocess.check_output(["docker", "inspect", name]))[0]
    return {
        "container": name,
        "method": "Android sys.powerctl shutdown in private PID namespace",
        "host_namespace": host,
        "container_namespace": child,
        "request_returncode": request.returncode,
        "docker_stop_fallback": fallback,
        "running": info["State"]["Running"],
        "exit_code": info["State"]["ExitCode"],
        "oom_killed": info["State"]["OOMKilled"],
        "data_retained": True,
        "shutdown_seconds": round(time.monotonic() - start, 3),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("container")
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    result = stop(a.container)
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    if result["running"]:
        raise SystemExit("Container did not stop")
