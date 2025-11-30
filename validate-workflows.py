#!/usr/bin/env python3
"""
Validate GitHub Actions workflow YAML files
"""

import yaml
import os
from pathlib import Path

def validate_yaml_file(file_path):
    """Validate YAML syntax and structure"""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Basic validation
        required_keys = ['name', 'on', 'jobs']
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            return False, f"Missing required keys: {missing_keys}"
        
        # Validate jobs structure
        if not isinstance(data['jobs'], dict):
            return False, "Jobs must be a dictionary"
        
        for job_name, job_config in data['jobs'].items():
            if 'runs-on' not in job_config:
                return False, f"Job '{job_name}' missing 'runs-on'"
            
            if 'steps' not in job_config:
                return False, f"Job '{job_name}' missing 'steps'"
        
        return True, "Valid YAML structure"
        
    except yaml.YAMLError as e:
        return False, f"YAML syntax error: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"

def main():
    """Main validation function"""
    
    print("GitHub Actions Workflow Validation")
    print("=" * 40)
    
    workflow_dir = Path(".github/workflows")
    
    if not workflow_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    all_valid = True
    
    for workflow_file in workflow_files:
        print(f"\nValidating {workflow_file.name}...")
        
        is_valid, message = validate_yaml_file(workflow_file)
        
        if is_valid:
            print(f"VALID {workflow_file.name}: {message}")
        else:
            print(f"ERROR {workflow_file.name}: {message}")
            all_valid = False
    
    # Check for required workflows
    required_workflows = ['build-and-test.yml', 'deploy.yml']
    existing_workflows = [f.name for f in workflow_files]
    
    print(f"\nRequired Workflows Check:")
    for required in required_workflows:
        if required in existing_workflows:
            print(f"FOUND {required}: Found")
        else:
            print(f"MISSING {required}: Missing")
            all_valid = False
    
    # Summary
    print(f"\nValidation Summary:")
    print(f"Total workflows: {len(workflow_files)}")
    print(f"Status: {'All Valid' if all_valid else 'Issues Found'}")
    
    return all_valid

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)