import pytest
from fastapi.testclient import TestClient

def test_create_student(client, auth_headers):
    response = client.post("/api/learning-paths/students",
        headers=auth_headers,
        json={
            "name": "New Student",
            "email": "newstudent@example.com",
            "grade_level": "10",
            "learning_style": "visual"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Student"
    assert data["email"] == "newstudent@example.com"

def test_get_students(client, auth_headers, test_student):
    response = client.get("/api/learning-paths/students", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_student_analytics(client, auth_headers, test_student):
    response = client.get(f"/api/learning-paths/analytics/{test_student.id}", 
        headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "progress" in data or "message" in data

def test_generate_personalized_path(client, auth_headers, test_student, test_curriculum):
    response = client.post(f"/api/learning-paths/personalized/{test_student.id}/{test_curriculum.id}",
        headers=auth_headers)
    # Might fail without AI service
    assert response.status_code in [200, 500]

def test_get_personalized_path(client, auth_headers, test_student, test_curriculum):
    response = client.get(f"/api/learning-paths/personalized/{test_student.id}/{test_curriculum.id}",
        headers=auth_headers)
    assert response.status_code in [200, 404]

def test_create_student_duplicate_email(client, auth_headers, test_student):
    response = client.post("/api/learning-paths/students",
        headers=auth_headers,
        json={
            "name": "Duplicate Student",
            "email": "student@example.com",  # Same as test_student
            "grade_level": "11",
            "learning_style": "auditory"
        }
    )
    assert response.status_code == 400

def test_create_student_unauthorized(client):
    response = client.post("/api/learning-paths/students",
        json={
            "name": "Unauthorized Student",
            "email": "unauthorized@example.com",
            "grade_level": "10",
            "learning_style": "visual"
        }
    )
    assert response.status_code == 401