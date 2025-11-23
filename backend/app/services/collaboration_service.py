from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime
import uuid

class CollaborationService:
    def __init__(self):
        # In-memory storage for demo (use Redis in production)
        self.active_sessions = {}
        self.document_locks = {}
        self.change_history = {}
    
    async def create_collaboration_session(self, curriculum_id: int, user_id: int, user_name: str) -> str:
        """Create a new collaboration session"""
        session_id = str(uuid.uuid4())
        
        self.active_sessions[session_id] = {
            "curriculum_id": curriculum_id,
            "created_by": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "participants": {
                str(user_id): {
                    "name": user_name,
                    "joined_at": datetime.utcnow().isoformat(),
                    "is_active": True,
                    "cursor_position": None
                }
            },
            "document_state": {},
            "pending_changes": []
        }
        
        return session_id
    
    async def join_session(self, session_id: str, user_id: int, user_name: str) -> Dict[str, Any]:
        """Join an existing collaboration session"""
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
        
        session = self.active_sessions[session_id]
        session["participants"][str(user_id)] = {
            "name": user_name,
            "joined_at": datetime.utcnow().isoformat(),
            "is_active": True,
            "cursor_position": None
        }
        
        return {
            "session_id": session_id,
            "curriculum_id": session["curriculum_id"],
            "participants": session["participants"],
            "document_state": session["document_state"]
        }
    
    async def leave_session(self, session_id: str, user_id: int):
        """Leave a collaboration session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            if str(user_id) in session["participants"]:
                session["participants"][str(user_id)]["is_active"] = False
                session["participants"][str(user_id)]["left_at"] = datetime.utcnow().isoformat()
    
    async def apply_change(self, session_id: str, user_id: int, change: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a change to the collaborative document"""
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
        
        session = self.active_sessions[session_id]
        
        # Add change metadata
        change_with_metadata = {
            **change,
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "applied": False
        }
        
        # Check for conflicts
        conflict = await self._check_conflicts(session_id, change_with_metadata)
        
        if not conflict:
            # Apply change to document state
            await self._apply_change_to_document(session_id, change_with_metadata)
            change_with_metadata["applied"] = True
            
            # Add to history
            if session_id not in self.change_history:
                self.change_history[session_id] = []
            self.change_history[session_id].append(change_with_metadata)
        
        return {
            "change_id": change_with_metadata["id"],
            "applied": change_with_metadata["applied"],
            "conflict": conflict,
            "document_state": session["document_state"]
        }
    
    async def _check_conflicts(self, session_id: str, change: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check for conflicts with pending changes"""
        session = self.active_sessions[session_id]
        
        # Simple conflict detection based on field being edited
        field_path = change.get("field_path")
        if not field_path:
            return None
        
        # Check if another user is editing the same field
        for pending_change in session["pending_changes"]:
            if (pending_change.get("field_path") == field_path and 
                pending_change.get("user_id") != change["user_id"]):
                return {
                    "type": "concurrent_edit",
                    "conflicting_user": pending_change["user_id"],
                    "field": field_path
                }
        
        return None
    
    async def _apply_change_to_document(self, session_id: str, change: Dict[str, Any]):
        """Apply change to the document state"""
        session = self.active_sessions[session_id]
        
        change_type = change.get("type")
        field_path = change.get("field_path")
        new_value = change.get("value")
        
        if change_type == "text_edit" and field_path:
            # Navigate to the field and update value
            self._set_nested_value(session["document_state"], field_path, new_value)
        elif change_type == "add_item":
            # Add new item to array
            array_path = change.get("array_path")
            item = change.get("item")
            if array_path and item:
                array = self._get_nested_value(session["document_state"], array_path)
                if isinstance(array, list):
                    array.append(item)
        elif change_type == "remove_item":
            # Remove item from array
            array_path = change.get("array_path")
            item_index = change.get("item_index")
            if array_path and item_index is not None:
                array = self._get_nested_value(session["document_state"], array_path)
                if isinstance(array, list) and 0 <= item_index < len(array):
                    array.pop(item_index)
    
    def _get_nested_value(self, obj: Dict[str, Any], path: str) -> Any:
        """Get value from nested object using dot notation"""
        keys = path.split(".")
        current = obj
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _set_nested_value(self, obj: Dict[str, Any], path: str, value: Any):
        """Set value in nested object using dot notation"""
        keys = path.split(".")
        current = obj
        
        # Navigate to parent object
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value
        current[keys[-1]] = value
    
    async def update_cursor_position(self, session_id: str, user_id: int, position: Dict[str, Any]):
        """Update user's cursor position"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            if str(user_id) in session["participants"]:
                session["participants"][str(user_id)]["cursor_position"] = position
    
    async def get_session_state(self, session_id: str) -> Dict[str, Any]:
        """Get current session state"""
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
        
        session = self.active_sessions[session_id]
        return {
            "session_id": session_id,
            "participants": session["participants"],
            "document_state": session["document_state"],
            "active_participants": [
                p for p in session["participants"].values() 
                if p.get("is_active", False)
            ]
        }
    
    async def get_change_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get change history for a session"""
        if session_id not in self.change_history:
            return []
        
        history = self.change_history[session_id]
        return history[-limit:] if limit else history
    
    async def lock_field(self, session_id: str, user_id: int, field_path: str) -> bool:
        """Lock a field for editing"""
        lock_key = f"{session_id}:{field_path}"
        
        if lock_key in self.document_locks:
            # Field is already locked by another user
            if self.document_locks[lock_key]["user_id"] != user_id:
                return False
        
        self.document_locks[lock_key] = {
            "user_id": user_id,
            "locked_at": datetime.utcnow().isoformat(),
            "field_path": field_path
        }
        
        return True
    
    async def unlock_field(self, session_id: str, user_id: int, field_path: str):
        """Unlock a field"""
        lock_key = f"{session_id}:{field_path}"
        
        if (lock_key in self.document_locks and 
            self.document_locks[lock_key]["user_id"] == user_id):
            del self.document_locks[lock_key]
    
    async def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Clean up inactive sessions"""
        cutoff_time = datetime.utcnow().timestamp() - (max_age_hours * 3600)
        
        sessions_to_remove = []
        for session_id, session in self.active_sessions.items():
            created_at = datetime.fromisoformat(session["created_at"]).timestamp()
            
            # Check if session is old and has no active participants
            if created_at < cutoff_time:
                active_participants = [
                    p for p in session["participants"].values() 
                    if p.get("is_active", False)
                ]
                
                if not active_participants:
                    sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]
            if session_id in self.change_history:
                del self.change_history[session_id]