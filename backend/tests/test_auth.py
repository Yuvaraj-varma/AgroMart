import uuid


def test_signup_success(client):
    unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    res = client.post("/api/auth/signup", json={
        "name": "Test User",
        "email": unique_email,
        "password": "password123",
        "role": "buyer"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == unique_email
    assert data["role"] == "buyer"


def test_signup_duplicate_email(client):
    unique_email = f"dup_{uuid.uuid4().hex[:8]}@test.com"
    payload = {"name": "User", "email": unique_email, "password": "pass123", "role": "buyer"}
    client.post("/api/auth/signup", json=payload)
    res = client.post("/api/auth/signup", json=payload)
    assert res.status_code == 400
    assert "already registered" in res.json()["detail"]


def test_signup_invalid_role(client):
    res = client.post("/api/auth/signup", json={
        "name": "User",
        "email": "role@test.com",
        "password": "pass123",
        "role": "admin"
    })
    assert res.status_code == 422


def test_signup_short_password(client):
    res = client.post("/api/auth/signup", json={
        "name": "User",
        "email": "short@test.com",
        "password": "123",
        "role": "buyer"
    })
    assert res.status_code == 422


def test_signup_short_name(client):
    res = client.post("/api/auth/signup", json={
        "name": "A",
        "email": "name@test.com",
        "password": "pass123",
        "role": "buyer"
    })
    assert res.status_code == 422


def test_login_invalid_credentials(client):
    res = client.post("/api/auth/login", data={
        "username": "notexist@test.com",
        "password": "wrongpass"
    })
    assert res.status_code == 401
