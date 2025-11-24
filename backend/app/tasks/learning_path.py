from celery import Celery
from app.database import SessionLocal
from app.models.user import User
from app.agents.learning_path_agent import LearningPathAgent

celery_app = Celery('edweave')

@celery_app.task
def generate_learning_path(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.metadata:
            return
        
        agent = LearningPathAgent()
        learning_path = agent.generate_path(
            goals=user.metadata.get('goals', {}),
            subjects=user.metadata.get('subjects', []),
            availability=user.metadata.get('availability', {}),
            materials=user.metadata.get('uploads', [])
        )
        
        # Store generated path in user metadata
        metadata = user.metadata
        metadata['learning_path'] = learning_path
        user.metadata = metadata
        db.commit()
        
    finally:
        db.close()