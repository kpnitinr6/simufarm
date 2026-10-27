import pytest
from pydantic import ValidationError
from simufarm_schema import DeviceProfile, SimulatorManifest, validate_pair


def test_asserted_build_requires_primary_provenance(profile_data):
    profile_data["build"].pop("sources")
    with pytest.raises(ValidationError, match="provenance|source_type"):
        DeviceProfile(**profile_data)


def test_source_classification_is_constrained(profile_data):
    profile_data["build"]["source_type"] = "model_guess"
    with pytest.raises(ValidationError):
        DeviceProfile(**profile_data)


def test_partial_sourced_identity_remains_static_only(profile_data, manifest_data):
    profile_data["build"]["ro.product.device"] = None
    with pytest.raises(ValueError, match="unknown"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_complete_sourced_reviewed_identity_can_pass_contract(profile_data, manifest_data):
    validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))
