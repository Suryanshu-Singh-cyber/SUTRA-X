"""
Role-Based Access Control
"""

USERS_DB = {
    "admin": {"password": "admin123", "role": "admin", "name": "Administrator"},
    "investigator": {"password": "invest123", "role": "investigator", "name": "Senior Investigator"},
    "analyst": {"password": "analyst123", "role": "analyst", "name": "Data Analyst"},
    "viewer": {"password": "viewer123", "role": "viewer", "name": "Viewer"}
}

ROLE_PERMISSIONS = {
    "admin": ["view_data", "export_data", "manage_entities", "manage_users", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "investigator": ["view_data", "export_data", "manage_entities", "view_audit", "manage_alerts", "run_simulation", "use_ai"],
    "analyst": ["view_data", "export_data", "view_audit", "use_ai"],
    "viewer": ["view_data"]
}

def authenticate_user(username, password):
    if username in USERS_DB and USERS_DB[username]["password"] == password:
        return USERS_DB[username]
    return None

def has_permission(role, permission):
    return permission in ROLE_PERMISSIONS.get(role, [])
