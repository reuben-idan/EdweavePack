import sys
sys.path.append('.')

from app.core.database import engine, Base, get_db
from app.models.user import User
from app.schemas.auth import UserCreate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import traceback

def test_registration():
    print("Testing registration...")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Tables created/verified")
        
        # Get database session
        db = next(get_db())
        
        # Test data
        user_data = UserCreate(
            email="z@gmail.com",
            password="lkjlkjlkjkljl.22",
            full_name="Hagar",
            institution="Legon",
            role="teacher"
        )
        
        print(f"User data: {user_data}")
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            print(f"User already exists: {existing_user.email}")
            # Delete for test
            db.delete(existing_user)
            db.commit()
            print("Deleted existing user")
        
        # Hash password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        def get_password_hash(password):
            if len(password.encode('utf-8')) > 72:
                password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(password)
        
        hashed_password = get_password_hash(user_data.password)
        print("Password hashed successfully")
        
        # Create user
        db_user = User(
            email=user_data.email.strip().lower(),
            name=user_data.full_name.strip(),
            hashed_password=hashed_password,
            institution=user_data.institution.strip() if user_data.institution else "Not specified",
            role=user_data.role,
            is_active=True
        )
        
        print(f"Creating user: {db_user.email}")
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"SUCCESS: User created with ID {db_user.id}")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_registration()