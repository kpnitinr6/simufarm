"""Reproducible secondary-source static draft import; no network or API calls."""

import argparse
import collections
import csv
import hashlib
import json
import math
import pathlib
import re
import subprocess

BRANDS = [
    "vivo",
    "samsung",
    "xiaomi",
    "oppo",
    "realme",
    "oneplus",
    "google",
    "motorola",
    "honor",
    "huawei",
    "nokia",
    "sony",
    "asus",
    "lenovo",
    "lg",
    "tecno",
    "infinix",
    "nothing",
    "zte",
    "tcl",
]
REV = "db1dea0c38ff07fcf400aa05d8c8e4393348eb25"
FIELDS = [
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
]


def canonical(name, brand):
    original = name
    name = re.sub(r"\([^)]*(?:RAM|GB)[^)]*\)", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\b\d+\s*(?:GB|TB)(?:\s*RAM)?\b", "", name, flags=re.IGNORECASE)
    name = name.replace("+", " Plus ")
    name = re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()
    name = re.sub(r"^" + brand + r"\s+", "", name)
    name = re.sub(r"\b20(?:20|21|22|23|24|25|26)\b", "", name)
    if brand in ["google", "nothing", "sony", "asus"]:
        name = re.sub(r"\b5g\b", "", name)
    if brand == "google" and name.strip() == "pixel 4a" and "5g" in original.lower():
        name = "pixel 4a 5g"
    if brand == "lenovo":
        name = name.replace("legion phone", "legion")
        name = name.replace("legion 2 pro", "legion pro 2")
    if brand == "sony":
        name = name.replace("ace 2", "ace ii")
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"\s+(\d)", r"\1", name)
    return re.sub(r"[^a-z0-9]", "", name)


def family(s):
    s = s.lower()
    for a, b in [
        ("snapdragon", "qualcomm-snapdragon"),
        ("dimensity", "mediatek-dimensity"),
        ("helio", "mediatek-helio"),
        ("tensor", "google-tensor"),
        ("exynos", "samsung-exynos"),
        ("kirin", "huawei-kirin"),
        ("unisoc", "unisoc"),
        ("spreadtrum", "unisoc"),
    ]:
        if a in s:
            return b
    return ""


