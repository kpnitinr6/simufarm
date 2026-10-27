from pathlib import Path

from simufarm_schema import DeviceProfile, SimulatorManifest, is_review_approved, validate_pair

root = Path(__file__).resolve().parents[1]
profiles = {}
for path in (root / "data/profiles").glob("*.json"):
    p = DeviceProfile.model_validate_json(path.read_text())
    assert p.id == path.stem, f"Profile filename mismatch: {path}"
    assert is_review_approved(p), f"Review required: {p.id}"
    assert (root / f"data/sources/{p.id}.evidence.json").exists(), f"Field evidence missing: {p.id}"
    profiles[p.id] = p
for path in (root / "data/manifests").glob("*.json"):
    m = SimulatorManifest.model_validate_json(path.read_text())
    validate_pair(profiles[m.profile_id], m)
print(f"Validated {len(profiles)} approved profiles; target proposals are not profiles.")
