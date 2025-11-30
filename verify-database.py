#!/usr/bin/env python3
"""Verify database setup and data"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def verify_database():
    """Verify database tables and data"""
    
    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)
    
    try:
        # Create engine and session
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        print("🔍 Verifying database setup...")
        
        # Check if tables exist
        tables_query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = db.execute(tables_query).fetchall()
        table_names = [row[0] for row in tables]
        
        print(f"📊 Found {len(table_names)} tables:")
        for table in table_names:
            print(f"   - {table}")
        
        # Verify required tables exist
        required_tables = ['users', 'curricula', 'assessments']
        missing_tables = [t for t in required_tables if t not in table_names]
        
        if missing_tables:
            print(f"❌ Missing required tables: {missing_tables}")
            return False
        
        print("✅ All required tables exist")
        
        # Count records in key tables
        counts = {}
        for table in required_tables:
            count_query = text(f"SELECT COUNT(*) FROM {table}")
            count = db.execute(count_query).scalar()
            counts[table] = count
            print(f"📈 {table}: {count} records")
        
        # Verify minimum data requirements
        if counts['users'] == 0:
            print("❌ No users found - seed data may not have been loaded")
            return False
        
        if counts['curricula'] == 0:
            print("❌ No curricula found - seed data may not have been loaded")
            return False
        
        print("✅ Database verification successful")
        
        # Sample data queries
        print("\n🔍 Sample data verification:")
        
        # Sample users
        users_query = text("SELECT id, email, name, role FROM users LIMIT 3")
        users = db.execute(users_query).fetchall()
        print("👥 Sample users:")
        for user in users:
            print(f"   ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}")
        
        # Sample curricula
        curricula_query = text("SELECT id, title, subject, grade_level FROM curricula LIMIT 3")
        curricula = db.execute(curricula_query).fetchall()
        print("📚 Sample curricula:")
        for curriculum in curricula:
            print(f"   ID: {curriculum[0]}, Title: {curriculum[1]}, Subject: {curriculum[2]}, Grade: {curriculum[3]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False
    finally:
        db.close()

def main():
    """Main verification function"""
    print("EdweavePack Database Verification")
    print("=" * 40)
    
    success = verify_database()
    
    if success:
        print("\n🎉 Database verification completed successfully!")
        print("✅ Ready for application deployment")
    else:
        print("\n❌ Database verification failed")
        print("🔧 Run migrations and seed data before proceeding")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)