import json

from fastapi.testclient import TestClient
from simufarm_api.main import create_app


def test_empty_catalog(tmp_path):
    client = TestClient(create_app(tmp_path))
    assert client.get("/health/live").json()["status"] == "ok"
    assert client.get("/api/profiles").json() == []
    assert client.get("/api/profiles/missing").status_code == 404


def test_catalog_filters_unreviewed_data(tmp_path, profile_data):
    (tmp_path / "fixture.json").write_text(json.dumps(profile_data))
    client = TestClient(create_app(tmp_path))
    assert client.get("/api/profiles").json()[0]["id"] == profile_data["id"]
    assert client.get("/api/profiles/" + profile_data["id"]).status_code == 200
    profile_data["verified_by"] = "gemini"
    (tmp_path / "fixture.json").write_text(json.dumps(profile_data))
    assert client.get("/api/profiles").json() == []
    assert client.get("/api/profiles/" + profile_data["id"]).status_code == 404
