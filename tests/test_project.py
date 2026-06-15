def get_auth_headers(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })

    login_response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "password123"
    })

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

def test_create_project(client):
    headers = get_auth_headers(client)

    response = client.post("/projects/", json={
        "name": "Test Project",
        "description": "Testing project creation"
    },
    headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "Testing project creation"
    assert "id" in data
    assert "owner_id" in data

def test_get_my_projects(client):
    headers = get_auth_headers(client)

    client.post("/projects/", json={
        "name": "Project 1",
        "description": "First project"
        },
        headers=headers
    )

    response = client.get("/projects/", headers= headers)

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Project 1"

def test_create_project_without_token(client):
    response = client.post("/projects/", json={
        "name": "No Token Project",
        "description": "Should fail"
    })

    assert response.status_code == 401