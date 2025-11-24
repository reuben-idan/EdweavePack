import sys
sys.path.append('.')
import os
import shutil

def fix_registration():
    print("Fixing registration issue...")
    
    # Backup existing database
    if os.path.exists("edweavepack.db"):
        shutil.copy("edweavepack.db", "edweavepack.db.backup")
        print("Database backed up")
    
    # Remove existing database to start fresh
    if os.path.exists("edweavepack.db"):
        os.remove("edweavepack.db")
        print("Old database removed")
    
    # Create fresh database
    from app.core.database import engine, Base
    from app.models import User
    
    print("Creating fresh database...")
    Base.metadata.create_all(bind=engine)
    print("Fresh database created")
    
    # Test registration
    from app.core.database import get_db
    from app.schemas.auth import UserCreate
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def get_password_hash(password):
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)
    
    db = next(get_db())
    
    try:
        # Test user data
        user_data = UserCreate(
            email="z@gmail.com",
            password="lkjlkjlkjkljl.22",
            full_name="Hagar",
            institution="Legon",
            role="teacher"
        )
        
        # Create user
        db_user = User(
            email=user_data.email.lower(),
            name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            institution=user_data.institution or "Not specified",
            role=user_data.role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"SUCCESS: Test user created with ID {db_user.id}")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    fix_registration()