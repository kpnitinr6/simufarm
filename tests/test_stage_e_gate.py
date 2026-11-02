import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("stage_e_gate", ROOT / "scripts/stage_e_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def setup(tmp_path, *, complete=False, accepted=False, profile=None):
    (tmp_path / "data").mkdir()
    (tmp_path / "data/stage-gates.json").write_text(
        json.dumps({"stage_c2": {"engineering_complete": complete, "human_accepted": accepted}})
    )
    (tmp_path / "profiles/runtime").mkdir(parents=True)
    if profile:
        (tmp_path / "profiles/runtime/fixture.json").write_text(json.dumps(profile))


def test_runtime_profile_alone_does_not_unblock_c2(tmp_path, profile_data):
    setup(tmp_path, complete=False, accepted=False, profile=profile_data)
    assert gate.assess(tmp_path)["stage_e_authorized"] is False


def test_c2_completion_without_runtime_subset_stays_blocked(tmp_path):
    setup(tmp_path, complete=True, accepted=True)
    assert gate.assess(tmp_path)["stage_e_authorized"] is False


def test_review_and_runtime_subset_are_both_required(tmp_path, profile_data):
    setup(tmp_path, complete=True, accepted=True, profile=profile_data)
    assert gate.assess(tmp_path)["stage_e_authorized"] is True
