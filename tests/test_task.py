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

def test_get_my_tasks(client):
    headers = get_auth_headers(client)
    project_id = create_project(client, headers)

    client.post("/tasks/", json={
        "title": "Test task1",
        "description": "Task1 creation for test",
        "project_id": project_id
    },headers= headers)

    response = client.get(f"/tasks/project/{project_id}", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Test task1"

def test_update_task(client):
    headers = get_auth_headers(client)
    project_id = create_project(client, headers)

    task_create_response = client.post("/tasks/", json={
        "title": "Test task1",
        "description": "Task1 creation for test",
        "project_id": project_id
    },headers= headers)

    task_id = task_create_response.json()["id"]
    
    response = client.patch(f"/tasks/{task_id}", json={
        "status": "done"
    }, headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "done"

def test_delete_task(client):
    headers = get_auth_headers(client)
    project_id = create_project(client, headers)

    task_create_response = client.post("/tasks/", json={
        "title": "Test task1",
        "description": "Task1 creation for test",
        "project_id": project_id
    },headers= headers)

    task_id = task_create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"