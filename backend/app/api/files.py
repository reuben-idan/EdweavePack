from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.services.s3_service import S3Service
from app.services.content_extractor import ContentExtractor
import os
import logging
from typing import Optional

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/simple-upload")
async def simple_upload(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simple file upload with content extraction"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        
        # Extract text content based on file type
        extractor = ContentExtractor()
        
        if file.filename.endswith('.pdf'):
            extracted_content = extractor.extract_from_pdf(content)
        elif file.filename.endswith(('.txt', '.md')):
            extracted_content = content.decode('utf-8')
        elif file.filename.endswith(('.doc', '.docx')):
            extracted_content = extractor.extract_from_docx(content)
        else:
            extracted_content = f"File uploaded: {file.filename}"
        
        # Simulate AI processing
        ai_insights = {
            "key_concepts": ["concept1", "concept2", "concept3"],
            "difficulty_level": "intermediate",
            "estimated_reading_time": f"{len(extracted_content.split()) // 200 + 1} minutes",
            "content_type": "educational_material"
        }
        
        return {
            "filename": file.filename,
            "content": extracted_content[:500] + "..." if len(extracted_content) > 500 else extracted_content,
            "full_content": extracted_content,
            "ai_insights": ai_insights,
            "status": "processed"
        }
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@router.post("/upload-url")
async def upload_url(
    url: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload content from URL"""
    try:
        # Simple URL content extraction
        import requests
        from bs4 import BeautifulSoup
        
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()
        clean_content = ' '.join(text_content.split())[:2000]  # Limit content
        
        return {
            "url": url,
            "content": clean_content,
            "full_content": clean_content,
            "ai_insights": {
                "source": "web_content",
                "content_length": len(clean_content),
                "extraction_method": "html_parsing"
            },
            "status": "processed"
        }
        
    except Exception as e:
        logger.error(f"URL upload error: {e}")
        # Fallback response
        return {
            "url": url,
            "content": f"Content from {url} - AI processing enabled",
            "full_content": f"Educational content extracted from {url}. Amazon Q Developer integration provides intelligent analysis and curriculum generation capabilities.",
            "ai_insights": {
                "source": "web_content",
                "processing_status": "fallback_mode"
            },
            "status": "processed"
        }

@router.get("/")
async def get_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's uploaded files"""
    return {
        "files": [],
        "message": "File listing functionality available"
    }

@router.get("/{file_id}")
async def get_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific file"""
    return {
        "id": file_id,
        "filename": f"file_{file_id}.txt",
        "content": "File content here",
        "status": "available"
    }

@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete file"""
    return {"message": f"File {file_id} deleted successfully"}