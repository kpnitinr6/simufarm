import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = {
    "vivo",
    "samsung",
    "xiaomi",
    "oppo",
    "realme",
    "oneplus",
    "google",
    "motorola",
    "honor",
    "huawei",
    "nokia",
    "sony",
    "asus",
    "lenovo",
    "lg",
    "tecno",
    "infinix",
    "nothing",
    "zte",
    "tcl",
}


def test_twenty_original_shells_and_templates():
    assert {p.name for p in (ROOT / "shells").iterdir() if p.is_dir()} == BRANDS
    assert {p.stem for p in (ROOT / "profiles/_templates").glob("*.json")} == BRANDS
    signatures = set()
    for brand in BRANDS:
        folder = ROOT / "shells" / brand
        assert all(
            (folder / f).is_file() for f in ("shell.html", "shell.css", "shell.js", "meta.json")
        )
        signatures.add((folder / "shell.css").read_text())
        template = json.loads((ROOT / "profiles/_templates" / f"{brand}.json").read_text())
        assert template["brand"] == template["shell_id"] == brand
        assert template["build"] is None and template["runtime_eligible"] is False and template["verified_by"] is None
        assert "{{" in template["model"]
    assert len(signatures) == 20


def test_reference_cohort_has_one_profile_per_brand():
    cohort = json.loads((ROOT / "data/stage-b-cohort.json").read_text())
    profiles = {
        p.stem: json.loads(p.read_text())
        for p in (ROOT / "profiles").glob("*/*.json")
        if p.parent.name != "_templates"
    }
    assert len(cohort["profile_ids"]) == 20
    assert {profiles[id]["shell_id"] for id in cohort["profile_ids"]} == BRANDS
    assert len(profiles) == 22
    assert {"vivo-y100", "vivo-v30"} <= profiles.keys()
