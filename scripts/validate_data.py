"""Validate v3 profiles/evidence; --allow-draft permits labeled static review artifacts only."""

import argparse
import json
from pathlib import Path

from simufarm_schema import DeviceProfile, SimulatorManifest, is_review_approved, validate_pair

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT, allow_draft=False):
    profiles = {}
    for path in (root / "profiles").rglob("*.json"):
        if "_templates" in path.parts:
            continue
        p = DeviceProfile.model_validate_json(path.read_text())
        if p.id != path.stem or p.id in profiles:
            raise ValueError("Profile identity/filename mismatch or duplicate")
        if not allow_draft and not is_review_approved(p):
            raise ValueError(f"Human review required: {p.id}")
        evidence = json.loads((root / f"data/sources/{p.id}.evidence.json").read_text())
        if evidence["profile_id"] != p.id:
            raise ValueError("Evidence/profile mismatch")
        for field in p.model_dump(by_alias=True):
            if field == "screen":
                keys = ["screen.width_px", "screen.height_px", "screen.dpi"]
            else:
                keys = [field]
            for key in keys:
                item = evidence["field_evidence"][key]
                if not item.get("source_urls") or not item.get("method"):
                    raise ValueError(f"Missing field evidence: {p.id}:{key}")
                if not set(item["source_urls"]).issubset({str(url) for url in p.sources}):
                    raise ValueError(f"Evidence source absent from profile sources: {p.id}:{key}")
        if not {str(url) for url in p.build.sources}.issubset({str(url) for url in p.sources}):
            raise ValueError(f"Build provenance absent from profile sources: {p.id}")
        profiles[p.id] = p
    for path in (root / "data/manifests").glob("*.json"):
        m = SimulatorManifest.model_validate_json(path.read_text())
        p = profiles[m.profile_id]
        if m.kind == "runtime" or not allow_draft:
            validate_pair(p, m)
        elif m.shell_id != p.shell_id:
            raise ValueError("Static manifest shell mismatch")
    return len(profiles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    print(
        f"Validated {validate(allow_draft=args.allow_draft)} sourced profiles; allow_draft={args.allow_draft}"
    )
