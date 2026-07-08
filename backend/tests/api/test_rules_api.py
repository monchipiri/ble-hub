from fastapi.testclient import TestClient

from app.main import app


def test_delete_rule_removes_rule():
    with TestClient(app) as client:
        create_response = client.post(
            "/rules",
            json={
                "name": "Temporary rule",
                "enabled": True,
                "conditions": {"rssi_gt": -70},
                "actions": [{"type": "alert", "params": {"message": "near"}}],
            },
        )
        rule_id = create_response.json()["id"]

        delete_response = client.delete(f"/rules/{rule_id}")
        list_response = client.get("/rules")

    assert create_response.status_code == 200
    assert delete_response.status_code == 204
    assert list_response.json() == []


def test_delete_unknown_rule_returns_404():
    with TestClient(app) as client:
        response = client.delete("/rules/999")

    assert response.status_code == 404
