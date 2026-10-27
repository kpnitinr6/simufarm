import pytest


@pytest.fixture
def profile_data():
    # Deliberately fictional test fixture. Never stored under data/profiles.
    return {
        "id": "synthetic-test-device",
        "brand": "Synthetic Fixture",
        "model": "Test Device",
        "release_year": 2024,
        "os_family": "android",
        "os_versions": ["14"],
        "screen": {"width_px": 1000, "height_px": 2000, "dpi": 400, "aspect": "2:1"},
        "body": {"width_mm": 70, "height_mm": 140, "thickness_mm": 8},
        "notch": {"type": "none", "position": "none"},
        "buttons": [],
        "ram_gb": 4,
        "storage_gb": 64,
        "sources": ["https://example.org/test-fixture"],
        "source_type": "manual",
        "confidence": 1,
        "verified_by": "human",
        "verified_at": "2026-10-27T00:00:00Z",
    }


@pytest.fixture
def manifest_data():
    return {
        "simulator_id": "synthetic-test-device-android14",
        "profile_id": "synthetic-test-device",
        "kind": "emulator",
        "base_image_id": "shared-android14",
        "shell_asset_id": "generic-css",
        "storage_ref": "s3://simufarm/test",
        "status": "building",
        "limits": {"ram_mb": 4096, "vcpu": 2},
    }
