from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import io
from app.core.database import get_db
from app.models.curriculum import Curriculum
from app.models.user import User
from app.api.auth import get_current_user
from app.services.ai_service import AIService
from app.services.pedagogical_templates import PedagogicalTemplate
from app.services.export_service import ExportService

router = APIRouter()
ai_service = AIService()
pedagogical_templates = PedagogicalTemplate()
export_service = ExportService()

@router.post("/{curriculum_id}/adapt-level")
async def adapt_curriculum_level(
    curriculum_id: int,
    target_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adapt curriculum for different education levels"""
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Adapt curriculum using pedagogical templates
    adapted_data = pedagogical_templates.adapt_curriculum_for_level(
        curriculum.metadata, target_level
    )
    
    # Create new adapted curriculum
    new_curriculum = Curriculum(
        title=f"{curriculum.title} - {target_level} Adapted",
        description=f"Adapted for {target_level} level",
        subject=curriculum.subject,
        grade_level=target_level,
        user_id=current_user.id,
        source_content=curriculum.source_content,
        metadata=adapted_data
    )
    
    db.add(new_curriculum)
    db.commit()
    db.refresh(new_curriculum)
    
    return {
        "original_curriculum_id": curriculum_id,
        "adapted_curriculum_id": new_curriculum.id,
        "target_level": target_level,
        "adaptations_made": {
            "duration_adjustments": "Adjusted for age-appropriate attention spans",
            "activity_modifications": "Activities matched to developmental level",
            "assessment_changes": "Assessment types appropriate for level"
        }
    }

@router.post("/{curriculum_id}/generate-project")
async def generate_scaffolded_project(
    curriculum_id: int,
    project_topic: str,
    education_level: str = Query(..., description="K-2, 3-5, 6-8, 9-12, or University"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate scaffolded project-based assignment with rubrics"""
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Generate scaffolded project
    project_data = pedagogical_templates.generate_scaffolded_project(
        curriculum.subject, education_level, project_topic
    )
    
    return {
        "curriculum_id": curriculum_id,
        "project_data": project_data,
        "education_level": education_level,
        "subject": curriculum.subject
    }

@router.get("/{curriculum_id}/export/pdf")
async def export_curriculum_pdf(
    curriculum_id: int,
    format_type: str = Query("detailed", description="detailed or summary"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export curriculum as PDF lesson plan"""
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Generate PDF
    pdf_content = export_service.export_lesson_plan_pdf(curriculum.metadata, format_type)
    
    # Create filename
    filename = f"{curriculum.title.replace(' ', '_')}_lesson_plan.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/{curriculum_id}/export/docx")
async def export_curriculum_docx(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export curriculum as DOCX lesson plan"""
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Generate DOCX
    docx_content = export_service.export_lesson_plan_docx(curriculum.metadata)
    
    # Create filename
    filename = f"{curriculum.title.replace(' ', '_')}_lesson_plan.docx"
    
    return StreamingResponse(
        io.BytesIO(docx_content),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/{curriculum_id}/share")
async def create_shareable_link(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate shareable link for curriculum"""
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Generate shareable link
    shareable_link = export_service.generate_shareable_link(curriculum_id, current_user.id)
    
    return {
        "curriculum_id": curriculum_id,
        "shareable_link": shareable_link,
        "expires_in": "30 days",
        "permissions": "view_only"
    }

@router.get("/templates/levels")
async def get_education_levels():
    """Get available education levels and their characteristics"""
    
    levels = {}
    for level in ["K-2", "3-5", "6-8", "9-12", "University"]:
        template = pedagogical_templates.get_template(level)
        levels[level] = {
            "duration_range": f"{template['learning_duration']['min']}-{template['learning_duration']['max']} minutes",
            "assessment_types": template["assessment_types"],
            "bloom_focus": template["bloom_focus"],
            "instruction_style": template["instruction_style"]
        }
    
    return {
        "available_levels": levels,
        "description": "Education levels with pedagogical adaptations"
    }

@router.post("/project/{project_id}/export-rubric")
async def export_project_rubric(
    project_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Export project rubric as PDF"""
    
    # Generate rubric PDF
    pdf_content = export_service.export_project_rubric(project_data)
    
    # Create filename
    filename = f"{project_data.get('title', 'project').replace(' ', '_')}_rubric.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )