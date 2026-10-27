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
        "os_version": "14",
        "shell_id": "synthetic-shell",
        "base_image_id": "shared-android14",
        "build": {
            "ro.product.brand": "Synthetic",
            "ro.product.model": "Fixture",
            "ro.product.device": "fixture",
            "ro.build.fingerprint": "synthetic/test-only",
            "source_type": "firmware",
            "sources": ["https://example.org/test-fixture"],
        },
        "screen": {"width_px": 1000, "height_px": 2000, "dpi": 400},
        "notch": {"type": "none", "position": "none"},
        "ram_gb": 4,
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
        "kind": "runtime",
        "base_image_id": "shared-android14",
        "shell_id": "synthetic-shell",
        "status": "building",
        "limits": {"ram_mb": 4096, "vcpu": 2},
    }
