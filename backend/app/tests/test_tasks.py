from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    client.post("/auth/register", json={
        "email": "task@test.com",
        "password": "12345678"
    })
    response = client.post("/auth/login", json={
        "email": "task@test.com",
        "password": "12345678"
    })
    return response.json()["access_token"]


def test_create_task():
    token = get_token()
    response = client.post(
        "/tasks/",
        json={"title": "My task"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "My task"


def test_get_tasks():
    token = get_token()
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)