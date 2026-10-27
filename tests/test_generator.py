"""Stage C generator safety, reproducibility, and unwaivable diversity checks."""

import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "stage_c_generator", ROOT / "scripts/generate_profiles.py"
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def row(**changes):
    value = {
        "id": "google-test",
        "brand": "google",
        "model": "Sourced test model",
        "release_year": "2023",
        "os_version": "13",
        "width_px": "1080",
        "height_px": "2400",
        "dpi": "400",
        "notch": "punch_hole",
        "notch_position": "top_center",
        "ram_gb": "8",
        "screen_inches": "6.4",
        "chipset_family": "test family",
        "source_urls": '["https://example.com/spec"]',
    }
    return value | changes


def write_csv(path, rows):
    fields = sorted(set().union(*(item.keys() for item in rows)))
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(tmp_path, rows):
    source = tmp_path / "devices.csv"
    write_csv(source, rows)
    return generator.generate(source, root=tmp_path, templates=ROOT / "profiles/_templates")


def test_generator_null_policy_evidence_and_idempotency(tmp_path):
    assert run(tmp_path, [row(build='{"ro.product.brand":"forged"}', runtime_eligible="true")]) == 1
    profile_path = tmp_path / "profiles/generated/google/google-test.json"
    profile = json.loads(profile_path.read_text())
    assert profile["build"] is None
    assert profile["runtime_eligible"] is False
    assert profile["verified_by"] is None and profile["verified_at"] is None
    assert profile["source_type"] == "scraper" and profile["confidence"] < 0.9
    evidence = json.loads((tmp_path / "data/sources/google-test.evidence.json").read_text())
    assert evidence["field_evidence"]["screen.dpi"]["csv_column"] == "dpi"
    assert evidence["field_evidence"]["build"]["csv_column"] is None
    assert evidence["field_evidence"]["model"]["csv_line"] == 2
    before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in tmp_path.rglob("*.json")}
    run(tmp_path, [row(build='{"ro.product.brand":"forged"}', runtime_eligible="true")])
    assert before == {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before}


@pytest.mark.parametrize(
    "bad",
    [
        row(id="../escape"),
        row(brand="../google"),
        row(source_urls='["file:///etc/passwd"]'),
        row(dpi="nan"),
        row(width_px="0"),
        row(model=""),
    ],
)
def test_bad_input_never_writes_partial_output(tmp_path, bad):
    with pytest.raises((ValueError, TypeError)):
        run(tmp_path, [row(id="google-good", model="First valid"), bad])
    assert not (tmp_path / "profiles").exists()
    assert not (tmp_path / "data/sources").exists()


@pytest.mark.parametrize("second", [row(), row(id="different", model=" SOURCED  TEST MODEL ")])
def test_duplicate_id_or_model_rejected(tmp_path, second):
    with pytest.raises(ValueError, match="Duplicate"):
        run(tmp_path, [row(), second])


def test_stale_generated_data_requires_explicit_reconciliation(tmp_path):
    run(tmp_path, [row()])
    with pytest.raises(ValueError, match="Stale"):
        run(tmp_path, [row(id="google-replacement", model="Replacement")])
    assert (tmp_path / "profiles/generated/google/google-test.json").exists()


def cohort_rows():
    brands = ["nothing"] + [f"brand{n}" for n in range(19)]
    rows = []
    for number, brand in enumerate(brands):
        count = 11 if brand == "nothing" else 89 if number == 1 else 50
        for index in range(count):
            rows.append(
                row(
                    id=f"{brand}-{index}",
                    brand=brand,
                    model=f"Model {index}",
                    os_version=str(12 + index % 3),
                    screen_inches="5.9" if index % 2 else "6.7",
                    chipset_family=f"family{index % 2}",
                )
            )
    return rows


def quota_exemptions():
    return [
        {
            "brand": brand,
            "constraint": "quota",
            "reason": "Approved quota redistribution",
            "global_minimum": "3 OS versions, 2 screen sizes, 2 chipset families",
        }
        for brand in ("nothing", "brand0")
    ]


def test_cohort_total_and_global_constraints_cannot_be_waived():
    rows = cohort_rows()
    assert sum(generator.validate_cohort(rows, quota_exemptions()).values()) == 1000
    with pytest.raises(ValueError, match="exactly"):
        generator.validate_cohort(rows[:-1], quota_exemptions())
    for item in rows:
        item["chipset_family"] = "same"
    with pytest.raises(ValueError, match="Mandatory global"):
        generator.validate_cohort(rows, quota_exemptions())


def test_per_brand_exemption_must_be_explicit_and_current():
    rows = cohort_rows()
    for item in rows:
        if item["brand"] == "nothing":
            item["os_version"] = "14"
    with pytest.raises(ValueError, match="nothing:os_versions"):
        generator.validate_cohort(rows, quota_exemptions())
    exemptions = quota_exemptions() + [
        {
            "brand": "nothing",
            "constraint": "os_versions",
            "reason": "Documented available-device shortage",
            "global_minimum": "3 OS versions remain globally",
        }
    ]
    assert generator.validate_cohort(rows, exemptions)["nothing"] == 11
    with pytest.raises(ValueError, match="Stale"):
        generator.validate_cohort(cohort_rows(), exemptions)
