from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.curriculum import Curriculum, LearningPath, Assessment, Question
from app.models.user import User
from app.schemas.curriculum import CurriculumCreate, CurriculumResponse, LearningPathResponse
from app.api.auth import get_current_user
from app.services.ai_service import AIService
from app.services.content_extractor import ContentExtractor
from app.services.pedagogical_templates import PedagogicalTemplate
from app.services.export_service import ExportService

router = APIRouter()
ai_service = AIService()
content_extractor = ContentExtractor()
pedagogical_templates = PedagogicalTemplate()
export_service = ExportService()

@router.post("/", response_model=CurriculumResponse)
async def create_curriculum(
    curriculum: CurriculumCreate,
    db: Session = Depends(get_db)
):
    # Generate curriculum from uploaded content
    content_preview = curriculum.source_content[:500] if curriculum.source_content else "No content provided"
    content_words = curriculum.source_content.split() if curriculum.source_content else []
    
    # Extract key topics from content (simple keyword extraction)
    key_topics = []
    if len(content_words) > 10:
        # Take every 10th word as a "key concept" for demo
        key_topics = [word.strip('.,!?') for word in content_words[::10]][:5]
    
    ai_result = {
        "weekly_modules": [
            {
                "week_number": 1,
                "title": f"Introduction: {curriculum.title}",
                "description": f"Based on uploaded materials: {content_preview}...",
                "bloom_focus": "Remember & Understand",
                "learning_outcomes": [
                    f"Understand key concepts from {curriculum.title}",
                    f"Identify main topics in the uploaded materials",
                    "Recall fundamental principles covered in the content"
                ],
                "content_blocks": [
                    {
                        "title": "Material Overview",
                        "content_type": "lecture",
                        "estimated_duration": 45,
                        "description": "Introduction based on your uploaded content",
                        "content": content_preview + "..."
                    },
                    {
                        "title": "Key Topics Identified",
                        "content_type": "reading",
                        "estimated_duration": 30,
                        "description": "Main concepts extracted from your materials",
                        "content": f"Key topics found: {', '.join(key_topics) if key_topics else 'Various concepts from uploaded content'}"
                    }
                ]
            },
            {
                "week_number": 2,
                "title": "Deep Dive into Content",
                "description": "Detailed exploration of uploaded material concepts",
                "bloom_focus": "Apply & Analyze",
                "learning_outcomes": [
                    "Apply concepts from the uploaded materials",
                    "Analyze relationships between topics in the content",
                    "Synthesize information from multiple sections"
                ],
                "content_blocks": [
                    {
                        "title": "Content Analysis",
                        "content_type": "activity",
                        "estimated_duration": 60,
                        "description": "Interactive analysis of your uploaded materials",
                        "content": f"Analyze the following content sections: {curriculum.source_content[:200] if curriculum.source_content else 'Content from uploaded files'}..."
                    },
                    {
                        "title": "Practical Applications",
                        "content_type": "discussion",
                        "estimated_duration": 45,
                        "description": "Apply concepts from your materials",
                        "content": f"Discussion topics based on: {', '.join(key_topics[:3]) if key_topics else 'uploaded content themes'}"
                    }
                ]
            }
        ],
        "learning_objectives": [
            f"Master concepts from uploaded {curriculum.subject} materials",
            "Apply knowledge extracted from your content",
            "Demonstrate understanding of material-specific topics",
            f"Connect theory from uploads to {curriculum.subject} practice"
        ]
    }
    
    # Create curriculum
    # Get first user for testing
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No users found")
    
    db_curriculum = Curriculum(
        title=curriculum.title,
        description=curriculum.description,
        subject=curriculum.subject,
        grade_level=curriculum.grade_level,
        user_id=user.id,
        source_content=curriculum.source_content,
        curriculum_metadata=ai_result
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
    db: Session = Depends(get_db)
):
    return db.query(Curriculum).all()

@router.get("/test/{curriculum_id}")
async def get_curriculum_test(
    curriculum_id: int
):
    # Mock curriculum with generated modules
    return {
        "id": curriculum_id,
        "title": "Sample Curriculum from Uploaded Content",
        "description": "Generated from your uploaded materials",
        "subject": "General Studies",
        "grade_level": "Intermediate",
        "metadata": {
            "weekly_modules": [
                {
                    "week_number": 1,
                    "title": "Introduction from Your Materials",
                    "description": "Content extracted from uploaded files",
                    "bloom_focus": "Remember & Understand",
                    "learning_outcomes": [
                        "Understand key concepts from uploaded content",
                        "Identify main topics in your materials"
                    ],
                    "content_blocks": [
                        {
                            "title": "Material Overview",
                            "content_type": "lecture",
                            "estimated_duration": 45,
                            "description": "Based on your uploaded content",
                            "content": "This module is generated from your uploaded materials and contains the key concepts identified."
                        }
                    ]
                }
            ],
            "learning_objectives": [
                "Master concepts from uploaded materials",
                "Apply knowledge from your content"
            ]
        }
    }

@router.get("/{curriculum_id}", response_model=CurriculumResponse)
async def get_curriculum(
    curriculum_id: int,
    db: Session = Depends(get_db)
):
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    return curriculum

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
    url: str = None,
    current_user: User = Depends(get_current_user)
):
    try:
        if url:
            # Extract from URL
            extracted_data = content_extractor.extract_from_url(url)
        else:
            # Extract from uploaded file
            file_content = await file.read()
            
            if file.content_type == "application/pdf":
                extracted_data = content_extractor.extract_from_pdf(file_content)
            elif file.content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                extracted_data = content_extractor.extract_from_docx(file_content)
            elif file.content_type.startswith("text/"):
                text_content = file_content.decode("utf-8")
                extracted_data = content_extractor.extract_from_text(text_content)
            else:
                # Try as text fallback
                text_content = file_content.decode("utf-8", errors="ignore")
                extracted_data = content_extractor.extract_from_text(text_content)
        
        return {
            "content": extracted_data["content"][:5000],
            "full_content": extracted_data["content"],
            "metadata": extracted_data["metadata"],
            "learning_objectives": extracted_data["learning_objectives"],
            "filename": file.filename if file else url
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Content extraction failed: {str(e)}")