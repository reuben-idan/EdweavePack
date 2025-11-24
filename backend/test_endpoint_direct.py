#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.auth import register
from app.schemas.auth import UserCreate
from app.core.database import get_db
import asyncio

async def test_endpoint_direct():
    """Test the registration endpoint function directly"""
    print("=== Testing Registration Endpoint Direct ===")
    
    try:
        # Create test data
        user_data = UserCreate(
            email="testuser@example.com",
            full_name="Test User",
            password="testpassword123",
            institution="Test Institution",
            role="teacher"
        )
        
        print(f"User data: {user_data}")
        
        # Get database session
        db = next(get_db())
        
        # Call the registration function directly
        print("Calling registration function...")
        result = await register(user_data, db)
        
        print(f"Registration result: {result}")
        print("OK Registration endpoint test PASSED")
        
    except Exception as e:
        print(f"ERROR Registration endpoint failed: {e}")
        import traceback
        print(traceback.format_exc())
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    asyncio.run(test_endpoint_direct())