def collect(root):
    out = {b: {} for b in BRANDS}
    rejected = collections.Counter()
    for b in BRANDS:
        for f in sorted((root / "data/smartphone" / b).rglob("*.json")):
            x = json.loads(f.read_text())
            d = x.get("display", {})
            raw = x.get("raw_smartprix", {})
            name = x.get("name", "")
            name = re.sub(r"\([^)]*(?:RAM|GB)[^)]*\)", "", name, flags=re.IGNORECASE).strip()
            if (
                re.search(
                    r"TD-LTE|Dual SIM|Standard Edition|Premium Edition|UW 5G|\bSM-|\b(?:Tab|Pad|Tablet)\b",
                    name,
                    re.IGNORECASE,
                )
                or len(name) > 65
            ):
                rejected["regional_or_nonphone"] += 1
                continue
            name = re.sub(r"\s+", " ", name).strip()
            if re.search(
                r"LTE-A|WiMAX|\bLM[A-Z0-9]|\bZS\d|\b(?:China|Japan|Transparent|Community Edition|Batman|Diablo|Top Edition)\b",
                name,
                re.IGNORECASE,
            ):
                rejected["regional_or_cosmetic"] += 1
                continue
            if b == "asus" and ("ROG Phone 10" in name or "ROG Phone 7 Pro" in name):
                rejected["unverified_future_or_unreleased"] += 1
                continue
            if b == "lg" and ("Dual Screen" in name or " UW" in name):
                rejected["accessory_or_carrier_variant"] += 1
                continue
            name = name.replace("Strix Edition", "Strix")
            key = canonical(name, b)
            if b == "google" and key == "pixel 5a 5g":
                key = "pixel 5a"
            os = str(x.get("os_version", ""))
            osmatch = re.search(r"Android\s*v?\s*(\d+)", str(x.get("os") or ""))
            if not os and osmatch:
                os = osmatch[1]
            year = str(x.get("release_date", ""))[:4]
            if b == "lg" and "x4plus" in key:
                rejected["known_misdated_2018_model"] += 1
                continue
            if (
                str(x.get("release_date", "")) > "2026-10-27"
                or not str(x.get("os", "")).lower().startswith("android")
                or any(
                    t in str(x.get("release_status", "")).lower()
                    for t in ["rumor", "cancel", "unannounced"]
                )
            ):
                rejected["future_nonandroid_or_unreleased"] += 1
                continue
            res = str(d.get("resolution") or "")
            m = re.search(r"(\d{3,4})\s*[x×]\s*(\d{3,4})", res)
            if not m:
                m = re.search(r"(\d{3,4})\s*[x×]\s*(\d{3,4})", str(d.get("size") or ""))
            inches = d.get("size_inch")
            im = re.search(r"(\d+(?:\.\d+)?)\s*inches", str(d.get("size") or ""))
            if not inches and im:
                inches = float(im[1])
            ram = x.get("ram_gb")
            soc = x.get("soc") or raw.get("Technical.Chipset")
            urls = x.get("source_urls", [])
            if not (
                year.isdigit()
                and 2020 <= int(year) <= 2026
                and os.isdigit()
                and m
                and inches
                and ram
                and soc
                and urls
            ):
                rejected["missing_required_or_year"] += 1
                continue
            w, h = sorted(map(int, m.groups()))
            if not (3.5 <= float(inches) <= 8 and 300 <= w <= 2500 and h >= w and float(ram) > 0):
                rejected["invalid_geometry"] += 1
                continue
            fam = family(soc)
            if not fam:
                soc = raw.get("Technical.Chipset", "")
                fam = family(soc)
            if not fam:
                rejected["unknown_chipset"] += 1
                continue
            # Prefer records with direct manufacturer citations, then terse curated records.
            secondary = any(
                any(t in u for t in ["kaggle.com", "phonedb.net", "aitoolbuzz.com"]) for u in urls
            )
            score = (
                not secondary,
                len(f.relative_to(root).parts) == 5,
                x.get("verified", False),
                -len(name),
                str(x.get("release_date")),
            )
            slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
            recordurl = (
                f"https://github.com/GetTechAPI/TechAPI/blob/{REV}/{f.relative_to(root).as_posix()}"
            )
            row = {
                "id": f"gen-{b}-{slug}",
                "brand": b,
                "model": name,
                "release_year": int(year),
                "os_version": os,
                "width_px": w,
                "height_px": h,
                "dpi": round(math.hypot(w, h) / float(inches)),
                "notch": "unknown",
                "notch_position": "unknown",
                "ram_gb": float(ram),
                "screen_inches": float(inches),
                "chipset_family": fam,
                "source_urls": json.dumps([recordurl] + urls, separators=(",", ":")),
            }
            evidence = {
                "record_path": f.relative_to(root).as_posix(),
                "record_sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                "record_url": recordurl,
                "upstream_source_urls": urls,
                "evidence_status": "secondary-source-static-draft; human review pending",
                "raw_name": x.get("name"),
                "canonical_model_key": key,
                "raw_os": x.get("os"),
                "raw_os_version": x.get("os_version"),
                "raw_display": d,
                "raw_ram_gb": ram,
                "raw_soc": soc,
                "raw_release_date": x.get("release_date"),
                "dpi_method": "round(hypot(width_px,height_px)/display_inches); physical PPI, not Android logical density",
                "notch_method": "unknown: source does not establish cutout geometry; no device fact inferred",
            }
            if key not in out[b] or score > out[b][key][0]:
                out[b][key] = (score, row, evidence)
    return out, rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", type=pathlib.Path)
    ap.add_argument("--output", type=pathlib.Path, default=pathlib.Path("data"))
    a = ap.parse_args()
    policy_path = pathlib.Path("data/cohort-policy.json")
    if (
        policy_path.exists()
        and json.loads(policy_path.read_text()).get("mode") == "distinct_no_padding"
        and a.output.resolve() == pathlib.Path("data").resolve()
    ):
        raise SystemExit(
            "C2 curated catalog: import into a separate scratch --output path; do not overwrite the authoritative remediated CSV"
        )

    observed_revision = subprocess.run(
        ["git", "-C", str(a.dataset), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if observed_revision != REV:
        raise ValueError(f"Dataset revision mismatch: expected {REV}, got {observed_revision}")
    allrows, rejected = collect(a.dataset)
    supplement = json.loads(
        pathlib.Path(__file__).with_name("nothing-primary-supplement.json").read_text()
    )
    for item in supplement:
        row = item["row"]
        allrows["nothing"][canonical(row["model"], "nothing")] = (
            (True, True, True, 0, "2026"),
            row,
            item["evidence"],
        )
    eligible = {b: len(allrows[b]) for b in BRANDS}
    quotas = {b: min(50, eligible[b]) for b in BRANDS}
    quotas["nothing"] = min(11, eligible["nothing"])
    while sum(quotas.values()) < 1000:
        choices = [b for b in BRANDS if b != "nothing" and quotas[b] < eligible[b]]
        if not choices:
            break
        for b in choices:
            if sum(quotas.values()) == 1000:
                break
            quotas[b] += 1
    selected = []
    for b in BRANDS:
        candidates = sorted(
            allrows[b].values(),
            key=lambda v: (v[1]["release_year"], v[0], v[1]["id"]),
            reverse=True,
        )
        chosen = []
        seen = [set(), set(), set()]
        # Seed factual diversity before filling with recent distinct models.
        for target, field in [(3, "os_version"), (2, "screen_inches"), (2, "chipset_family")]:
            idx = ["os_version", "screen_inches", "chipset_family"].index(field)
            for x in candidates:
                val = x[1][field]
                if field == "screen_inches":
                    val = "small" if val < 6 else "medium" if val < 6.5 else "large"
                if val not in seen[idx] and len(seen[idx]) < target:
                    if x not in chosen:
                        chosen.append(x)
                    seen[idx].add(val)
        chosen = chosen[: quotas[b]]
        for x in candidates:
            if len(chosen) >= quotas[b]:
                break
            if x not in chosen:
                chosen.append(x)
        selected.extend(chosen)
    selected.sort(key=lambda v: (BRANDS.index(v[1]["brand"]), v[1]["id"]))
    a.output.mkdir(parents=True, exist_ok=True)
    with (a.output / "devices.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(x[1] for x in selected)
    research = a.output / "research/stage-c"
    research.mkdir(parents=True, exist_ok=True)
    (research / "row-provenance.json").write_text(
        json.dumps({x[1]["id"]: x[2] for x in selected}, indent=2) + "\n"
    )
    report = {
        "dataset_revision": REV,
        "eligible_distinct_models": eligible,
        "selected_per_brand": quotas,
        "total": len(selected),
        "rejected_records": dict(rejected),
        "note": "Selection is deterministic coverage/release recency, not model popularity; market rank unknown unless separately sourced.",
    }
    (research / "import-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
