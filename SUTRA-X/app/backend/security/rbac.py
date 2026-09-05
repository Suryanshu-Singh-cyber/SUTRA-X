
"""
Real Role-Based Access Control
"""

from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime
import json
import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

class Role(Enum):
    ADMIN = "admin"
    INVESTIGATOR = "investigator"
    ANALYST = "analyst"
    VIEWER = "viewer"

class Permission(Enum):
    VIEW_DATA = "view_data"
    EXPORT_DATA = "export_data"
    MANAGE_ENTITIES = "manage_entities"
    MANAGE_USERS = "manage_users"
    VIEW_AUDIT = "view_audit"
    MANAGE_ALERTS = "manage_alerts"
    RUN_SIMULATION = "run_simulation"

# Role permissions mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.VIEW_DATA,
        Permission.EXPORT_DATA,
        Permission.MANAGE_ENTITIES,
        Permission.MANAGE_USERS,
        Permission.VIEW_AUDIT,
        Permission.MANAGE_ALERTS,
        Permission.RUN_SIMULATION
    ],
    Role.INVESTIGATOR: [
        Permission.VIEW_DATA,
        Permission.EXPORT_DATA,
        Permission.MANAGE_ENTITIES,
        Permission.VIEW_AUDIT,
        Permission.MANAGE_ALERTS,
        Permission.RUN_SIMULATION
    ],
    Role.ANALYST: [
        Permission.VIEW_DATA,
        Permission.EXPORT_DATA,
        Permission.VIEW_AUDIT
    ],
    Role.VIEWER: [
        Permission.VIEW_DATA
    ]
}

class RBACManager:
    """Real RBAC Manager"""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "your_jwt_secret_here")
        self.users = {}
        self._load_users()
    
    def _load_users(self):
        """Load users from storage"""
        # In production, this would load from a database
        # For demo, we'll use in-memory storage
        self.users = {
            "admin": {
                "password": self._hash_password("admin123"),
                "role": Role.ADMIN,
                "created_at": datetime.now().isoformat()
            },
            "investigator": {
                "password": self._hash_password("invest123"),
                "role": Role.INVESTIGATOR,
                "created_at": datetime.now().isoformat()
            },
            "analyst": {
                "password": self._hash_password("analyst123"),
                "role": Role.ANALYST,
                "created_at": datetime.now().isoformat()
            },
            "viewer": {
                "password": self._hash_password("viewer123"),
                "role": Role.VIEWER,
                "created_at": datetime.now().isoformat()
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        if self.verify_password(password, user['password']):
            return {
                'username': username,
                'role': user['role'].value,
                'permissions': [p.value for p in ROLE_PERMISSIONS.get(user['role'], [])]
            }
        return None
    
    def generate_token(self, user_data: Dict) -> str:
        """Generate JWT token"""
        payload = {
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def has_permission(self, user_role: str, permission: str) -> bool:
        """Check if user has permission"""
        try:
            role = Role(user_role)
            permissions = ROLE_PERMISSIONS.get(role, [])
            return Permission(permission) in permissions
        except:
            return False
    
    def get_user_roles(self) -> Dict[str, str]:
        """Get all available roles"""
        return {r.value: r.value.capitalize() for r in Role}

# Singleton instance
rbac_manager = RBACManager()
