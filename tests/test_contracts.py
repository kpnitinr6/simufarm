import pytest
from pydantic import ValidationError
from simufarm_schema import DeviceProfile, SimulatorManifest, validate_pair


def test_valid_pair(profile_data, manifest_data):
    validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


@pytest.mark.parametrize(
    "mutation",
    [
        {"sources": []},
        {"sources": ["file:///private/spec"]},
        {"confidence": 1.1},
        {"verified_by": "codex"},
        {"verified_at": "2026-10-27T00:00:00"},
        {"surprise": "field"},
    ],
)
def test_bad_profile_rejected(profile_data, mutation):
    profile_data.update(mutation)
    with pytest.raises(ValidationError):
        DeviceProfile(**profile_data)


def test_dimensions_positive(profile_data):
    profile_data["screen"]["width_px"] = 0
    with pytest.raises(ValidationError):
        DeviceProfile(**profile_data)


def test_ios_emulator_prohibited(profile_data, manifest_data):
    profile_data["os_family"] = "ios"
    with pytest.raises(ValueError, match="iOS"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


@pytest.mark.parametrize("kind", ["static", "interactive"])
def test_ios_visual_allowed(profile_data, manifest_data, kind):
    profile_data["os_family"] = "ios"
    manifest_data.update(kind=kind, base_image_id=None)
    validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_emulator_requires_base(manifest_data):
    manifest_data["base_image_id"] = None
    with pytest.raises(ValidationError):
        SimulatorManifest(**manifest_data)


@pytest.mark.parametrize("mutation", [{"verified_by": "gemini"}, {"confidence": 0.89}])
def test_unapproved_pair_rejected(profile_data, manifest_data, mutation):
    profile_data.update(mutation)
    with pytest.raises(ValueError, match="Human review"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_identity_mismatch(profile_data, manifest_data):
    manifest_data["profile_id"] = "different"
    with pytest.raises(ValueError, match="identity"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_resource_limits(manifest_data):
    manifest_data["limits"]["vcpu"] = 100
    with pytest.raises(ValidationError):
        SimulatorManifest(**manifest_data)
