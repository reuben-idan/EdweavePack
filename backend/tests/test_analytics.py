import pytest
from fastapi.testclient import TestClient

def test_get_dashboard_analytics(client, auth_headers):
    response = client.get("/api/analytics/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_curricula" in data
    assert "total_students" in data
    assert "total_assessments" in data

def test_get_class_performance(client, auth_headers, test_curriculum):
    response = client.get("/api/analytics/class-performance",
        headers=auth_headers,
        params={"curriculum_id": test_curriculum.id}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_misconceptions(client, auth_headers):
    response = client.get("/api/analytics/misconceptions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_student_progress(client, auth_headers, test_student):
    response = client.get(f"/api/analytics/progress-tracking/{test_student.id}",
        headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "progress" in data or "message" in data

def test_analytics_unauthorized(client):
    response = client.get("/api/analytics/dashboard")
    assert response.status_code == 401

def test_get_nonexistent_student_progress(client, auth_headers):
    response = client.get("/api/analytics/progress-tracking/999", headers=auth_headers)
    assert response.status_code == 404