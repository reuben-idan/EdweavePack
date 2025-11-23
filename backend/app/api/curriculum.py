from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.curriculum import Curriculum, LearningPath, Assessment, Question
from app.models.user import User
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, LearningPathResponse
from app.api.auth import get_current_user
from app.services.ai_service import AIService
import PyPDF2
import io

router = APIRouter()
ai_service = AIService()

@router.post("/", response_model=CurriculumResponse)
async def create_curriculum(
    curriculum: CurriculumCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate AI curriculum
    ai_result = await ai_service.generate_curriculum(
        curriculum.source_content,
        curriculum.subject,
        curriculum.grade_level
    )
    
    # Create curriculum
    db_curriculum = Curriculum(
        title=curriculum.title,
        description=curriculum.description,
        subject=curriculum.subject,
        grade_level=curriculum.grade_level,
        user_id=current_user.id,
        source_content=curriculum.source_content,
        metadata=ai_result
    )
    db.add(db_curriculum)
    db.commit()
    db.refresh(db_curriculum)
    
    # Create learning paths
    for i, path_data in enumerate(ai_result.get("learning_paths", [])):
        learning_path = LearningPath(
            title=path_data["title"],
            description=path_data["description"],
            curriculum_id=db_curriculum.id,
            sequence_order=i + 1,
            content=path_data,
            estimated_duration=path_data.get("estimated_duration", 60)
        )
        db.add(learning_path)
    
    # Create assessments
    for assessment_data in ai_result.get("assessments", []):
        assessment = Assessment(
            title=assessment_data["title"],
            description=f"Auto-generated {assessment_data['type']}",
            curriculum_id=db_curriculum.id,
            assessment_type=assessment_data["type"],
            total_points=len(assessment_data.get("questions", [])) * 10
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        # Create questions
        for q_data in assessment_data.get("questions", []):
            question = Question(
                assessment_id=assessment.id,
                question_text=q_data["question"],
                question_type=q_data["type"],
                options=q_data.get("options"),
                correct_answer=q_data.get("correct_answer"),
                points=10
            )
            db.add(question)
    
    db.commit()
    return db_curriculum

@router.get("/", response_model=List[CurriculumResponse])
async def get_curricula(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Curriculum).filter(Curriculum.user_id == current_user.id).all()

@router.get("/{curriculum_id}/learning-paths", response_model=List[LearningPathResponse])
async def get_learning_paths(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    return db.query(LearningPath).filter(
        LearningPath.curriculum_id == curriculum_id
    ).order_by(LearningPath.sequence_order).all()

@router.post("/upload")
async def upload_content(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    content = ""
    
    if file.content_type == "application/pdf":
        pdf_content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        for page in pdf_reader.pages:
            content += page.extract_text()
    else:
        content = (await file.read()).decode("utf-8")
    
    return {"content": content[:5000], "filename": file.filename}