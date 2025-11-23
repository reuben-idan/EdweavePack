#!/usr/bin/env python3
"""
EdweavePack Deployment Readiness Check
Final validation before production deployment
"""

import os
import sys
import json
import subprocess
import time
import requests
from pathlib import Path
from typing import Dict, List, Any

class DeploymentChecker:
    def __init__(self):
        self.checks = []
        self.critical_failures = []
        self.warnings = []
    
    def add_check(self, name: str, status: str, message: str, critical: bool = False):
        """Add a check result"""
        check = {
            "name": name,
            "status": status,  # "pass", "fail", "warning"
            "message": message,
            "critical": critical,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.checks.append(check)
        
        if status == "fail" and critical:
            self.critical_failures.append(check)
        elif status == "warning":
            self.warnings.append(check)
    
    def check_production_config(self):
        """Check production configuration"""
        print("🔍 Checking production configuration...")
        
        # Check environment variables
        env_file = Path("backend/.env")
        if env_file.exists():
            with open(env_file, "r") as f:
                content = f.read()
                
                # Check for development values
                dev_indicators = [
                    ("SECRET_KEY", ["dev-secret", "your-secret-key-here"]),
                    ("DATABASE_URL", ["sqlite:///"]),
                    ("DEBUG", ["True", "true"])
                ]
                
                for var, bad_values in dev_indicators:
                    for bad_value in bad_values:
                        if bad_value in content:
                            self.add_check(
                                f"Production Config - {var}",
                                "fail",
                                f"Development value detected in {var}",
                                critical=True
                            )
                            return
                
                self.add_check("Production Config", "pass", "No development values detected")
        else:
            self.add_check("Production Config", "fail", ".env file missing", critical=True)
    
    def check_security_headers(self):
        """Check security configuration"""
        print("🔍 Checking security configuration...")
        
        # Check CORS settings
        main_py = Path("backend/main.py")
        if main_py.exists():
            with open(main_py, "r") as f:
                content = f.read()
                
                if 'allow_origins=["*"]' in content:
                    self.add_check(
                        "Security - CORS",
                        "fail",
                        "CORS allows all origins",
                        critical=True
                    )
                else:
                    self.add_check("Security - CORS", "pass", "CORS properly configured")
        
        # Check for HTTPS enforcement
        if "https" not in content.lower():
            self.add_check(
                "Security - HTTPS",
                "warning",
                "HTTPS enforcement not detected"
            )
    
    def check_database_migrations(self):
        """Check database migration status"""
        print("🔍 Checking database migrations...")
        
        alembic_dir = Path("backend/alembic")
        if alembic_dir.exists():
            versions_dir = alembic_dir / "versions"
            if versions_dir.exists():
                migrations = list(versions_dir.glob("*.py"))
                if migrations:
                    self.add_check(
                        "Database Migrations",
                        "pass",
                        f"Found {len(migrations)} migration files"
                    )
                else:
                    self.add_check(
                        "Database Migrations",
                        "warning",
                        "No migration files found"
                    )
            else:
                self.add_check(
                    "Database Migrations",
                    "fail",
                    "Alembic versions directory missing",
                    critical=True
                )
        else:
            self.add_check(
                "Database Migrations",
                "warning",
                "Alembic not configured"
            )
    
    def check_docker_production_config(self):
        """Check Docker production configuration"""
        print("🔍 Checking Docker production configuration...")
        
        prod_compose = Path("docker-compose.prod.yml")
        if prod_compose.exists():
            with open(prod_compose, "r") as f:
                content = f.read()
                
                # Check for production indicators
                prod_indicators = ["restart: unless-stopped", "healthcheck:", "volumes:"]
                found_indicators = sum(1 for indicator in prod_indicators if indicator in content)
                
                if found_indicators >= 2:
                    self.add_check("Docker Production", "pass", "Production Docker config found")
                else:
                    self.add_check("Docker Production", "warning", "Basic Docker config detected")
        else:
            self.add_check("Docker Production", "warning", "Production Docker compose missing")
    
    def check_monitoring_setup(self):
        """Check monitoring and logging setup"""
        print("🔍 Checking monitoring setup...")
        
        # Check for logging configuration
        logging_indicators = [
            Path("backend/logging.conf"),
            Path("backend/app/core/logging.py")
        ]
        
        logging_found = any(path.exists() for path in logging_indicators)
        
        if logging_found:
            self.add_check("Monitoring - Logging", "pass", "Logging configuration found")
        else:
            self.add_check("Monitoring - Logging", "warning", "No logging configuration detected")
        
        # Check for health check endpoints
        main_py = Path("backend/main.py")
        if main_py.exists():
            with open(main_py, "r") as f:
                content = f.read()
                if "/health" in content:
                    self.add_check("Monitoring - Health Check", "pass", "Health check endpoint found")
                else:
                    self.add_check("Monitoring - Health Check", "warning", "No health check endpoint")
    
    def check_performance_config(self):
        """Check performance configuration"""
        print("🔍 Checking performance configuration...")
        
        # Check for caching configuration
        redis_configured = False
        env_file = Path("backend/.env")
        if env_file.exists():
            with open(env_file, "r") as f:
                if "REDIS_URL" in f.read():
                    redis_configured = True
        
        if redis_configured:
            self.add_check("Performance - Caching", "pass", "Redis caching configured")
        else:
            self.add_check("Performance - Caching", "warning", "No caching configuration found")
        
        # Check for static file serving
        nginx_conf = Path("frontend/nginx.conf")
        if nginx_conf.exists():
            self.add_check("Performance - Static Files", "pass", "Nginx configuration found")
        else:
            self.add_check("Performance - Static Files", "warning", "No static file optimization")
    
    def check_backup_strategy(self):
        """Check backup and recovery strategy"""
        print("🔍 Checking backup strategy...")
        
        backup_indicators = [
            Path("scripts/backup.sh"),
            Path("scripts/backup.py"),
            Path("backup/"),
            Path("infrastructure/backup.tf")
        ]
        
        backup_found = any(path.exists() for path in backup_indicators)
        
        if backup_found:
            self.add_check("Backup Strategy", "pass", "Backup configuration found")
        else:
            self.add_check("Backup Strategy", "warning", "No backup strategy detected")
    
    def check_ssl_certificates(self):
        """Check SSL certificate configuration"""
        print("🔍 Checking SSL configuration...")
        
        ssl_indicators = [
            Path("certs/"),
            Path("ssl/"),
            Path("nginx/ssl/")
        ]
        
        ssl_found = any(path.exists() for path in ssl_indicators)
        
        # Check docker-compose for SSL configuration
        compose_files = [Path("docker-compose.yml"), Path("docker-compose.prod.yml")]
        ssl_in_compose = False
        
        for compose_file in compose_files:
            if compose_file.exists():
                with open(compose_file, "r") as f:
                    content = f.read()
                    if "443:" in content or "ssl" in content.lower():
                        ssl_in_compose = True
                        break
        
        if ssl_found or ssl_in_compose:
            self.add_check("SSL Configuration", "pass", "SSL configuration detected")
        else:
            self.add_check("SSL Configuration", "warning", "No SSL configuration found")
    
    def check_infrastructure_as_code(self):
        """Check Infrastructure as Code setup"""
        print("🔍 Checking Infrastructure as Code...")
        
        iac_files = [
            Path("infrastructure/main.tf"),
            Path("terraform/"),
            Path("cloudformation/"),
            Path("k8s/"),
            Path("kubernetes/")
        ]
        
        iac_found = any(path.exists() for path in iac_files)
        
        if iac_found:
            self.add_check("Infrastructure as Code", "pass", "IaC configuration found")
        else:
            self.add_check("Infrastructure as Code", "warning", "No IaC configuration detected")
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("🔍 Running integration tests...")
        
        try:
            # Start services for testing
            result = subprocess.run(
                ["docker-compose", "up", "-d", "postgres", "redis"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                time.sleep(10)  # Wait for services to start
                
                # Run tests
                test_result = subprocess.run(
                    ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                    cwd="backend",
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if test_result.returncode == 0:
                    self.add_check("Integration Tests", "pass", "All integration tests passed")
                else:
                    self.add_check(
                        "Integration Tests",
                        "fail",
                        "Integration tests failed",
                        critical=True
                    )
                
                # Cleanup
                subprocess.run(["docker-compose", "down"], capture_output=True)
            else:
                self.add_check("Integration Tests", "warning", "Could not start test services")
        
        except subprocess.TimeoutExpired:
            self.add_check("Integration Tests", "fail", "Tests timed out", critical=True)
        except Exception as e:
            self.add_check("Integration Tests", "warning", f"Test execution error: {e}")
    
    def check_secrets_management(self):
        """Check secrets management"""
        print("🔍 Checking secrets management...")
        
        # Check for hardcoded secrets
        sensitive_files = [
            "backend/main.py",
            "backend/app/core/database.py",
            "backend/.env"
        ]
        
        hardcoded_secrets = []
        secret_patterns = ["password=", "secret=", "key=", "token="]
        
        for file_path in sensitive_files:
            if Path(file_path).exists():
                with open(file_path, "r") as f:
                    content = f.read().lower()
                    for pattern in secret_patterns:
                        if pattern in content and "os.getenv" not in content:
                            hardcoded_secrets.append(file_path)
                            break
        
        if hardcoded_secrets:
            self.add_check(
                "Secrets Management",
                "fail",
                f"Hardcoded secrets found in: {', '.join(hardcoded_secrets)}",
                critical=True
            )
        else:
            self.add_check("Secrets Management", "pass", "No hardcoded secrets detected")
    
    def generate_deployment_report(self) -> Dict[str, Any]:
        """Generate deployment readiness report"""
        total_checks = len(self.checks)
        passed_checks = len([c for c in self.checks if c["status"] == "pass"])
        failed_checks = len([c for c in self.checks if c["status"] == "fail"])
        warning_checks = len([c for c in self.checks if c["status"] == "warning"])
        
        readiness_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        # Determine deployment readiness
        deployment_ready = len(self.critical_failures) == 0 and readiness_score >= 70
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "deployment_ready": deployment_ready,
            "readiness_score": readiness_score,
            "summary": {
                "total_checks": total_checks,
                "passed": passed_checks,
                "failed": failed_checks,
                "warnings": warning_checks,
                "critical_failures": len(self.critical_failures)
            },
            "checks": self.checks,
            "critical_failures": self.critical_failures,
            "warnings": self.warnings,
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate deployment recommendations"""
        recommendations = []
        
        if self.critical_failures:
            recommendations.append("🚨 Fix all critical failures before deployment")
        
        if len(self.warnings) > 5:
            recommendations.append("⚠️ Consider addressing warnings for better production readiness")
        
        # Specific recommendations based on checks
        check_names = [c["name"] for c in self.checks if c["status"] != "pass"]
        
        if any("SSL" in name for name in check_names):
            recommendations.append("🔒 Configure SSL/TLS certificates for production")
        
        if any("Backup" in name for name in check_names):
            recommendations.append("💾 Implement backup and disaster recovery strategy")
        
        if any("Monitoring" in name for name in check_names):
            recommendations.append("📊 Set up monitoring and alerting")
        
        if not recommendations:
            recommendations.append("🎉 System appears ready for deployment!")
        
        return recommendations
    
    def run_all_checks(self):
        """Run all deployment readiness checks"""
        print("🚀 EdweavePack Deployment Readiness Check")
        print("=" * 50)
        
        checks = [
            self.check_production_config,
            self.check_security_headers,
            self.check_database_migrations,
            self.check_docker_production_config,
            self.check_monitoring_setup,
            self.check_performance_config,
            self.check_backup_strategy,
            self.check_ssl_certificates,
            self.check_infrastructure_as_code,
            self.check_secrets_management,
            self.run_integration_tests
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.add_check(
                    f"System - {check.__name__}",
                    "fail",
                    f"Check failed: {e}",
                    critical=True
                )
        
        return self.generate_deployment_report()

def main():
    """Main deployment checker"""
    os.chdir(Path(__file__).parent)
    
    checker = DeploymentChecker()
    report = checker.run_all_checks()
    
    # Print summary
    print("\\n" + "=" * 50)
    print("🚀 DEPLOYMENT READINESS REPORT")
    print("=" * 50)
    
    print(f"Readiness Score: {report['readiness_score']:.1f}%")
    print(f"Deployment Ready: {'✅ YES' if report['deployment_ready'] else '❌ NO'}")
    
    print(f"\\nChecks Summary:")
    print(f"  Passed: {report['summary']['passed']}")
    print(f"  Failed: {report['summary']['failed']}")
    print(f"  Warnings: {report['summary']['warnings']}")
    print(f"  Critical Failures: {report['summary']['critical_failures']}")
    
    if report['critical_failures']:
        print("\\n🚨 CRITICAL FAILURES:")
        for failure in report['critical_failures']:
            print(f"  • {failure['name']}: {failure['message']}")
    
    if report['warnings']:
        print("\\n⚠️ WARNINGS:")
        for warning in report['warnings'][:5]:  # Show top 5
            print(f"  • {warning['name']}: {warning['message']}")
    
    print("\\n📋 RECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    
    # Save report
    with open("deployment_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\\n📄 Detailed report saved to: deployment_report.json")
    
    if report['deployment_ready']:
        print("\\n🎉 READY FOR DEPLOYMENT!")
        sys.exit(0)
    else:
        print("\\n⚠️ NOT READY FOR DEPLOYMENT - Address critical issues first")
        sys.exit(1)

if __name__ == "__main__":
    main()