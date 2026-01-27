import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    email = f"test_{uuid.uuid4()}@test.com"

    response = client.post("/auth/register", json={
        "email": email,
        "password": "12345678"
    })

    assert response.status_code == 200
    data = response.json()
    assert "id" in data or "email" in data

def test_login_user():

    email = f"test_{uuid.uuid4()}@test.com"
    password = "12345678"

    reg = client.post("/auth/register", json={"email": email, "password": password})
    assert reg.status_code == 200

    response = client.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") in ("bearer", "Bearer")