import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_target_proposal():
    proposal = json.loads((ROOT / "data/profiles/_targets.yaml").read_text())
    rows = proposal["targets"]
    assert len(rows) == 1000
    assert len({x["target_id"] for x in rows}) == 1000
    assert len({x["proposed_profile_id"] for x in rows}) == 1000
    assert len({(x["brand"].casefold(), x["model"].casefold()) for x in rows}) == 1000
    assert all(
        x["review_status"] == "pending" and x["source_url"].startswith("https://") for x in rows
    )
    assert proposal["approval_status"] == "pending-human"
    assert not list((ROOT / "data/profiles").glob("*.json"))
