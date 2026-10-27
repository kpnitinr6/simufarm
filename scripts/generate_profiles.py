"""Deterministic, static-only Stage C CSV generation. No runtime promotion or research."""

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from simufarm_schema import DeviceProfile

ROOT = Path(__file__).resolve().parents[1]
SAFE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = {
    "id",
    "brand",
    "model",
    "release_year",
    "os_version",
    "width_px",
    "height_px",
    "dpi",
    "notch",
    "notch_position",
    "ram_gb",
    "screen_inches",
    "chipset_family",
    "source_urls",
}
FIELD_COLUMNS = {
    "id": "id",
    "brand": "brand",
    "model": "model",
    "release_year": "release_year",
    "os_version": "os_version",
    "screen.width_px": "width_px",
    "screen.height_px": "height_px",
    "screen.dpi": "dpi",
    "notch": "notch",
    "ram_gb": "ram_gb",
}


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def write_changed(path, content):
    if not path.exists() or path.read_text() != content:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def screen_class(inches):
    return "under-6" if inches < 6 else "6-to-under-6.5" if inches < 6.5 else "6.5-plus"


def read_rows(csv_path):
    with Path(csv_path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError(
                f"Missing CSV columns: {sorted(REQUIRED - set(reader.fieldnames or []))}"
            )
        rows = list(reader)
    ids, identities = set(), set()
    for line, row in enumerate(rows, 2):
        if None in row or any(not (row.get(key) or "").strip() for key in REQUIRED):
            raise ValueError(f"Missing or malformed CSV fields on line {line}")
        if not SAFE_ID.fullmatch(row["id"]) or not SAFE_ID.fullmatch(row["brand"]):
            raise ValueError(f"Unsafe identity on line {line}")
        model_key = re.sub(r"[^a-z0-9]", "", row["model"].casefold().replace("+", "plus"))
        brand_key = re.sub(r"[^a-z0-9]", "", row["brand"].casefold())
        if model_key.startswith(brand_key):
            model_key = model_key[len(brand_key) :]
        identity = (row["brand"], model_key)
        if row["id"] in ids or identity in identities:
            raise ValueError(f"Duplicate device on line {line}")
        ids.add(row["id"])
        identities.add(identity)
        for field in ("dpi", "ram_gb", "screen_inches"):
            if not math.isfinite(float(row[field])) or float(row[field]) <= 0:
                raise ValueError(f"Invalid {field} on line {line}")
        if int(row["release_year"]) < 2020 and not row.get("pre_2020_justification", "").strip():
            raise ValueError(f"Pre-2020 device needs sourced justification on line {line}")
        urls = json.loads(row["source_urls"])
        if (
            not isinstance(urls, list)
            or not urls
            or any(
                not isinstance(url, str)
                or urlparse(url).scheme not in {"http", "https"}
                or not urlparse(url).netloc
                for url in urls
            )
        ):
            raise ValueError(f"Invalid source_urls on line {line}")
        if row["chipset_family"].strip().casefold() in {"0", "unknown", "none", "n/a", "null"}:
            raise ValueError(f"Unknown chipset cannot count as diversity evidence on line {line}")
        row["_sources"] = sorted(set(urls))
        row["_line"] = line
    return rows


def validate_cohort(rows, exemptions=()):
    """Exemptions waive per-brand constraints only; global diversity cannot be waived."""
    counts = Counter(row["brand"] for row in rows)
    if len(rows) != 1000 or len(counts) != 20 or counts.get("nothing") != 11:
        raise ValueError("Cohort requires exactly 1000 rows, 20 brands, and Nothing quota 11")
    constraints = {
        "os_versions": (lambda row: row["os_version"], 3),
        "screen_sizes": (lambda row: screen_class(float(row["screen_inches"])), 2),
        "chipset_families": (lambda row: row["chipset_family"].casefold(), 2),
    }
    allowed = {}
    for item in exemptions:
        if not all(item.get(key) for key in ("brand", "constraint", "reason", "global_minimum")):
            raise ValueError("Exemption requires brand, constraint, reason, global_minimum")
        key = (item["brand"], item["constraint"])
        if key in allowed or item["constraint"] not in {*constraints, "quota"}:
            raise ValueError("Duplicate or unknown exemption")
        allowed[key] = item
    used = set()
    for constraint, (get_value, minimum) in constraints.items():
        if len({get_value(row) for row in rows}) < minimum:
            raise ValueError(f"Mandatory global diversity failed: {constraint}")
        for brand in counts:
            if len({get_value(row) for row in rows if row["brand"] == brand}) < minimum:
                key = (brand, constraint)
                if key not in allowed:
                    raise ValueError(
                        f"Per-brand diversity requires exemption: {brand}:{constraint}"
                    )
                used.add(key)
    for brand, count in counts.items():
        if count != 50:
            key = (brand, "quota")
            if key not in allowed:
                raise ValueError(f"Quota redistribution requires exemption: {brand}")
            used.add(key)
    if set(allowed) != used:
        raise ValueError("Stale exemption does not correspond to a failed constraint")
    return dict(sorted(counts.items()))


def prepare(row, template, csv_name):
    sources = row["_sources"]
    payload = dict(template)
    payload.update(
        {
            "id": row["id"],
            "brand": row["brand"],
            "model": row["model"],
            "release_year": int(row["release_year"]),
            "os_family": "android",
            "os_version": row["os_version"],
            "shell_id": row["brand"],
            "base_image_id": None,
            "screen": {
                "width_px": int(row["width_px"]),
                "height_px": int(row["height_px"]),
                "dpi": float(row["dpi"]),
            },
            "notch": {"type": row["notch"], "position": row["notch_position"]},
            "ram_gb": float(row["ram_gb"]),
            "build": None,
            "runtime_eligible": False,
            "source_type": "scraper",
            "sources": sources,
            "confidence": 0.85,
            "verified_by": None,
            "verified_at": None,
        }
    )
    # Canonical validation occurs before any output mutation, including evidence writes.
    profile = DeviceProfile.model_validate(payload).model_dump(mode="json", by_alias=True)
    fields = {}
    for field in profile:
        for key in (
            ["screen.width_px", "screen.height_px", "screen.dpi"] if field == "screen" else [field]
        ):
            column = FIELD_COLUMNS.get(key)
            fields[key] = {
                "source_urls": sources,
                "method": "CSV supplied fact; human review pending"
                if column
                else "Generator static-only policy or template metadata; not a device fact",
                "csv_file": csv_name,
                "csv_line": row["_line"],
                "csv_column": column,
            }
    evidence = {
        "profile_id": row["id"],
        "review_status": "needs-human",
        "runtime_ready": False,
        "field_evidence": fields,
        "cohort": "stage-c-generated",
        "source_record": {
            key: row.get(key)
            for key in ("source_record", "source_record_sha256", "source_dataset", "source_notes")
            if row.get(key)
        },
        "pre_2020_justification": row.get("pre_2020_justification") or None,
        "screen_inches": float(row["screen_inches"]),
        "screen_size_class": screen_class(float(row["screen_inches"])),
        "chipset_family": row["chipset_family"],
        "diversity_evidence": {
            "source_urls": sources,
            "csv_file": csv_name,
            "csv_line": row["_line"],
            "csv_columns": ["screen_inches", "chipset_family", "os_version"],
        },
        "popularity": {
            "source": row.get("popularity_source") or None,
            "rank": row.get("popularity_rank") or None,
        },
        "notes": [
            "Sources identify supplied evidence, not independent verification.",
            "dpi is supplied physical PPI; no logical density claim.",
            "Build is null and runtime eligibility is false by generator policy.",
        ],
    }
    return profile, evidence


def generate(
    csv_path,
    root=ROOT,
    output=None,
    evidence_output=None,
    templates=None,
    require_cohort=False,
    exemptions=(),
):
    root = Path(root)
    output = Path(output) if output else root / "profiles/generated"
    evidence_output = Path(evidence_output) if evidence_output else root / "data/sources"
    templates = Path(templates) if templates else root / "profiles/_templates"
    rows = read_rows(csv_path)
    if require_cohort:
        validate_cohort(rows, exemptions)
    reference_ids = {
        path.stem
        for path in (root / "profiles").rglob("*.json")
        if "_templates" not in path.parts and not path.is_relative_to(output)
    }
    if reference_ids.intersection(row["id"] for row in rows):
        raise ValueError("Generated identities collide with preserved reference/runtime profiles")
    pending = []
    for row in sorted(rows, key=lambda item: item["id"]):
        template = json.loads((templates / f"{row['brand']}.json").read_text())
        if template["brand"] != row["brand"] or template["shell_id"] != row["brand"]:
            raise ValueError("Template brand/shell identity mismatch")
        profile, evidence = prepare(row, template, Path(csv_path).name)
        pending.extend(
            [
                (output / row["brand"] / f"{row['id']}.json", encode(profile)),
                (evidence_output / f"{row['id']}.evidence.json", encode(evidence)),
            ]
        )
    existing = {path for path in output.rglob("*.json")} if output.exists() else set()
    expected = {path for path, _ in pending if path.is_relative_to(output)}
    if existing - expected:
        raise ValueError("Stale generated profiles found; reconcile explicitly before generation")
    for path, content in pending:
        write_changed(path, content)
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--evidence-output", type=Path)
    parser.add_argument("--templates", type=Path)
    parser.add_argument("--require-cohort", action="store_true")
    parser.add_argument("--exemptions", type=Path)
    args = parser.parse_args()
    exemptions = []
    if args.exemptions:
        import yaml

        loaded = yaml.safe_load(args.exemptions.read_text())
        exemptions = loaded.get("exemptions", []) if isinstance(loaded, dict) else loaded
    print(
        f"Generated {generate(args.csv, args.root, args.output, args.evidence_output, args.templates, args.require_cohort, exemptions)} static drafts"
    )
