import importlib.util
import json
from pathlib import Path

import pytest
from simufarm_schema import DeviceProfile, SimulatorManifest, validate_pair
from simufarm_schema.identity import validate_distinct_identities

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("render_static", ROOT / "scripts/render_static.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def test_three_stage_a_profiles_are_sourced_drafts():
    paths = list((ROOT / "profiles/vivo").glob("*.json"))
    assert {x.stem for x in paths} == {"vivo-y100", "vivo-x100", "vivo-v30"}
    for path in paths:
        p = DeviceProfile.model_validate_json(path.read_text())
        assert len(p.sources) >= 2 and p.verified_by is None and p.verified_at is None
        assert p.build.brand is None and p.build.model is None and p.build.device is None
        if p.id != "vivo-v30":
            assert p.build.fingerprint and p.build.source_type == "firmware"
        else:
            assert p.build.fingerprint is None


def test_static_generation_is_deterministic_and_idempotent(tmp_path):
    assert renderer.generate(ROOT / "profiles", tmp_path, allow_draft=True) == len(
        [p for p in (ROOT / "profiles").glob("*/*.json") if p.parent.name != "_templates"]
    )
    first = {
        str(p.relative_to(tmp_path)): (p.read_bytes(), p.stat().st_mtime_ns)
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    assert renderer.generate(ROOT / "profiles", tmp_path, allow_draft=True) == len(
        [p for p in (ROOT / "profiles").glob("*/*.json") if p.parent.name != "_templates"]
    )
    second = {
        str(p.relative_to(tmp_path)): (p.read_bytes(), p.stat().st_mtime_ns)
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    assert first == second
    assert len(list((tmp_path / "simulators").glob("*.html"))) == len(
        [p for p in (ROOT / "profiles").glob("*/*.json") if p.parent.name != "_templates"]
    )
    assert len(json.loads((tmp_path / "catalog.json").read_text())) == len(
        [p for p in (ROOT / "profiles").glob("*/*.json") if p.parent.name != "_templates"]
    )


def test_draft_rendering_requires_explicit_opt_in(tmp_path):
    with pytest.raises(ValueError, match="Human review"):
        renderer.generate(ROOT / "profiles", tmp_path)
    assert not list(tmp_path.rglob("*.html"))


def test_null_build_identity_never_enters_runtime(profile_data, manifest_data):
    profile_data["build"]["ro.build.fingerprint"] = None
    with pytest.raises(ValueError, match="unknown"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def identities():
    keys = ("container_id", "adb_serial", "android_id", "imei", "device_serial")
    return (
        {key: f"synthetic-a-{key}" for key in keys},
        {key: f"synthetic-b-{key}" for key in keys},
    )


def test_distinct_identity_evidence():
    validate_distinct_identities(*identities())


@pytest.mark.parametrize(
    "field", ["container_id", "adb_serial", "android_id", "imei", "device_serial"]
)
def test_duplicate_identity_rejected(field):
    a, b = identities()
    b[field] = a[field]
    with pytest.raises(ValueError, match="Duplicate"):
        validate_distinct_identities(a, b)


def test_absent_imei_is_unknown_not_automatically_unique():
    a, b = identities()
    b["imei"] = None
    with pytest.raises(ValueError, match="Missing"):
        validate_distinct_identities(a, b)
