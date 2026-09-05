
"""
Real Audit Log System
"""

from datetime import datetime
from typing import Dict, List, Optional
import json
import os
from pathlib import Path

class AuditLogger:
    """Real Audit Logger with file storage"""
    
    def __init__(self, log_file: str = "audit_logs.json"):
        self.log_file = log_file
        self.logs = []
        self._load_logs()
    
    def _load_logs(self):
        """Load logs from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.logs = json.load(f)
            except:
                self.logs = []
        else:
            self.logs = []
    
    def _save_logs(self):
        """Save logs to file"""
        try:
            # Keep only last 1000 logs
            if len(self.logs) > 1000:
                self.logs = self.logs[-1000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(self.logs, f, indent=2)
        except Exception as e:
            print(f"Error saving logs: {e}")
    
    def log(self, action: str, user: str, resource: str, details: str = "", 
            ip: str = "127.0.0.1", status: str = "success"):
        """Log an action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'user': user,
            'resource': resource,
            'details': details,
            'ip': ip,
            'status': status,
            'id': len(self.logs) + 1
        }
        self.logs.append(log_entry)
        self._save_logs()
        return log_entry
    
    def get_logs(self, limit: int = 100, user: Optional[str] = None, 
                 action: Optional[str] = None) -> List[Dict]:
        """Get logs with filters"""
        logs = self.logs
        
        if user:
            logs = [l for l in logs if l.get('user') == user]
        
        if action:
            logs = [l for l in logs if l.get('action') == action]
        
        return logs[-limit:] if limit else logs
    
    def get_actions(self) -> List[str]:
        """Get all unique actions"""
        actions = set()
        for log in self.logs:
            actions.add(log.get('action', ''))
        return sorted(list(actions))
    
    def get_users(self) -> List[str]:
        """Get all unique users"""
        users = set()
        for log in self.logs:
            users.add(log.get('user', ''))
        return sorted(list(users))
    
    def get_stats(self) -> Dict:
        """Get audit statistics"""
        total = len(self.logs)
        action_count = {}
        user_count = {}
        
        for log in self.logs:
            action = log.get('action', 'unknown')
            user = log.get('user', 'unknown')
            action_count[action] = action_count.get(action, 0) + 1
            user_count[user] = user_count.get(user, 0) + 1
        
        return {
            'total_logs': total,
            'action_count': action_count,
            'user_count': user_count,
            'last_24h': len([l for l in self.logs 
                           if (datetime.now() - datetime.fromisoformat(l['timestamp'])).days < 1])
        }

# Singleton instance
audit_logger = AuditLogger()
