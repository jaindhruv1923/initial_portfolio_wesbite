"""
Sample authentication module for Kavach demo.
Shows typical code structure that Kavach will analyze.
"""

import hashlib
from typing import Optional


class User:
    """Represents a user in the system."""
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.password_hash: Optional[str] = None
        self.is_active = True
    
    def set_password(self, password: str) -> None:
        """Hash and store user password."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify provided password against stored hash."""
        if not self.password_hash:
            return False
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash


def authenticate_user(username: str, password: str, user_db: dict) -> Optional[User]:
    """
    Authenticate a user by username and password.
    
    Args:
        username: The user's username
        password: The user's plain-text password
        user_db: Dictionary of username -> User mappings
    
    Returns:
        The authenticated User object, or None if auth failed
    """
    if not username or not password:
        return None
    
    user = user_db.get(username)
    if user and user.verify_password(password) and user.is_active:
        return user
    
    return None


def create_session_token(user: User) -> str:
    """Create a session token for an authenticated user."""
    # In production, would use secure token generation
    # This is simplified for demo purposes
    import uuid
    return f"session_{user.username}_{uuid.uuid4()}"
