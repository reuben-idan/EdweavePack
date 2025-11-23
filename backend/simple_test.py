#!/usr/bin/env python3
"""
Simple test to verify basic functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from app.models.user import User
        from app.models.curriculum import Curriculum
        from app.models.student import Student
        from app.api.auth import router as auth_router
        from app.api.curriculum import router as curriculum_router
        from app.services.ai_service import AIService
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_models():
    """Test database model creation"""
    try:
        from app.core.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database models created successfully")
        return True
    except Exception as e:
        print(f"❌ Database model error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    try:
        from main import app
        print(f"✅ FastAPI app created: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def test_ai_service():
    """Test AI service functionality"""
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        # Test fallback curriculum generation
        result = ai_service._generate_fallback_curriculum("Math", "10", [])
        assert "curriculum_overview" in result
        assert "weekly_modules" in result
        print("✅ AI service working")
        return True
    except Exception as e:
        print(f"❌ AI service error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running EdweavePack Basic Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_database_models,
        test_fastapi_app,
        test_ai_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        return True
    else:
        print("💥 Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)