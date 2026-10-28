"""Explicit, logged removal of superseded generated artifacts; references are untouched."""

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "profiles_generator", ROOT / "scripts/generate_profiles.py"
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


def reconcile(root=ROOT, *, apply=False):
    root = Path(root)
    rows = generator.read_rows(root / "data/devices.csv")
    ids = {row["id"] for row in rows}
    log = json.loads((root / "data/research/stage-c2/change-log.json").read_text())
    removed = {
        item["profile_id"] for item in log["changes"] if item["action"] in ("remove", "merge")
    }
    if removed & ids or len(rows) != log["after_count"] or len(removed) != log["removed_count"]:
        raise ValueError("Remediation log disagrees with actual retained/removed CSV identities")
    # Validate every retained payload before deleting any artifact.
    for row in rows:
        template = json.loads((root / "profiles/_templates" / f"{row['brand']}.json").read_text())
        generator.prepare(row, template, "devices.csv")
    paths = []
    for id in sorted(removed):
        if not id.startswith("gen-") or not generator.SAFE_ID.fullmatch(id):
            raise ValueError("Only generated IDs may be reconciled")
        paths += list((root / "profiles/generated").glob(f"*/{id}.json"))
        paths += [
            root / f"data/sources/{id}.evidence.json",
            root / f"apps/web/public/profiles/{id}.json",
            root / f"apps/web/public/simulators/{id}.html",
        ]
    existing = [p for p in paths if p.is_file()]
    if apply:
        for path in existing:
            path.unlink()
    return {"removed_ids": len(removed), "artifacts_found": len(existing), "applied": apply}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(reconcile(apply=args.apply), indent=2))
