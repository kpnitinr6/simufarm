#!/usr/bin/env python3
"""Local GADS compatibility wrapper; use as `appium` before the real binary on PATH."""

import os
import sys
from pathlib import Path


def server_args(args, log):
    management = any(
        x
        in (
            "driver",
            "plugin",
            "setup",
            "extension",
            "--help",
            "-h",
            "--version",
            "-v",
            "--show-config",
        )
        for x in args
    )
    if management:
        return args
    normalized = [
        ("--use-plugins=" + x.split("=", 1)[1]) if x.startswith("--use-plugin=") else x
        for x in args
    ]
    return normalized + ["--address", "127.0.0.1", "--log", str(log)]


def main():
    real = Path(os.environ["SIMUFARM_APPIUM_REAL"]).resolve()
    if real == Path(__file__).resolve():
        raise SystemExit("Real Appium path cannot point back to wrapper")
    log = Path(os.environ.get("SIMUFARM_APPIUM_LOG", "appium-managed.log")).resolve()
    os.execv(str(real), [str(real)] + server_args(sys.argv[1:], log))


if __name__ == "__main__":
    main()
