import importlib.util
from pathlib import Path

import pytest
from pydantic import ValidationError
from simufarm_schema import DeviceProfile, SimulatorManifest, validate_pair

spec = importlib.util.spec_from_file_location(
    "zero_spend_check", Path(__file__).resolve().parents[1] / "scripts/zero_spend_check.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_source_type_required(profile_data):
    profile_data.pop("source_type")
    with pytest.raises(ValidationError):
        DeviceProfile(**profile_data)


@pytest.mark.parametrize("source", ["api", "manual"])
def test_non_scraped_low_confidence_still_needs_review(profile_data, manifest_data, source):
    profile_data.update(source_type=source, confidence=0.8)
    with pytest.raises(ValueError, match="Human review"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_scraper_retains_low_confidence_after_human_review(profile_data, manifest_data):
    profile_data.update(source_type="scraper", confidence=0.8)
    validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))
    profile_data["verified_by"] = "ollama"
    with pytest.raises(ValueError, match="Human review"):
        validate_pair(DeviceProfile(**profile_data), SimulatorManifest(**manifest_data))


def test_scraper_cannot_claim_high_confidence(profile_data):
    profile_data.update(source_type="scraper", confidence=0.9)
    with pytest.raises(ValidationError):
        DeviceProfile(**profile_data)


@pytest.mark.parametrize(
    "check",
    [
        {},
        {"will_create_bill": False, "execution_class": "cloud_resource", "passed": True},
        {"will_create_bill": "unknown", "execution_class": "local_only", "passed": True},
    ],
)
def test_unknown_external_cost_blocks(check):
    result = module.assess({"id": "test", "zero_spend_check": check})
    assert result["allowed_local_preparation"] is False
    assert result["external_execution_authorized"] is False


def test_local_preparation_does_not_authorize_external_work():
    result = module.assess(
        {
            "id": "test",
            "zero_spend_check": {
                "will_create_bill": False,
                "execution_class": "local_only",
                "passed": True,
            },
        }
    )
    assert result["allowed_local_preparation"] is True
    assert result["external_execution_authorized"] is False
