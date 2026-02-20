from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_user(name: str = "Aman") -> str:
    response = client.post("/register", json={"name": name})
    assert response.status_code == 200
    return response.json()["token"]


def test_register_and_task_flow():
    token = register_user()

    tasks_response = client.get("/tasks")
    assert tasks_response.status_code == 200
    tasks = tasks_response.json()["tasks"]
    assert len(tasks) >= 1

    complete_response = client.post(
        f"/tasks/{tasks[0]['id']}/complete", json={"token": token}
    )
    assert complete_response.status_code == 200
    assert complete_response.json()["wallet"] == tasks[0]["reward"]

    wallet_response = client.post("/wallet", json={"token": token})
    assert wallet_response.status_code == 200
    assert wallet_response.json()["wallet"] == tasks[0]["reward"]


def test_prevent_duplicate_task_completion():
    token = register_user("Riya")
    task_id = 1

    first = client.post(f"/tasks/{task_id}/complete", json={"token": token})
    assert first.status_code == 200

    second = client.post(f"/tasks/{task_id}/complete", json={"token": token})
    assert second.status_code == 400
    assert "already completed" in second.json()["detail"]


def test_withdraw_flow():
    token = register_user("Neha")

    client.post("/tasks/2/complete", json={"token": token})
    withdraw = client.post(
        "/withdraw", json={"token": token, "amount": 10, "upi_id": "neha@upi"}
    )

    assert withdraw.status_code == 200
    assert withdraw.json()["wallet"] == 10
