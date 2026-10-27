from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Screen(Contract):
    width_px: int = Field(gt=0)
    height_px: int = Field(gt=0)
    dpi: float = Field(gt=0)
    aspect: str = Field(pattern=r"^\d+(?:\.\d+)?:\d+(?:\.\d+)?$")


class Body(Contract):
    width_mm: float = Field(gt=0)
    height_mm: float = Field(gt=0)
    thickness_mm: float = Field(gt=0)


class Notch(Contract):
    type: Literal["none", "punch_hole", "notch", "dynamic_island"]
    position: Literal["none", "top_center", "top_left", "top_right"]


class DeviceProfile(Contract):
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    release_year: int = Field(ge=1980, le=2100)
    os_family: Literal["android", "ios"]
    os_versions: list[str] = Field(min_length=1)
    screen: Screen
    body: Body
    notch: Notch
    buttons: list[str]
    ram_gb: float = Field(gt=0)
    storage_gb: float = Field(gt=0)
    sources: list[HttpUrl] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    verified_by: Literal["human", "gemini", "ollama"]
    verified_at: AwareDatetime


class Limits(Contract):
    ram_mb: int = Field(gt=0, le=32768)
    vcpu: int = Field(gt=0, le=16)


class SimulatorManifest(Contract):
    simulator_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    profile_id: str = Field(min_length=1)
    kind: Literal["static", "interactive", "emulator"]
    base_image_id: str | None
    shell_asset_id: str = Field(min_length=1)
    storage_ref: str = Field(pattern=r"^(?:s3|https)://.+$")
    status: Literal["ready", "building", "failed"]
    limits: Limits

    @model_validator(mode="after")
    def emulator_requires_base(self):
        if self.kind == "emulator" and not self.base_image_id:
            raise ValueError("Emulator manifests require a shared base image")
        return self


def validate_pair(profile: DeviceProfile, manifest: SimulatorManifest) -> None:
    if manifest.profile_id != profile.id:
        raise ValueError("Manifest/profile identity mismatch")
    if profile.os_family == "ios" and manifest.kind == "emulator":
        raise ValueError("Functional iOS emulation is prohibited")
    if profile.verified_by != "human" or profile.confidence < 0.9:
        raise ValueError("Human review with confidence >= 0.9 is required for promotion")
