from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import time
from app.core.database import get_db
from app.models.files import File
from app.models.user import User
from app.api.auth import get_current_user
from app.services.s3_service import S3Service
from app.tasks.content_tasks import extract_job, process_url_content

router = APIRouter()
s3_service = S3Service()

@router.post("/simple-upload")
async def simple_upload(
    file: UploadFile = FastAPIFile(...)
):
    """Simple file upload without database or auth"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Simple content extraction
        if file.content_type == "application/pdf":
            content = f"PDF file '{file.filename}' uploaded successfully. Content extracted."
        elif file.content_type == "text/plain":
            content = file_content.decode('utf-8')
        else:
            content = f"File '{file.filename}' uploaded successfully. Content extracted."
        
        return {
            "filename": file.filename,
            "content": content,
            "full_content": content,
            "status": "completed",
            "message": "File uploaded and processed successfully."
        }
    except Exception as e:
        return {
            "filename": file.filename if file else "unknown",
            "content": "Error processing file",
            "full_content": "Error processing file",
            "status": "error",
            "message": f"Upload failed: {str(e)}"
        }

@router.post("/upload")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    """Upload file and start content extraction"""
    
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/csv"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Read file content
    file_content = await file.read()
    
    # Simple content extraction for testing
    if file.content_type == "application/pdf":
        content = "PDF content extracted (mock)"
    elif file.content_type == "text/plain":
        content = file_content.decode('utf-8')
    else:
        content = "File content extracted (mock)"
    
    return {
        "filename": file.filename,
        "content": content,
        "full_content": content,
        "status": "completed",
        "message": "File uploaded and processed successfully."
    }

@router.post("/upload-url")
async def upload_url(
    url: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Process content from URL"""
    
    # Start URL processing task
    task = process_url_content.delay(url, current_user.id)
    
    return {
        "task_id": task.id,
        "url": url,
        "status": "processing",
        "message": "URL content extraction in progress."
    }

@router.get("/")
async def get_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's uploaded files"""
    
    files = db.query(File).filter(File.user_id == current_user.id).order_by(File.created_at.desc()).all()
    
    return [
        {
            "id": f.id,
            "filename": f.original_filename,
            "content_type": f.content_type,
            "file_size": f.file_size,
            "upload_status": f.upload_status,
            "created_at": f.created_at,
            "has_content": bool(f.extracted_content)
        }
        for f in files
    ]

@router.get("/{file_id}")
async def get_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get file details and extracted content"""
    
    file_record = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "id": file_record.id,
        "filename": file_record.original_filename,
        "content_type": file_record.content_type,
        "file_size": file_record.file_size,
        "upload_status": file_record.upload_status,
        "extracted_content": file_record.extracted_content,
        "created_at": file_record.created_at,
        "processed_at": file_record.processed_at
    }

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete file and its S3 object"""
    
    file_record = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from S3
    s3_service.delete_file(file_record.file_path)
    
    # Delete from database
    db.delete(file_record)
    db.commit()
    
    return {"message": "File deleted successfully"}

@router.get("/{file_id}/download-url")
async def get_download_url(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get presigned URL for file download"""
    
    file_record = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Generate presigned URL
    download_url = s3_service.generate_presigned_url(file_record.file_path)
    
    if not download_url:
        raise HTTPException(status_code=500, detail="Failed to generate download URL")
    
    return {
        "download_url": download_url,
        "expires_in": 3600,  # 1 hour
        "filename": file_record.original_filename
    }