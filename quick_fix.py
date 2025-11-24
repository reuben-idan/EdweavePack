#!/usr/bin/env python3

import subprocess
import json

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def update_frontend_config():
    """Update frontend to use correct API URL"""
    
    # Get current ECS task definition
    success, stdout, _ = run_command("aws ecs describe-services --cluster edweavepack-cluster --services edweavepack-service --region eu-north-1")
    
    if not success:
        print("ERROR: Could not get ECS service info")
        return False
    
    try:
        data = json.loads(stdout)
        task_def_arn = data['services'][0]['taskDefinition']
        
        # Get task definition details
        success, stdout, _ = run_command(f"aws ecs describe-task-definition --task-definition {task_def_arn} --region eu-north-1")
        
        if not success:
            print("ERROR: Could not get task definition")
            return False
        
        task_def = json.loads(stdout)['taskDefinition']
        
        # Update frontend container environment
        for container in task_def['containerDefinitions']:
            if container['name'] == 'frontend':
                # Add or update REACT_APP_API_URL
                env_vars = container.get('environment', [])
                
                # Remove existing REACT_APP_API_URL if present
                env_vars = [env for env in env_vars if env['name'] != 'REACT_APP_API_URL']
                
                # Add new API URL
                env_vars.append({
                    'name': 'REACT_APP_API_URL',
                    'value': 'http://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com'
                })
                
                container['environment'] = env_vars
        
        # Remove fields that can't be updated
        for field in ['taskDefinitionArn', 'revision', 'status', 'requiresAttributes', 'placementConstraints', 'compatibilities', 'registeredAt', 'registeredBy']:
            task_def.pop(field, None)
        
        # Register new task definition
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(task_def, f, indent=2)
            temp_file = f.name
        
        success, stdout, stderr = run_command(f"aws ecs register-task-definition --cli-input-json file://{temp_file} --region eu-north-1")
        
        if not success:
            print(f"ERROR: Could not register task definition: {stderr}")
            return False
        
        # Update service to use new task definition
        success, _, _ = run_command("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment --region eu-north-1")
        
        if success:
            print("SUCCESS: Service updated with correct API URL")
            return True
        else:
            print("ERROR: Could not update service")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    update_frontend_config()