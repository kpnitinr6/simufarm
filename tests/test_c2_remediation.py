import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rejected_and_merged_records_are_absent_from_active_artifacts():
    log = json.loads((ROOT / "data/research/stage-c2/change-log.json").read_text())
    rows = list(csv.DictReader((ROOT / "data/devices.csv").open()))
    ids = {row["id"] for row in rows}
    removed = {c["profile_id"] for c in log["changes"] if c["action"] in ("merge", "remove")}
    assert len(rows) == log["after_count"]
    assert len(removed) == log["removed_count"]
    assert not (removed & ids)
    for id in removed:
        assert not list((ROOT / "profiles/generated").glob(f"*/{id}.json"))
        assert not (ROOT / f"data/sources/{id}.evidence.json").exists()
        assert not (ROOT / f"apps/web/public/profiles/{id}.json").exists()
        assert not (ROOT / f"apps/web/public/simulators/{id}.html").exists()


def test_ram_is_float_in_every_current_profile():
    for path in (ROOT / "profiles").rglob("*.json"):
        if "_templates" in path.parts:
            continue
        assert type(json.loads(path.read_text())["ram_gb"]) is float


def test_primary_corrections_and_conflicts_remain_visible():
    rows = {r["id"]: r for r in csv.DictReader((ROOT / "data/devices.csv").open())}
    assert rows["gen-sony-xperia1iv"]["ram_gb"] == "12.0"
    assert rows["gen-samsung-galaxym445g"]["release_year"] == "2023"
    assert rows["gen-samsung-galaxys25fe"]["os_version"] == "16"
    assert "gen-samsung-galaxya53s5g" not in rows
    assert "Android **16**" in (ROOT / "data/research/stage-c2/SOURCE_CONFLICTS.md").read_text()


def test_geometry_coverage_is_100_sourced_rows_without_claimed_popularity():
    rows = {r["id"]: r for r in csv.DictReader((ROOT / "data/devices.csv").open())}
    packet = json.loads((ROOT / "data/research/stage-c2/notch-candidates.json").read_text())
    assert len(packet["records"]) == 100
    complete = {
        id for id, r in rows.items() if r["notch"] != "unknown" and r["notch_position"] != "unknown"
    }
    assert complete == {r["id"] for r in packet["records"]}
    for record in packet["records"]:
        row = rows[record["id"]]
        assert row["notch"] == record["notch"] and row["notch_position"] == record["notch_position"]
        assert record["sources"] and record["method"]
        assert record["rank"] is None and record["rank_source"] is None
        assert set(record["sources"]) <= set(json.loads(row["source_urls"]))
