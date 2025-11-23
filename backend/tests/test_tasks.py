import pytest
from fastapi.testclient import TestClient

def test_get_task_status(client, auth_headers):
    # Test with non-existent task
    response = client.get("/api/tasks/status/nonexistent-task-id", headers=auth_headers)
    assert response.status_code in [200, 404]

def test_get_active_tasks(client, auth_headers):
    response = client.get("/api/tasks/active", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_cancel_task(client, auth_headers):
    # Test with non-existent task
    response = client.post("/api/tasks/cancel/nonexistent-task-id", headers=auth_headers)
    assert response.status_code in [200, 404]

def test_tasks_unauthorized(client):
    response = client.get("/api/tasks/active")
    assert response.status_code == 401