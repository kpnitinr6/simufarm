#!/usr/bin/env python3
"""Bounded OCI A1 retry adapter. Dry run by default; never use trial credits."""

import argparse
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path

SHAPE = "VM.Standard.A1.Flex"
UPSTREAM = "https://github.com/ibrahaimbadri/oci-arm-free-retry/tree/8de2e4cef89b453dd00945a89f0811fb323bfd25"


def oracle_enabled():
    target = Path(__file__).resolve().parents[1] / "config/stage-d-target.json"
    return target.exists() and json.loads(target.read_text()).get("oracle_enabled") is True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preflight",
        type=Path,
        required=True,
        help="Private, recently reviewed JSON evidence/config; do not commit",
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=12)
    args = parser.parse_args()
    if args.execute and not oracle_enabled():
        raise SystemExit("Oracle disabled: ADR 015 superseded by local hardware pivot")
    if not 1 <= args.max_attempts <= 144:
        parser.error("max-attempts must be 1..144")
    proof = json.loads(args.preflight.read_text())
    required = (
        "home_region",
        "compartment_id",
        "subnet_id",
        "image_id",
        "ssh_public_key_file",
        "always_free_image_evidence",
        "tenancy_allowance_evidence",
        "aggregate_inventory_evidence",
        "monthly_remaining_evidence",
        "repo_public_evidence",
        "reviewed_at",
        "availability_domains",
    )
    if any(not proof.get(key) for key in required):
        raise SystemExit("Incomplete private preflight evidence/config")
    reviewed = datetime.fromisoformat(proof["reviewed_at"])
    age = (datetime.now(UTC) - reviewed).total_seconds()
    if not 0 <= age <= 3600:
        raise SystemExit("Preflight evidence must be reviewed within the past hour")
    for key in (
        "always_free_image_evidence",
        "tenancy_allowance_evidence",
        "aggregate_inventory_evidence",
        "monthly_remaining_evidence",
        "repo_public_evidence",
    ):
        if not Path(proof[key]).is_file():
            raise SystemExit(f"Missing evidence file: {key}")
    if (
        proof.get("zero_spend_confirmed") is not True
        or proof.get("paid_fallback_allowed") is not False
    ):
        raise SystemExit("Zero-spend/no-paid-fallback attestation required")
    if proof.get("remaining_ocpus", 0) < 2 or proof.get("remaining_memory_gb", 0) < 12:
        raise SystemExit("Insufficient remaining free A1 allocation")
    if proof.get("remaining_storage_gb", 0) < 50 or proof.get("remaining_ocpu_hours", 0) < 1488:
        raise SystemExit("Insufficient remaining storage/monthly allocation")
    if proof.get("remaining_memory_gb_hours", 0) < 8928:
        raise SystemExit("Insufficient remaining monthly memory allocation")
    plan = {
        "shape": SHAPE,
        "ocpus": 2,
        "memory_gb": 12,
        "boot_volume_gb": 50,
        "max_attempts": args.max_attempts,
        "interval_seconds": 60,
        "upstream_review": UPSTREAM,
        "preflight_sha256": hashlib.sha256(args.preflight.read_bytes()).hexdigest(),
        "execute": args.execute,
    }
    print(json.dumps(plan, indent=2))
    if not args.execute:
        return
    import oci  # Optional SDK; not installed automatically and not needed for dry runs.

    config = oci.config.from_file(profile_name=proof.get("oci_profile", "DEFAULT"))
    if config["region"] != proof["home_region"]:
        raise SystemExit("OCI config region differs from attested home region")
    identity = oci.identity.IdentityClient(config)
    regions = identity.list_region_subscriptions(config["tenancy"]).data
    if not any(r.is_home_region and r.region_name == config["region"] for r in regions):
        raise SystemExit("Live tenancy home-region validation failed")
    compute = oci.core.ComputeClient(config)
    network = oci.core.VirtualNetworkClient(config)
    image = compute.get_image(proof["image_id"]).data
    if image.lifecycle_state != "AVAILABLE" or "aarch64" not in image.display_name.lower():
        raise SystemExit("Image not available or ARM64 image identification failed")
    subnet = network.get_subnet(proof["subnet_id"]).data
    if subnet.lifecycle_state != "AVAILABLE":
        raise SystemExit("Subnet unavailable")
    # The private aggregate inventory evidence must include ALL compartments and boot/block volumes.
    # SDK listing in the selected compartment is an extra duplicate guard, not an allowance calculation.
    existing = oci.pagination.list_call_get_all_results(
        compute.list_instances, proof["compartment_id"]
    ).data
    name = "simufarm-stage-d-a1"
    if any(
        i.display_name == name and i.lifecycle_state not in ("TERMINATED", "TERMINATING")
        for i in existing
    ):
        raise SystemExit("Existing Stage D instance: inspect/reuse instead of creating another")
    key = Path(proof["ssh_public_key_file"]).expanduser().read_text().strip()
    if not key.startswith(("ssh-ed25519 ", "ssh-rsa ", "ecdsa-sha2-")):
        raise SystemExit("A public SSH key is required")
    ads = proof["availability_domains"]
    launch_token = "simufarm-" + plan["preflight_sha256"][:48]
    for attempt in range(args.max_attempts):
        if (datetime.now(UTC) - reviewed).total_seconds() > 3600:
            raise SystemExit("Preflight review expired during retry window; refresh evidence")
        details = oci.core.models.LaunchInstanceDetails(
            display_name=name,
            compartment_id=proof["compartment_id"],
            availability_domain=ads[attempt % len(ads)],
            shape=SHAPE,
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=2, memory_in_gbs=12
            ),
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                image_id=proof["image_id"], boot_volume_size_in_gbs=50
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=proof["subnet_id"], assign_public_ip=True
            ),
            metadata={"ssh_authorized_keys": key},
            instance_options=oci.core.models.InstanceOptions(
                are_legacy_imds_endpoints_disabled=True
            ),
        )
        try:
            result = compute.launch_instance(
                details,
                opc_retry_token=launch_token + "-" + str(attempt % len(ads)),
                retry_strategy=oci.retry.NoneRetryStrategy(),
            ).data
            print(json.dumps({"instance_id": result.id, "state": result.lifecycle_state}))
            return
        except oci.exceptions.ServiceError as exc:
            capacity = "out of host capacity" in (exc.message or "").lower()
            if not capacity and exc.status != 429:
                raise  # Auth/quota/price/unknown failures never trigger a paid fallback or blind retry.
            print(
                json.dumps(
                    {
                        "attempt": attempt + 1,
                        "retry_reason": "capacity" if capacity else "rate_limit",
                    }
                )
            )
            if attempt + 1 < args.max_attempts:
                time.sleep(min(60 * (2 ** min(attempt, 4)) if exc.status == 429 else 60, 900))
    raise SystemExit("Bounded capacity attempts exhausted; no instance claimed")


if __name__ == "__main__":
    main()
