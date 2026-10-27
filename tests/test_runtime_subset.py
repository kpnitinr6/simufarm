import pytest
from pydantic import ValidationError
from simufarm_schema import DeviceProfile, SimulatorManifest, validate_pair


@pytest.mark.parametrize("source_type", ["third_party_device_db", "firmware_dump"])
def test_extended_build_source_types(profile_data, source_type):
    profile_data["build"]["source_type"] = source_type
    assert DeviceProfile(**profile_data).build.source_type == source_type


def test_null_build_is_static_only(profile_data, manifest_data):
    profile_data.update(build=None, runtime_eligible=False)
    p = DeviceProfile(**profile_data)
    assert p.model_dump()["build"] is None
    with pytest.raises(ValueError, match="unknown"):
        validate_pair(p, SimulatorManifest(**manifest_data))


def test_null_cannot_be_tagged_runtime_eligible(profile_data):
    profile_data["build"] = None
    with pytest.raises(ValidationError, match="unknown"):
        DeviceProfile(**profile_data)


def test_complete_identity_still_needs_explicit_promotion(profile_data, manifest_data):
    profile_data["runtime_eligible"] = False
    with pytest.raises(ValueError, match="explicitly human-promoted"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_runtime_tag_does_not_bypass_human_review(profile_data):
    profile_data.update(verified_by=None, verified_at=None)
    with pytest.raises(ValidationError, match="Human review"):
        DeviceProfile(**profile_data)
