def test_get_current_user(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    login_response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password123"
    })

    token = login_response.json()["access_token"]

    response = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["role"] == "user"

def test_get_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401



