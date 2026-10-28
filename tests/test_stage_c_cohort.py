"""Audit the real generated cohort, rather than a synthetic 1000-row fixture."""

import importlib.util
import json
from collections import Counter
from pathlib import Path

import yaml
from simufarm_schema import DeviceProfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "cohort_generator", ROOT / "scripts/generate_profiles.py"
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def test_real_cohort_matches_csv_and_explicit_static_policy():
    rows = generator.read_rows(ROOT / "data/devices.csv")
    exemptions = yaml.safe_load((ROOT / "data/devices.csv.exemptions.yaml").read_text())[
        "exemptions"
    ]
    counts = generator.validate_cohort(rows, exemptions, target_total=None, nothing_target=None)
    policy = json.loads((ROOT / "data/cohort-policy.json").read_text())
    assert sum(counts.values()) == policy["retained_candidate_count"]
    assert policy["mode"] == "distinct_no_padding"
    paths = list((ROOT / "profiles/generated").glob("*/*.json"))
    assert len(paths) == len(rows)
    observed = Counter()
    actual = {}
    for path in paths:
        raw = json.loads(path.read_text())
        assert "build" in raw and raw["build"] is None
        assert "runtime_eligible" in raw and raw["runtime_eligible"] is False
        p = DeviceProfile.model_validate(raw)
        assert p.verified_by is None and p.verified_at is None
        assert p.base_image_id is None and p.sources
        observed[p.shell_id] += 1
        actual[p.id] = p.model
    assert dict(observed) == counts
    assert actual == {row["id"]: row["model"] for row in rows}


def test_generated_artifacts_have_no_drift_or_rewrite():
    paths = list((ROOT / "profiles/generated").rglob("*.json"))
    assert paths, "Real cohort must exist"
    before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
    exemptions = yaml.safe_load((ROOT / "data/devices.csv.exemptions.yaml").read_text())[
        "exemptions"
    ]
    assert generator.generate(
        ROOT / "data/devices.csv",
        require_cohort=True,
        exemptions=exemptions,
        target_total=None,
        nothing_target=None,
    ) == len(generator.read_rows(ROOT / "data/devices.csv"))
    assert before == {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
