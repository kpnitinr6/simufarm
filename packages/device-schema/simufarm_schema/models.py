from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Screen(Contract):
    width_px: int = Field(gt=0)
    height_px: int = Field(gt=0)
    dpi: float = Field(gt=0)


class Notch(Contract):
    type: Literal["none", "punch_hole", "notch", "teardrop", "dynamic_island"]
    position: Literal["none", "top_center", "top_left", "top_right"]


class Build(Contract):
    brand: str | None = Field(alias="ro.product.brand")
    model: str | None = Field(alias="ro.product.model")
    device: str | None = Field(alias="ro.product.device")
    fingerprint: str | None = Field(alias="ro.build.fingerprint")


class DeviceProfile(Contract):
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    release_year: int = Field(ge=1980, le=2100)
    os_family: Literal["android", "ios"]
    os_version: str = Field(min_length=1)
    shell_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    base_image_id: str | None
    screen: Screen
    notch: Notch
    ram_gb: float = Field(gt=0)
    build: Build
    source_type: Literal["api", "scraper", "manual"]
    sources: list[HttpUrl] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    verified_by: Literal["human", "gemini", "ollama"] | None
    verified_at: AwareDatetime | None

    @model_validator(mode="after")
    def review_policy(self):
        if self.source_type == "scraper" and self.confidence >= 0.9:
            raise ValueError("Scraped profiles must retain confidence below0.9")
        if (self.verified_by is None) != (self.verified_at is None):
            raise ValueError(
                "Reviewer and verification timestamp must both be present or both unknown"
            )
        return self


def is_review_approved(profile: DeviceProfile) -> bool:
    return (
        profile.verified_by == "human"
        and profile.verified_at is not None
        and (profile.source_type == "scraper" or profile.confidence >= 0.9)
    )


class Limits(Contract):
    ram_mb: int = Field(gt=0, le=32768)
    vcpu: int = Field(gt=0, le=16)


class SimulatorManifest(Contract):
    simulator_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    profile_id: str = Field(min_length=1)
    kind: Literal["static", "interactive", "runtime"]
    shell_id: str = Field(min_length=1)
    base_image_id: str | None
    status: Literal["ready", "building", "failed"]
    limits: Limits

    @model_validator(mode="after")
    def runtime_requires_base(self):
        if self.kind == "runtime" and not self.base_image_id:
            raise ValueError("Runtime manifests require a shared base image")
        return self


def validate_pair(profile: DeviceProfile, manifest: SimulatorManifest) -> None:
    if manifest.profile_id != profile.id:
        raise ValueError("Manifest/profile identity mismatch")
    if profile.os_family == "ios" and manifest.kind == "runtime":
        raise ValueError("Functional iOS emulation is prohibited")
    if not is_review_approved(profile):
        raise ValueError(
            "Human review and source-specific confidence policy required for promotion"
        )
    if manifest.shell_id != profile.shell_id:
        raise ValueError("Shell identity mismatch")
    if manifest.kind == "runtime":
        if profile.base_image_id != manifest.base_image_id:
            raise ValueError("Base image identity mismatch")
        if any(v is None or not v.strip() for v in profile.build.model_dump().values()):
            raise ValueError("Runtime build identity is unknown; static previews only")
