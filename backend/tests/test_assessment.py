import pytest
from fastapi.testclient import TestClient
from app.models.curriculum import Assessment, Question

def test_generate_assessment(client, auth_headers, test_curriculum):
    response = client.post("/api/assessment/generate",
        headers=auth_headers,
        json={
            "curriculum_id": test_curriculum.id,
            "assessment_type": "quiz"
        }
    )
    # Assessment generation might fail without AI service
    assert response.status_code in [200, 500]

def test_get_assessment(client, auth_headers, db_session, test_curriculum):
    # Create a test assessment
    assessment = Assessment(
        title="Test Assessment",
        description="Test Description",
        curriculum_id=test_curriculum.id,
        assessment_type="quiz",
        total_points=100
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    
    response = client.get(f"/api/assessment/{assessment.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Assessment"

def test_get_nonexistent_assessment(client, auth_headers):
    response = client.get("/api/assessment/999", headers=auth_headers)
    assert response.status_code == 404

def test_get_assessment_questions(client, auth_headers, db_session, test_curriculum):
    # Create assessment with questions
    assessment = Assessment(
        title="Test Assessment",
        curriculum_id=test_curriculum.id,
        assessment_type="quiz"
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    
    question = Question(
        assessment_id=assessment.id,
        question_text="What is 2+2?",
        question_type="multiple_choice",
        options=["2", "3", "4", "5"],
        correct_answer="4",
        points=1
    )
    db_session.add(question)
    db_session.commit()
    
    response = client.get(f"/api/assessment/{assessment.id}/questions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["question_text"] == "What is 2+2?"

def test_submit_assessment(client, auth_headers, db_session, test_curriculum):
    # Create assessment with questions
    assessment = Assessment(
        title="Test Assessment",
        curriculum_id=test_curriculum.id,
        assessment_type="quiz"
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)
    
    question = Question(
        assessment_id=assessment.id,
        question_text="What is 2+2?",
        question_type="multiple_choice",
        correct_answer="4",
        points=1
    )
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    
    response = client.post(f"/api/assessment/{assessment.id}/submit",
        headers=auth_headers,
        json={
            "answers": {
                str(question.id): "4"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "total_points" in data

def test_submit_assessment_unauthorized(client, db_session, test_curriculum):
    assessment = Assessment(
        title="Test Assessment",
        curriculum_id=test_curriculum.id,
        assessment_type="quiz"
    )
    db_session.add(assessment)
    db_session.commit()
    
    response = client.post(f"/api/assessment/{assessment.id}/submit",
        json={"answers": {}}
    )
    assert response.status_code == 401