import pytest
from fastapi.testclient import TestClient
from app.models.user import User

def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "email": "newuser@example.com",
        "password": "testpassword123",
        "full_name": "New User",
        "institution": "Test School",
        "role": "teacher"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client, test_user):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Duplicate User",
        "institution": "Test School",
        "role": "teacher"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_valid_credentials(client, test_user):
    response = client.post("/api/auth/token", data={
        "username": "test@example.com",
        "password": "secret"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/api/auth/token", data={
        "username": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"

def test_get_current_user_no_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_forgot_password(client, test_user):
    response = client.post("/api/auth/forgot-password", json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert "reset link has been sent" in response.json()["message"]

def test_forgot_password_nonexistent_email(client):
    response = client.post("/api/auth/forgot-password", json={
        "email": "nonexistent@example.com"
    })
    assert response.status_code == 200  # Should not reveal if email exists

def test_update_profile(client, auth_headers):
    response = client.put("/api/auth/profile", 
        headers=auth_headers,
        json={
            "fullName": "Updated Name",
            "email": "updated@example.com",
            "institution": "Updated School"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Updated Name"
    assert data["user"]["email"] == "updated@example.com"

def test_update_password(client, auth_headers):
    response = client.put("/api/auth/password",
        headers=auth_headers,
        json={
            "current_password": "secret",
            "new_password": "newsecret123"
        }
    )
    assert response.status_code == 200
    assert "Password updated successfully" in response.json()["message"]

def test_update_password_wrong_current(client, auth_headers):
    response = client.put("/api/auth/password",
        headers=auth_headers,
        json={
            "current_password": "wrongpassword",
            "new_password": "newsecret123"
        }
    )
    assert response.status_code == 400
    assert "Current password is incorrect" in response.json()["detail"]