"""Stage E stays blocked until C2 review and a real human-reviewed runtime subset."""

import json
from pathlib import Path

from simufarm_schema import DeviceProfile, is_review_approved

ROOT = Path(__file__).resolve().parents[1]


def assess(root=ROOT):
    root = Path(root)
    state = json.loads((root / "data/stage-gates.json").read_text())
    runtime_ids = set()
    for path in (root / "profiles").rglob("*.json"):
        if "_templates" in path.parts:
            continue
        profile = DeviceProfile.model_validate_json(path.read_text())
        if profile.runtime_eligible and is_review_approved(profile):
            runtime_ids.add(profile.id)
    c2_complete = state["stage_c2"]["engineering_complete"] and state["stage_c2"]["human_accepted"]
    return {
        "stage_c2_complete": bool(c2_complete),
        "human_reviewed_runtime_profiles": len(runtime_ids),
        "stage_e_authorized": bool(c2_complete and runtime_ids),
    }


if __name__ == "__main__":
    result = assess()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["stage_e_authorized"] else 1)
