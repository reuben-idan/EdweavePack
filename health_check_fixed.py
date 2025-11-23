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
            "backend/app/core/database.py",
            "backend/app/models/__init__.py",
            "backend/app/api/auth.py",
            "backend/app/schemas/auth.py",
            "frontend/package.json",
            "frontend/src/App.js",
            "frontend/src/services/api.js",
            "docker-compose.yml"
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
            self.log_issue("Environment", "backend/.env file missing", "warning")
            return True  # Not critical for development
        
        self.log_pass("Environment", "Environment configuration found")
        return True
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are properly installed"""
        print("🔍 Checking dependencies...")
        
        # Check if requirements.txt exists
        if not Path("backend/requirements.txt").exists():
            self.log_issue("Dependencies", "requirements.txt missing")
            return False
        
        # Check if package.json exists
        if not Path("frontend/package.json").exists():
            self.log_issue("Dependencies", "package.json missing")
            return False
        
        self.log_pass("Dependencies", "Dependency files present")
        return True
    
    def check_database_models(self) -> bool:
        """Check database model integrity"""
        print("🔍 Checking database models...")
        
        model_files = [
            "backend/app/models/user.py",
            "backend/app/models/curriculum.py",
            "backend/app/models/student.py"
        ]
        
        missing_models = []
        for model_file in model_files:
            if not Path(model_file).exists():
                missing_models.append(model_file)
        
        if missing_models:
            self.log_issue("Database Models", f"Missing model files: {', '.join(missing_models)}")
            return False
        
        self.log_pass("Database Models", "All model files present")
        return True
    
    def check_api_endpoints(self) -> bool:
        """Check if API endpoints are properly defined"""
        print("🔍 Checking API endpoints...")
        
        api_files = [
            "backend/app/api/auth.py",
            "backend/app/api/curriculum.py",
            "backend/app/api/assessment.py"
        ]
        
        missing_apis = []
        for api_file in api_files:
            if not Path(api_file).exists():
                missing_apis.append(api_file)
        
        if missing_apis:
            self.log_issue("API Endpoints", f"Missing API files: {', '.join(missing_apis)}")
            return False
        
        self.log_pass("API Endpoints", "All API files present")
        return True
    
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
    
    def check_docker_config(self) -> bool:
        """Check Docker configuration"""
        print("🔍 Checking Docker configuration...")
        
        if not Path("docker-compose.yml").exists():
            self.log_issue("Docker", "docker-compose.yml missing")
            return False
        
        self.log_pass("Docker", "Docker configuration present")
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
        }
        
        return report
    
    def run_all_checks(self) -> bool:
        """Run all health checks"""
        print("🏥 EdweavePack Health Check Starting...")
        print("=" * 50)
        
        checks = [
            self.check_file_structure,
            self.check_environment_config,
            self.check_dependencies,
            self.check_database_models,
            self.check_api_endpoints,
            self.check_frontend_components,
            self.check_docker_config
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.log_issue("System", f"Check failed: {check.__name__}: {e}")
        
        return len(self.issues) == 0

def main():
    """Main health check runner"""
    os.chdir(Path(__file__).parent)
    
    checker = HealthChecker()
    success = checker.run_all_checks()
    
    report = checker.generate_report()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    print(f"Health Score: {report['summary']['health_score']:.1f}%")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Warnings: {report['summary']['warnings']}")
    print(f"Errors: {report['summary']['errors']}")
    
    if report['errors']:
        print("\n❌ CRITICAL ISSUES:")
        for error in report['errors']:
            print(f"  • {error['category']}: {error['message']}")
    
    if report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in report['warnings']:
            print(f"  • {warning['category']}: {warning['message']}")
    
    # Save detailed report
    with open("health_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: health_report.json")
    
    if report['deployment_ready']:
        print("\n🎉 SYSTEM READY FOR DEPLOYMENT!")
        sys.exit(0)
    else:
        print("\n💥 SYSTEM NOT READY - Fix critical issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()