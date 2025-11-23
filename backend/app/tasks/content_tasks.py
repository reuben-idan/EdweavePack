from celery import current_task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.files import File
from app.services.content_extractor import ContentExtractor
from app.services.s3_service import S3Service
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def extract_job(self, file_id: int):
    """Extract content from uploaded file"""
    db = SessionLocal()
    
    try:
        # Update task status
        current_task.update_state(state='PROGRESS', meta={'progress': 10})
        
        # Get file record
        file_record = db.query(File).filter(File.id == file_id).first()
        if not file_record:
            raise Exception(f"File {file_id} not found")
        
        file_record.upload_status = "processing"
        db.commit()
        
        current_task.update_state(state='PROGRESS', meta={'progress': 30})
        
        # Download file from S3
        s3_service = S3Service()
        file_content = s3_service.download_file(file_record.file_path)
        
        current_task.update_state(state='PROGRESS', meta={'progress': 50})
        
        # Extract content based on file type
        content_extractor = ContentExtractor()
        
        if file_record.content_type == "application/pdf":
            extracted_data = content_extractor.extract_from_pdf(file_content)
        elif file_record.content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            extracted_data = content_extractor.extract_from_docx(file_content)
        else:
            # Try as text
            text_content = file_content.decode("utf-8", errors="ignore")
            extracted_data = content_extractor.extract_from_text(text_content)
        
        current_task.update_state(state='PROGRESS', meta={'progress': 80})
        
        # Update file record with extracted content
        file_record.extracted_content = extracted_data["content"]
        file_record.upload_status = "completed"
        db.commit()
        
        current_task.update_state(state='PROGRESS', meta={'progress': 100})
        
        return {
            "file_id": file_id,
            "status": "completed",
            "content_length": len(extracted_data["content"]),
            "learning_objectives": extracted_data.get("learning_objectives", [])
        }
        
    except Exception as e:
        logger.error(f"Content extraction failed for file {file_id}: {str(e)}")
        
        # Update file status to failed
        if 'file_record' in locals():
            file_record.upload_status = "failed"
            db.commit()
        
        raise Exception(f"Content extraction failed: {str(e)}")
        
    finally:
        db.close()

@celery_app.task(bind=True)
def process_url_content(self, url: str, user_id: int):
    """Extract content from URL"""
    db = SessionLocal()
    
    try:
        current_task.update_state(state='PROGRESS', meta={'progress': 20})
        
        content_extractor = ContentExtractor()
        extracted_data = content_extractor.extract_from_url(url)
        
        current_task.update_state(state='PROGRESS', meta={'progress': 80})
        
        # Create file record for URL content
        file_record = File(
            filename=f"url_content_{int(time.time())}.txt",
            original_filename=url,
            file_path=f"url_content/{user_id}/{int(time.time())}.txt",
            file_size=len(extracted_data["content"]),
            content_type="text/plain",
            upload_status="completed",
            extracted_content=extracted_data["content"],
            user_id=user_id
        )
        
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        return {
            "file_id": file_record.id,
            "status": "completed",
            "content": extracted_data["content"][:1000],  # First 1000 chars
            "learning_objectives": extracted_data.get("learning_objectives", [])
        }
        
    except Exception as e:
        logger.error(f"URL content extraction failed for {url}: {str(e)}")
        raise Exception(f"URL processing failed: {str(e)}")
        
    finally:
        db.close()