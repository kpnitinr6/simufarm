"""Rebuild a names-only target proposal from an operator-supplied Google device CSV.
Does not fetch specs or approve targets. Usage: python scripts/propose_targets.py input.csv
"""

import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]


def j(p, value):
    (R / p).write_text(json.dumps(value, indent=2) + "\n")


raw = Path(sys.argv[1]).read_bytes()
rows = list(csv.DictReader(raw.decode("utf-16").splitlines()))
priority = [
    "Samsung",
    "Xiaomi",
    "OPPO",
    "vivo",
    "motorola",
    "HUAWEI",
    "HONOR",
    "realme",
    "OnePlus",
    "Google",
    "Sony",
    "Nokia",
    "ASUS",
    "Lenovo",
    "LGE",
    "TECNO",
    "Infinix",
    "Nothing",
    "ZTE",
    "TCL",
]
pools = {}
exclusion = re.compile(r"(?i)\b(tv|watch|chromebook|projector|box)\b")
for brand in priority:
    unique = {}
    for x in rows:
        name = x["Marketing Name"].strip()
        if (
            x["Retail Branding"].casefold() != brand.casefold()
            or not name
            or exclusion.search(name)
        ):
            continue
        key = name.casefold()
        if key not in unique:
            unique[key] = x
    pools[brand] = sorted(unique.values(), key=lambda x: x["Marketing Name"].casefold())
selected = []
while len(selected) < 1000:
    progress = False
    for brand in priority:
        if pools[brand]:
            selected.append(pools[brand].pop(0))
            progress = True
        if len(selected) == 1000:
            break
    if not progress:
        raise RuntimeError("Insufficient candidates")
targets = []
for i, x in enumerate(selected, 1):
    slug = re.sub(
        "[^a-z0-9]+", "-", (x["Retail Branding"] + "-" + x["Marketing Name"]).lower()
    ).strip("-")
    targets.append(
        {
            "target_id": f"target-{i:04d}",
            "proposed_profile_id": slug
            + "-"
            + hashlib.sha256(
                (x["Retail Branding"] + "|" + x["Marketing Name"]).encode()
            ).hexdigest()[:8],
            "brand": next(b for b in priority if b.casefold() == x["Retail Branding"].casefold()),
            "source_branding": x["Retail Branding"],
            "model": x["Marketing Name"],
            "source_model_code": x["Model"],
            "source_device_code": x["Device"],
            "source_url": "https://storage.googleapis.com/play_public/supported_devices.csv",
            "review_status": "pending",
            "device_class": "needs-human-classification",
        }
    )
j(
    "data/profiles/_targets.yaml",
    {
        "proposal_version": 1,
        "approval_status": "pending-human",
        "target_count": 1000,
        "scope": "Android names only; balanced brand coverage, not a popularity ranking. iOS visual targets can be added after review. No specs extracted.",
        "selection": "Round-robin over 20 familiar brands; distinct marketing names per brand; alphabetical within brand; filters obvious TV/watch/box names. Phone/tablet classification and regional variants need human review.",
        "targets": targets,
    },
)
j(
    "data/sources/google-device-names.provenance.json",
    {
        "source_url": "https://storage.googleapis.com/play_public/supported_devices.csv",
        "publisher_page": "https://support.google.com/googleplay/answer/1727131",
        "retrieved_on": "2026-10-27",
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_row_count": len(rows),
        "selected_count": 1000,
        "brand_counts": dict(collections.Counter(x["brand"] for x in targets)),
        "use": "Names and model identifiers only. Not a source of technical device specifications.",
        "license_status": "Public reference; redistribution rights not independently established. No logos, wallpapers, images, or raw full dataset bundled.",
    },
)
