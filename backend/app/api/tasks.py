from fastapi import APIRouter, Depends, HTTPException
from app.core.celery_app import celery_app
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/status/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get status of a Celery task"""
    
    task_result = celery_app.AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task_result.state,
            'progress': 0,
            'status': 'Task is waiting to be processed'
        }
    elif task_result.state == 'PROGRESS':
        response = {
            'task_id': task_id,
            'state': task_result.state,
            'progress': task_result.info.get('progress', 0),
            'status': task_result.info.get('status', 'Processing...')
        }
    elif task_result.state == 'SUCCESS':
        response = {
            'task_id': task_id,
            'state': task_result.state,
            'progress': 100,
            'result': task_result.result
        }
    else:  # FAILURE
        response = {
            'task_id': task_id,
            'state': task_result.state,
            'progress': 0,
            'error': str(task_result.info)
        }
    
    return response

@router.post("/cancel/{task_id}")
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Cancel a running task"""
    
    celery_app.control.revoke(task_id, terminate=True)
    
    return {
        'task_id': task_id,
        'status': 'cancelled'
    }

@router.get("/active")
async def get_active_tasks(
    current_user: User = Depends(get_current_user)
):
    """Get list of active tasks"""
    
    inspect = celery_app.control.inspect()
    active_tasks = inspect.active()
    
    if not active_tasks:
        return {"active_tasks": []}
    
    # Flatten tasks from all workers
    all_tasks = []
    for worker, tasks in active_tasks.items():
        for task in tasks:
            all_tasks.append({
                'task_id': task['id'],
                'name': task['name'],
                'worker': worker,
                'args': task.get('args', []),
                'kwargs': task.get('kwargs', {})
            })
    
    return {"active_tasks": all_tasks}