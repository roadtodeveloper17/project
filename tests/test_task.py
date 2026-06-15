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

    return {"Authorization": f"Bearer {token}"}

def create_project(client, headers):
    response = client.post("/projects/", json={
        "name": "Test Project",
        "description": "Project for task tests"
    }, headers= headers)
    return response.json()["id"]

def test_create_task(client):
    headers = get_auth_headers(client)
    project_id = create_project(client, headers)

    response = client.post("/tasks/", json={
        "title": "Test task1",
        "description": "Task1 creation for test",
        "project_id": project_id
    }, headers= headers)

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test task1"
    assert data["description"] == "Task1 creation for test"
    assert data["project_id"] == project_id
    assert data["status"] == "todo"
