#!/usr/bin/env python3
"""
EdweavePack Health Check and Issue Detection
Comprehensive system validation before deployment
"""

import os
import sys
import json
import subprocess
import requests
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any

class HealthChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed_checks = []
        
    def log_issue(self, category: str, message: str, severity: str = "error"):
        """Log an issue or warning"""
        item = {"category": category, "message": message, "severity": severity}
        if severity == "error":
            self.issues.append(item)
        else:
            self.warnings.append(item)
    
    def log_pass(self, category: str, message: str):
        """Log a passed check"""
        self.passed_checks.append({"category": category, "message": message})
    
    def check_file_structure(self) -> bool:
        """Check if all required files and directories exist"""
        print("🔍 Checking file structure...")
        
        required_files = [
            "backend/main.py",
            "backend/requirements.txt",
            "backend/app/__init__.py",
            "backend/app/core/database.py",
            "backend/app/models/__init__.py",
            "backend/app/api/auth.py",
            "backend/app/schemas/auth.py",
            "frontend/package.json",
            "frontend/src/App.js",
            "frontend/src/services/api.js",
            "docker-compose.yml",
            ".env.example"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_issue("File Structure", f"Missing files: {', '.join(missing_files)}")
            return False
        
        self.log_pass("File Structure", "All required files present")
        return True
    
    def check_environment_config(self) -> bool:
        """Check environment configuration"""
        print("🔍 Checking environment configuration...")
        
        # Check if .env exists
        if not Path("backend/.env").exists():
            self.log_issue("Environment", "backend/.env file missing")
            return False
        
        # Check required environment variables
        required_vars = ["SECRET_KEY", "DATABASE_URL"]
        missing_vars = []
        
        try:
            with open("backend/.env", "r") as f:
                env_content = f.read()
                for var in required_vars:
                    if f"{var}=" not in env_content:
                        missing_vars.append(var)
        except Exception as e:
            self.log_issue("Environment", f"Error reading .env file: {e}")
            return False
        
        if missing_vars:
            self.log_issue("Environment", f"Missing environment variables: {', '.join(missing_vars)}")
            return False
        
        self.log_pass("Environment", "Environment configuration valid")
        return True
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are properly installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python dependencies
        try:
            result = subprocess.run(
                ["pip", "check"], 
                cwd="backend", 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                self.log_issue("Dependencies", f"Python dependency issues: {result.stdout}")
                return False
        except Exception as e:
            self.log_issue("Dependencies", f"Error checking Python dependencies: {e}")
            return False
        
        # Check Node dependencies
        try:
            if Path("frontend/node_modules").exists():
                self.log_pass("Dependencies", "Node modules installed")
            else:
                self.log_issue("Dependencies", "Node modules not installed")
                return False
        except Exception as e:
            self.log_issue("Dependencies", f"Error checking Node dependencies: {e}")
            return False
        
        self.log_pass("Dependencies", "All dependencies properly installed")
        return True
    
    def check_database_models(self) -> bool:
        """Check database model integrity"""
        print("🔍 Checking database models...")
        
        try:
            # Import and validate models
            sys.path.append("backend")
            from app.models.user import User
            from app.models.curriculum import Curriculum, Assessment, Question
            from app.models.student import Student
            
            # Check if models have required attributes
            required_user_attrs = ["id", "email", "name", "hashed_password"]
            for attr in required_user_attrs:
                if not hasattr(User, attr):
                    self.log_issue("Database Models", f"User model missing attribute: {attr}")
                    return False
            
            self.log_pass("Database Models", "All models properly defined")
            return True
        except ImportError as e:
            self.log_issue("Database Models", f"Model import error: {e}")
            return False
        except Exception as e:
            self.log_issue("Database Models", f"Model validation error: {e}")
            return False
    
    def check_api_endpoints(self) -> bool:
        """Check if API endpoints are properly defined"""
        print("🔍 Checking API endpoints...")
        
        try:
            sys.path.append("backend")
            from main import app
            
            # Get all routes
            routes = []
            for route in app.routes:
                if hasattr(route, 'path'):
                    routes.append(route.path)
            
            required_endpoints = [
                "/api/auth/register",
                "/api/auth/token",
                "/api/auth/me",
                "/api/curriculum/",
                "/api/assessment/generate"
            ]
            
            missing_endpoints = []
            for endpoint in required_endpoints:
                if not any(endpoint in route for route in routes):
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                self.log_issue("API Endpoints", f"Missing endpoints: {', '.join(missing_endpoints)}")
                return False
            
            self.log_pass("API Endpoints", "All required endpoints defined")
            return True
        except Exception as e:
            self.log_issue("API Endpoints", f"Error checking endpoints: {e}")
            return False
    
    def check_frontend_components(self) -> bool:
        """Check frontend component integrity"""
        print("🔍 Checking frontend components...")
        
        required_components = [
            "frontend/src/pages/Login.js",
            "frontend/src/pages/Register.js",
            "frontend/src/pages/Dashboard.js",
            "frontend/src/components/Layout.js",
            "frontend/src/hooks/useAuth.js"
        ]
        
        missing_components = []
        for component in required_components:
            if not Path(component).exists():
                missing_components.append(component)
        
        if missing_components:
            self.log_issue("Frontend Components", f"Missing components: {', '.join(missing_components)}")
            return False
        
        self.log_pass("Frontend Components", "All required components present")
        return True
    
    def check_security_config(self) -> bool:
        """Check security configuration"""
        print("🔍 Checking security configuration...")
        
        issues_found = []
        
        # Check for default/weak secrets
        try:
            with open("backend/.env", "r") as f:
                env_content = f.read()
                if "your-secret-key-here" in env_content:
                    issues_found.append("Default SECRET_KEY detected")
                if "dev-secret-key" in env_content:
                    issues_found.append("Development SECRET_KEY in use")
        except:
            pass
        
        # Check CORS configuration
        try:
            with open("backend/main.py", "r") as f:
                main_content = f.read()
                if "allow_origins=[\"*\"]" in main_content:
                    issues_found.append("CORS allows all origins")
        except:
            pass
        
        if issues_found:
            for issue in issues_found:
                self.log_issue("Security", issue, "warning")
        else:
            self.log_pass("Security", "Security configuration acceptable")
        
        return len(issues_found) == 0
    
    def check_docker_config(self) -> bool:
        """Check Docker configuration"""
        print("🔍 Checking Docker configuration...")
        
        required_docker_files = [
            "docker-compose.yml",
            "backend/Dockerfile",
            "frontend/Dockerfile"
        ]
        
        missing_files = []
        for file_path in required_docker_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_issue("Docker", f"Missing Docker files: {', '.join(missing_files)}")
            return False
        
        self.log_pass("Docker", "Docker configuration files present")
        return True
    
    def run_live_tests(self) -> bool:
        """Run live API tests if server is running"""
        print("🔍 Running live API tests...")
        
        try:
            # Test health endpoint
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                self.log_pass("Live Tests", "Health endpoint responding")
            else:
                self.log_issue("Live Tests", f"Health endpoint returned {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_issue("Live Tests", "API server not running", "warning")
            return False
        except Exception as e:
            self.log_issue("Live Tests", f"Error testing API: {e}")
            return False
        
        return True
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        total_checks = len(self.issues) + len(self.warnings) + len(self.passed_checks)
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_checks": total_checks,
                "passed": len(self.passed_checks),
                "warnings": len(self.warnings),
                "errors": len(self.issues),
                "health_score": (len(self.passed_checks) / total_checks * 100) if total_checks > 0 else 0
            },
            "passed_checks": self.passed_checks,
            "warnings": self.warnings,
            "errors": self.issues,
            "deployment_ready": len(self.issues) == 0
        }\n        \n        return report\n    \n    def run_all_checks(self) -> bool:\n        \"\"\"Run all health checks\"\"\"\n        print(\"🏥 EdweavePack Health Check Starting...\")\n        print(\"=\" * 50)\n        \n        checks = [\n            self.check_file_structure,\n            self.check_environment_config,\n            self.check_dependencies,\n            self.check_database_models,\n            self.check_api_endpoints,\n            self.check_frontend_components,\n            self.check_security_config,\n            self.check_docker_config,\n            self.run_live_tests\n        ]\n        \n        for check in checks:\n            try:\n                check()\n            except Exception as e:\n                self.log_issue(\"System\", f\"Check failed: {check.__name__}: {e}\")\n        \n        return len(self.issues) == 0\n\ndef main():\n    \"\"\"Main health check runner\"\"\"\n    os.chdir(Path(__file__).parent)\n    \n    checker = HealthChecker()\n    success = checker.run_all_checks()\n    \n    report = checker.generate_report()\n    \n    # Print summary\n    print(\"\\n\" + \"=\" * 50)\n    print(\"📊 HEALTH CHECK SUMMARY\")\n    print(\"=\" * 50)\n    \n    print(f\"Health Score: {report['summary']['health_score']:.1f}%\")\n    print(f\"Passed: {report['summary']['passed']}\")\n    print(f\"Warnings: {report['summary']['warnings']}\")\n    print(f\"Errors: {report['summary']['errors']}\")\n    \n    if report['errors']:\n        print(\"\\n❌ CRITICAL ISSUES:\")\n        for error in report['errors']:\n            print(f\"  • {error['category']}: {error['message']}\")\n    \n    if report['warnings']:\n        print(\"\\n⚠️  WARNINGS:\")\n        for warning in report['warnings']:\n            print(f\"  • {warning['category']}: {warning['message']}\")\n    \n    # Save detailed report\n    with open(\"health_report.json\", \"w\") as f:\n        json.dump(report, f, indent=2)\n    \n    print(f\"\\n📄 Detailed report saved to: health_report.json\")\n    \n    if report['deployment_ready']:\n        print(\"\\n🎉 SYSTEM READY FOR DEPLOYMENT!\")\n        sys.exit(0)\n    else:\n        print(\"\\n💥 SYSTEM NOT READY - Fix critical issues before deployment\")\n        sys.exit(1)\n\nif __name__ == \"__main__\":\n    main()