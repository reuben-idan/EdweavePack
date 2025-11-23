#!/usr/bin/env python3
"""
EdweavePack Issue Fixer
Automatically fixes common issues found during health checks
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import secrets
import string

class IssueFixer:
    def __init__(self):
        self.fixes_applied = []
        self.failed_fixes = []
    
    def log_fix(self, category: str, message: str, success: bool = True):
        """Log a fix attempt"""
        item = {"category": category, "message": message}
        if success:
            self.fixes_applied.append(item)
            print(f"✅ {category}: {message}")
        else:
            self.failed_fixes.append(item)
            print(f"❌ {category}: {message}")
    
    def fix_environment_config(self):
        """Fix environment configuration issues"""
        print("🔧 Fixing environment configuration...")
        
        # Create .env from example if missing
        backend_env = Path("backend/.env")
        backend_env_example = Path("backend/.env.example")
        
        if not backend_env.exists() and backend_env_example.exists():
            try:
                shutil.copy(backend_env_example, backend_env)
                self.log_fix("Environment", "Created .env from .env.example")
            except Exception as e:
                self.log_fix("Environment", f"Failed to create .env: {e}", False)
        
        # Generate secure SECRET_KEY if using default
        if backend_env.exists():
            try:
                with open(backend_env, "r") as f:
                    content = f.read()
                
                if "your-secret-key-here" in content or "dev-secret-key" in content:
                    # Generate secure random key
                    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
                    secure_key = ''.join(secrets.choice(alphabet) for _ in range(64))
                    
                    # Replace insecure keys
                    content = content.replace("your-secret-key-here", secure_key)
                    content = content.replace("dev-secret-key-change-in-production", secure_key)
                    
                    with open(backend_env, "w") as f:
                        f.write(content)
                    
                    self.log_fix("Environment", "Generated secure SECRET_KEY")
            except Exception as e:
                self.log_fix("Environment", f"Failed to update SECRET_KEY: {e}", False)
    
    def fix_missing_directories(self):
        """Create missing directories"""
        print("🔧 Creating missing directories...")
        
        required_dirs = [
            "backend/tests",
            "backend/app/api",
            "backend/app/core",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/services",
            "frontend/src/tests",
            "frontend/src/components",
            "frontend/src/pages",
            "frontend/src/hooks",
            "frontend/src/services"
        ]
        
        for dir_path in required_dirs:
            path = Path(dir_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.log_fix("Directories", f"Created {dir_path}")
                except Exception as e:
                    self.log_fix("Directories", f"Failed to create {dir_path}: {e}", False)
    
    def fix_missing_init_files(self):
        """Create missing __init__.py files"""
        print("🔧 Creating missing __init__.py files...")
        
        python_dirs = [
            "backend/app",
            "backend/app/api",
            "backend/app/core",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/services",
            "backend/app/tasks",
            "backend/tests"
        ]
        
        for dir_path in python_dirs:
            init_file = Path(dir_path) / "__init__.py"
            if Path(dir_path).exists() and not init_file.exists():
                try:
                    init_file.touch()
                    self.log_fix("Init Files", f"Created {init_file}")
                except Exception as e:
                    self.log_fix("Init Files", f"Failed to create {init_file}: {e}", False)
    
    def fix_cors_configuration(self):
        """Fix CORS configuration for security"""
        print("🔧 Fixing CORS configuration...")
        
        main_py = Path("backend/main.py")
        if main_py.exists():
            try:
                with open(main_py, "r") as f:
                    content = f.read()
                
                # Replace wildcard CORS with specific origins
                if 'allow_origins=["*"]' in content:
                    content = content.replace(
                        'allow_origins=["*"]',
                        'allow_origins=["http://localhost:3000", "http://localhost:3001"]'
                    )
                    
                    with open(main_py, "w") as f:
                        f.write(content)
                    
                    self.log_fix("Security", "Fixed CORS configuration")
            except Exception as e:
                self.log_fix("Security", f"Failed to fix CORS: {e}", False)
    
    def fix_database_url(self):
        """Fix database URL configuration"""
        print("🔧 Fixing database configuration...")
        
        backend_env = Path("backend/.env")
        if backend_env.exists():
            try:
                with open(backend_env, "r") as f:
                    content = f.read()
                
                # Ensure SQLite is used for development if PostgreSQL not configured
                if "DATABASE_URL=" not in content:
                    content += "\\nDATABASE_URL=sqlite:///./edweavepack.db\\n"
                    
                    with open(backend_env, "w") as f:
                        f.write(content)
                    
                    self.log_fix("Database", "Added SQLite DATABASE_URL")
            except Exception as e:
                self.log_fix("Database", f"Failed to fix database URL: {e}", False)
    
    def install_dependencies(self):
        """Install missing dependencies"""
        print("🔧 Installing dependencies...")
        
        # Install Python dependencies
        if Path("backend/requirements.txt").exists():
            try:
                result = subprocess.run(
                    ["pip", "install", "-r", "requirements.txt"],
                    cwd="backend",
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log_fix("Dependencies", "Installed Python dependencies")
                else:
                    self.log_fix("Dependencies", f"Failed to install Python deps: {result.stderr}", False)
            except Exception as e:
                self.log_fix("Dependencies", f"Error installing Python deps: {e}", False)
        
        # Install Node dependencies
        if Path("frontend/package.json").exists():
            try:
                result = subprocess.run(
                    ["npm", "install"],
                    cwd="frontend",
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log_fix("Dependencies", "Installed Node dependencies")
                else:
                    self.log_fix("Dependencies", f"Failed to install Node deps: {result.stderr}", False)
            except Exception as e:
                self.log_fix("Dependencies", f"Error installing Node deps: {e}", False)
    
    def create_missing_dockerfiles(self):
        """Create missing Dockerfile configurations"""
        print("🔧 Creating missing Docker files...")
        
        # Backend Dockerfile
        backend_dockerfile = Path("backend/Dockerfile")
        if not backend_dockerfile.exists():
            dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
            try:
                with open(backend_dockerfile, "w") as f:
                    f.write(dockerfile_content)
                self.log_fix("Docker", "Created backend Dockerfile")
            except Exception as e:
                self.log_fix("Docker", f"Failed to create backend Dockerfile: {e}", False)
        
        # Frontend Dockerfile
        frontend_dockerfile = Path("frontend/Dockerfile")
        if not frontend_dockerfile.exists():
            dockerfile_content = '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
'''
            try:
                with open(frontend_dockerfile, "w") as f:
                    f.write(dockerfile_content)
                self.log_fix("Docker", "Created frontend Dockerfile")
            except Exception as e:
                self.log_fix("Docker", f"Failed to create frontend Dockerfile: {e}", False)
    
    def fix_import_errors(self):
        """Fix common import errors"""
        print("🔧 Fixing import errors...")
        
        # Check and fix main.py imports
        main_py = Path("backend/main.py")
        if main_py.exists():
            try:
                with open(main_py, "r") as f:
                    content = f.read()
                
                # Add missing imports if needed
                fixes_needed = []
                
                if "from app.models import Base" not in content and "Base.metadata.create_all" in content:
                    fixes_needed.append("from app.models import Base")
                
                if fixes_needed:
                    # Add imports at the top
                    lines = content.split("\\n")
                    import_index = 0
                    for i, line in enumerate(lines):
                        if line.startswith("from ") or line.startswith("import "):
                            import_index = i + 1
                    
                    for fix in fixes_needed:
                        lines.insert(import_index, fix)
                        import_index += 1
                    
                    with open(main_py, "w") as f:
                        f.write("\\n".join(lines))
                    
                    self.log_fix("Imports", "Fixed missing imports in main.py")
            except Exception as e:
                self.log_fix("Imports", f"Failed to fix imports: {e}", False)
    
    def create_test_setup(self):
        """Create basic test setup files"""
        print("🔧 Setting up test configuration...")
        
        # Create pytest.ini
        pytest_ini = Path("backend/pytest.ini")
        if not pytest_ini.exists():
            content = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
'''
            try:
                with open(pytest_ini, "w") as f:
                    f.write(content)
                self.log_fix("Testing", "Created pytest.ini")
            except Exception as e:
                self.log_fix("Testing", f"Failed to create pytest.ini: {e}", False)
        
        # Create frontend test setup
        frontend_test_setup = Path("frontend/src/setupTests.js")
        if not frontend_test_setup.exists():
            content = '''import '@testing-library/jest-dom';
'''
            try:
                with open(frontend_test_setup, "w") as f:
                    f.write(content)
                self.log_fix("Testing", "Created frontend test setup")
            except Exception as e:
                self.log_fix("Testing", f"Failed to create test setup: {e}", False)
    
    def run_all_fixes(self):
        """Run all available fixes"""
        print("🔧 EdweavePack Issue Fixer Starting...")
        print("=" * 50)
        
        fixes = [
            self.fix_missing_directories,
            self.fix_missing_init_files,
            self.fix_environment_config,
            self.fix_cors_configuration,
            self.fix_database_url,
            self.fix_import_errors,
            self.create_missing_dockerfiles,
            self.create_test_setup,
            self.install_dependencies
        ]
        
        for fix in fixes:
            try:
                fix()
            except Exception as e:
                self.log_fix("System", f"Fix failed: {fix.__name__}: {e}", False)
        
        # Summary
        print("\\n" + "=" * 50)
        print("🔧 FIXES SUMMARY")
        print("=" * 50)
        print(f"Applied: {len(self.fixes_applied)}")
        print(f"Failed: {len(self.failed_fixes)}")
        
        if self.failed_fixes:
            print("\\n❌ FAILED FIXES:")
            for fix in self.failed_fixes:
                print(f"  • {fix['category']}: {fix['message']}")
        
        if self.fixes_applied:
            print("\\n✅ SUCCESSFUL FIXES:")
            for fix in self.fixes_applied:
                print(f"  • {fix['category']}: {fix['message']}")
        
        return len(self.failed_fixes) == 0

def main():
    """Main fixer runner"""
    os.chdir(Path(__file__).parent)
    
    fixer = IssueFixer()
    success = fixer.run_all_fixes()
    
    if success:
        print("\\n🎉 All fixes applied successfully!")
        print("Run health_check.py to verify the fixes.")
    else:
        print("\\n⚠️  Some fixes failed. Manual intervention may be required.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)