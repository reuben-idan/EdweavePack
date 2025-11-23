#!/usr/bin/env python3
"""
EdweavePack Deployment Preparation Master Script
Comprehensive testing, fixing, and validation pipeline
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_script(script_name: str, description: str) -> bool:
    """Run a script and return success status"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], check=False)
        success = result.returncode == 0
        
        if success:
            print(f"✅ {description} - COMPLETED SUCCESSFULLY")
        else:
            print(f"❌ {description} - FAILED")
        
        return success
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False

def main():
    """Main deployment preparation pipeline"""
    print("🚀 EdweavePack Deployment Preparation Pipeline")
    print("=" * 60)
    print("This script will:")
    print("1. Fix common issues automatically")
    print("2. Run comprehensive health checks")
    print("3. Execute all tests (backend & frontend)")
    print("4. Validate deployment readiness")
    print("5. Generate final deployment report")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Pipeline steps
    steps = [
        ("fix_issues.py", "Fixing Common Issues"),
        ("health_check.py", "Running Health Checks"),
        ("run_tests.py", "Executing Test Suite"),
        ("deployment_check.py", "Validating Deployment Readiness")
    ]
    
    results = []
    start_time = time.time()
    
    for script, description in steps:
        if Path(script).exists():
            success = run_script(script, description)
            results.append((description, success))
        else:
            print(f"⚠️ Script {script} not found, skipping...")
            results.append((description, False))
    
    # Final summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 DEPLOYMENT PREPARATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Duration: {duration:.1f} seconds")
    print(f"Steps Completed: {len(results)}")
    
    all_passed = True
    for step_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{step_name}: {status}")
        if not success:
            all_passed = False
    
    print(f"\n{'='*60}")
    
    if all_passed:
        print("🎉 DEPLOYMENT PREPARATION SUCCESSFUL!")
        print("✅ All checks passed")
        print("✅ All tests passed")
        print("✅ System is ready for deployment")
        print("\nNext steps:")
        print("1. Review deployment_report.json for final details")
        print("2. Deploy using: docker-compose -f docker-compose.prod.yml up -d")
        print("3. Monitor logs and health endpoints")
        sys.exit(0)
    else:
        print("💥 DEPLOYMENT PREPARATION FAILED!")
        print("❌ Some steps failed")
        print("❌ System is NOT ready for deployment")
        print("\nRequired actions:")
        print("1. Review error messages above")
        print("2. Fix critical issues")
        print("3. Re-run this script")
        print("4. Do not deploy until all checks pass")
        sys.exit(1)

if __name__ == "__main__":
    main()