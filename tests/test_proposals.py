import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "docs/archive/pre-v3/proposals" / name).read_text())


def test_popularity_proposal_has_no_inherited_extraction_approval():
    proposal = load("popularity-targets.yaml")
    rows = proposal["targets"]
    assert len(rows) == 500
    assert len({x["target_id"] for x in rows}) == 500
    assert sum(x["proposed_top100"] for x in rows) == 100
    assert all(
        x["model_reach_percent"] is None and x["spec_extraction_authorized"] is False for x in rows
    )
    pilot = load("android-top100-pilot.yaml")
    assert pilot["approval_status"] == "pending-human"
    assert pilot["spec_extraction_authorized"] is False
    assert pilot["targets"] == [x for x in rows if x["proposed_top100"]]


def test_apple_scope_is_visual_only_and_unapproved():
    proposal = load("ios-visual-targets.yaml")
    rows = proposal["targets"]
    assert len(rows) == 55
    assert len({x["id"] for x in rows}) == 55
    assert proposal["approved"] is False
    assert proposal["spec_extraction_authorized"] is False
    assert all(x["scope"] == "visual-only" and x["popularity_rank"] is None for x in rows)
