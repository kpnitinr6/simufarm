#!/usr/bin/env python3
"""Prepared local Appium harness. No network action without --execute."""

import argparse
import base64
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def local_endpoint(value):
    u = urlsplit(value)
    if (
        u.scheme != "http"
        or u.hostname not in ("127.0.0.1", "localhost")
        or u.username
        or u.password
        or u.query
        or u.fragment
        or u.path not in ("", "/")
        or u.port != 14723
    ):
        raise ValueError("Expected local SSH-tunneled Appium endpoint on port14723")
    return value.rstrip("/")


def request(endpoint, method, route, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = Request(
        endpoint + route, data=body, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urlopen(req, timeout=120) as response:
            result = json.load(response)
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"Appium HTTP{exc.code} {route}: {detail}") from exc
    value = result.get("value", {})
    if isinstance(value, dict) and value.get("error"):
        raise RuntimeError(value)
    return result


def smoke(endpoint, caps, output, *, gads_managed=False):
    session = None
    report = {
        "stage": "G",
        "mode": "gads-managed-appium-smoke" if gads_managed else "standalone-appium-smoke",
        "passed": False,
    }
    output.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    try:
        status = request(endpoint, "GET", "/status")
        if not status.get("value", {}).get("ready"):
            raise RuntimeError("Appium is not ready")
        result = request(endpoint, "POST", "/session", {"capabilities": {"alwaysMatch": caps}})
        value = result["value"]
        session = value["sessionId"]
        report["session_id"] = session
        report["capabilities"] = value.get("capabilities", {})
        source = request(endpoint, "GET", f"/session/{session}/source")["value"]
        if not source or "<hierarchy" not in source:
            raise RuntimeError("No Android view hierarchy returned")
        (output / "source.xml").write_text(source)
        if "io.appium.android.apis" not in source:
            raise RuntimeError("ApiDemos package absent from the view hierarchy")
        steps = []
        for label in ("Views", "Buttons", "Normal"):
            element = request(
                endpoint,
                "POST",
                f"/session/{quote(session, safe='')}/element",
                {"using": "accessibility id", "value": label},
            )["value"]
            element_id = element.get("element-6066-11e4-a52e-4f735466cecf") or element.get(
                "ELEMENT"
            )
            if not element_id:
                raise RuntimeError(f"Missing element id for {label}")
            request(
                endpoint,
                "POST",
                f"/session/{quote(session, safe='')}/element/{quote(element_id, safe='')}/click",
                {},
            )
            steps.append({"action": "click", "accessibility_id": label, "passed": True})
        report["steps"] = steps
        (output / "source-after-actions.xml").write_text(
            request(endpoint, "GET", f"/session/{quote(session, safe='')}/source")["value"]
        )

        shot = request(endpoint, "GET", f"/session/{session}/screenshot")["value"]
        (output / "screenshot.png").write_bytes(base64.b64decode(shot, validate=True))
        report["passed"] = True
    except Exception as exc:
        report["error"] = str(exc)
        raise
    finally:
        if session:
            try:
                request(endpoint, "DELETE", f"/session/{session}")
                report["session_deleted"] = True
            except (RuntimeError, OSError, ValueError) as exc:
                report["session_deleted"] = False
                report["teardown_error"] = str(exc)
                report["passed"] = False
        report["elapsed_seconds"] = round(time.monotonic() - start, 3)
        (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    if not report["passed"]:
        raise RuntimeError("Smoke teardown failed; see evidence")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--endpoint", default="http://127.0.0.1:14723", type=local_endpoint)
    p.add_argument(
        "--capabilities",
        type=Path,
        default=ROOT / "infra/local-automation/appium-capabilities.json",
    )
    p.add_argument("--output", type=Path, default=ROOT / "data/runtime/local/stage-g-smoke")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--gads-managed", action="store_true")
    a = p.parse_args()
    caps = json.loads(a.capabilities.read_text())
    print(
        json.dumps(
            {
                "execute": a.execute,
                "endpoint": a.endpoint,
                "device_in_vm": caps["appium:udid"],
                "ssh_port_is_not_adb": 2222,
            }
        )
    )
    if a.execute:
        smoke(a.endpoint, caps, a.output, gads_managed=a.gads_managed)


if __name__ == "__main__":
    main()
