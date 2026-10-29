#!/usr/bin/env python3
"""ADR 015: one home-region A1 VM; no implicit retries or paid fallback."""

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

import oci_rest
from oci_rest import OCIError, call, get, listing

SHAPE = "VM.Standard.A1.Flex"
CONFIG = {"ocpus": 2, "memoryInGBs": 12}
TAGS = {"project": "simufarm", "tier": "always-free", "stage": "D"}


def capacity_error(exc):
    return (
        exc.status == 500
        and exc.data.get("code") == "InternalError"
        and exc.data.get("message", "").strip().lower().rstrip(".") == "out of host capacity"
    )


def validate_instance(instance, ad):
    conf = instance.get("shapeConfig", {})
    if instance.get("shape") != SHAPE or conf.get("ocpus") != 2 or conf.get("memoryInGBs") != 12:
        raise RuntimeError("P0: unexpected instance shape/config; halt immediately")
    if instance.get("availabilityDomain") != ad:
        raise RuntimeError("P0: unexpected availability domain")


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2) + "\n")
    os.chmod(temp, 0o600)
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--pin", required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    c, region = oci_rest.configure()
    proof = json.loads(args.preflight.read_text())
    base = Path(__file__).resolve().parents[1]
    head = subprocess.check_output(["git", "-C", str(base), "rev-parse", "HEAD"], text=True).strip()
    if head != args.pin:
        raise SystemExit("Pinned commit differs from checkout")
    for file in ["scripts/stage_d_adr015_retry.py", "scripts/oci_rest.py"]:
        pinned = subprocess.check_output(["git", "-C", str(base), "show", head + ":" + file])
        if hashlib.sha256(pinned).digest() != hashlib.sha256((base / file).read_bytes()).digest():
            raise SystemExit("Runtime code differs from pinned commit")
    if proof["home_region"] != "ap-mumbai-1" or region != proof["home_region"]:
        raise SystemExit("Home-region guard failed")
    if proof["ad"] != "PeUh:AP-MUMBAI-1-AD-1" or proof["compartment_id"] != c["tenancy"]:
        raise SystemExit("AD/compartment guard failed")
    if proof["zero_spend_confirmed"] is not True or proof["billing_nonfree_observed"] is not False:
        raise SystemExit("Zero-spend guard failed")
    if proof["existing_instances"] or proof["existing_storage_gb"] != 0:
        raise SystemExit("Expected clean aggregate tenancy inventory")
    if not args.execute:
        print(
            json.dumps(
                {
                    "shape": SHAPE,
                    "shape_config": CONFIG,
                    "max_attempts": 500,
                    "max_seconds": 86400,
                    "backoff_seconds": 60,
                    "pin": head,
                }
            )
        )
        return
    args.state_dir.mkdir(parents=True, exist_ok=True)
    lock = (args.state_dir / "run.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    if (args.state_dir / "state.json").exists():
        raise SystemExit("Prior run state exists: do not reset bounds or duplicate launches")
    ad = proof["ad"]
    compartment = proof["compartment_id"]
    regions = get("identity", "/20160918/tenancies/" + c["tenancy"] + "/regionSubscriptions")
    if not any(x["isHomeRegion"] and x["regionName"] == region for x in regions):
        raise SystemExit("Live home-region guard failed")
    existing = listing("iaas", "/20160918/instances", {"compartmentId": compartment})
    if any(x["lifecycleState"] not in ["TERMINATED"] for x in existing):
        raise SystemExit("Existing instance found; inspect rather than launch")
    subnet = get("iaas", "/20160918/subnets/" + proof["subnet_id"])
    if subnet["lifecycleState"] != "AVAILABLE":
        raise SystemExit("Subnet unavailable")
    image = get("iaas", "/20160918/images/" + proof["image_id"])
    if (
        image["lifecycleState"] != "AVAILABLE"
        or "aarch64" not in image["displayName"]
        or image["operatingSystem"] != "Canonical Ubuntu"
    ):
        raise SystemExit("Image guard failed")
    started = datetime.now(UTC).isoformat()
    clock = time.monotonic()
    deadline = clock + 86400
    wall_deadline = time.time() + 86400
    state = {
        "started_at": started,
        "attempts": 0,
        "status": "running",
        "pin": head,
        "region": region,
        "ad": ad,
        "pid": os.getpid(),
        "deadline_hours": 24,
    }
    atomic(args.state_dir / "state.json", state)
    token = "simufarm-d-" + hashlib.sha256(started.encode()).hexdigest()[:48]
    key = Path(proof["ssh_public_key_file"]).read_text().strip()
    if not key.startswith("ssh-ed25519 "):
        raise SystemExit("Expected dedicated public SSH key")
    launch = {
        "displayName": "simufarm-stage-d-a1",
        "compartmentId": compartment,
        "availabilityDomain": ad,
        "shape": SHAPE,
        "shapeConfig": CONFIG,
        "sourceDetails": {
            "sourceType": "image",
            "imageId": proof["image_id"],
            "bootVolumeSizeInGBs": 50,
        },
        "createVnicDetails": {"subnetId": proof["subnet_id"], "assignPublicIp": True},
        "metadata": {"ssh_authorized_keys": key},
        "freeformTags": TAGS,
        "instanceOptions": {"areLegacyImdsEndpointsDisabled": True},
    }
    try:
        for attempt in range(1, 501):
            if time.monotonic() >= deadline or time.time() >= wall_deadline:
                break
            state["attempts"] = attempt
            atomic(args.state_dir / "state.json", state)
            outcome = {"attempt": attempt, "at": datetime.now(UTC).isoformat()}
            try:
                instance = call(
                    "iaas", "/20160918/instances", launch, extra={"opc-retry-token": token}
                )[0]
                outcome.update(outcome="launch_returned", instance_id=instance["id"])
            except OCIError as exc:
                outcome.update(
                    outcome="capacity" if capacity_error(exc) else "fatal",
                    http_status=exc.status,
                    code=exc.data.get("code"),
                    message=exc.data.get("message"),
                )
                with (args.state_dir / "attempts.jsonl").open("a") as f:
                    f.write(json.dumps(outcome) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                print(json.dumps(outcome), flush=True)
                if not capacity_error(exc):
                    raise
                if (
                    attempt < 500
                    and time.monotonic() + 60 < deadline
                    and time.time() + 60 < wall_deadline
                ):
                    time.sleep(60)
                    continue
                break
            except Exception as exc:
                outcome.update(outcome="fatal", error_type=type(exc).__name__, message=str(exc))
                with (args.state_dir / "attempts.jsonl").open("a") as f:
                    f.write(json.dumps(outcome) + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                raise
            with (args.state_dir / "attempts.jsonl").open("a") as f:
                f.write(json.dumps(outcome) + "\n")
                f.flush()
                os.fsync(f.fileno())
            # Save identity immediately, before any SSH or further action.
            evidence = {
                "instance_ocid": instance["id"],
                "shape": instance.get("shape"),
                "shape_config": instance.get("shapeConfig"),
                "ad": ad,
                "region": region,
                "public_ip": None,
                "launch_timestamp": instance.get("timeCreated"),
                "preflight_a1_availability": proof["capacity"],
                "attempt_count": attempt,
                "pin": head,
                "time_to_capacity_seconds": time.monotonic() - clock,
                "ssh_started": False,
            }
            atomic(args.evidence, evidence)
            validate_instance(instance, ad)
            updated = call(
                "iaas",
                "/20160918/instances/" + instance["id"],
                {"freeformTags": TAGS},
                method="PUT",
            )[0]
            validate_instance(updated, ad)
            evidence["freeform_tags"] = updated.get("freeformTags")
            atomic(args.evidence, evidence)
            # Poll reads only; a post-launch error halts rather than launching again.
            for _ in range(120):
                current = get("iaas", "/20160918/instances/" + instance["id"])
                validate_instance(current, ad)
                evidence["lifecycle_state"] = current["lifecycleState"]
                vnics = listing(
                    "iaas",
                    "/20160918/vnicAttachments",
                    {"compartmentId": compartment, "instanceId": instance["id"]},
                )
                for attachment in vnics:
                    if attachment.get("vnicId") and attachment["lifecycleState"] == "ATTACHED":
                        evidence["public_ip"] = get(
                            "iaas", "/20160918/vnics/" + attachment["vnicId"]
                        ).get("publicIp")
                atomic(args.evidence, evidence)
                if current["lifecycleState"] == "RUNNING" and evidence["public_ip"]:
                    state.update(status="success", instance_ocid=instance["id"])
                    atomic(args.state_dir / "state.json", state)
                    print(json.dumps(state), flush=True)
                    return
                if current["lifecycleState"] in ["TERMINATED", "TERMINATING"]:
                    raise RuntimeError("Instance unexpectedly terminated")
                time.sleep(10)
            raise RuntimeError("Post-launch observation timed out; do not launch another VM")
        state["status"] = "bounds_exhausted"
    except Exception as exc:
        state.update(status="halted", error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        state["updated_at"] = datetime.now(UTC).isoformat()
        atomic(args.state_dir / "state.json", state)


if __name__ == "__main__":
    main()
