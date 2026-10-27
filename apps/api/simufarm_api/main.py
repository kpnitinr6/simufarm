import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from simufarm_schema import DeviceProfile

DEFAULT_PROFILES = Path(__file__).resolve().parents[3] / "data" / "profiles"


def create_app(profile_dir: Path | None = None) -> FastAPI:
    app = FastAPI(title="SimuFarm", version="0.1.0")
    directory = profile_dir or Path(os.getenv("PROFILE_DIR", str(DEFAULT_PROFILES)))

    def approved():
        profiles = []
        for path in sorted(directory.glob("*.json")):
            profile = DeviceProfile.model_validate_json(path.read_text())
            if profile.verified_by == "human" and profile.confidence >= 0.9:
                profiles.append(profile)
        return profiles

    @app.get("/health/live")
    def health():
        return {"status": "ok", "phase": "bootstrap"}

    @app.get("/api/profiles", response_model=list[DeviceProfile])
    def profiles():
        return approved()

    @app.get("/api/profiles/{profile_id}", response_model=DeviceProfile)
    def profile(profile_id: str):
        for value in approved():
            if value.id == profile_id:
                return value
        raise HTTPException(404, "Approved profile not found")

    return app


app = create_app()
