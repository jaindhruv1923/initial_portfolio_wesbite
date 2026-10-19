"""
API endpoints for user authentication.
"""

from typing import Optional
from auth import authenticate_user, create_session_token
from database import init_database


class APIEndpoints:
    """REST API endpoints for the demo application."""
    
    def __init__(self):
        self.db = init_database()
    
    def login(self, username: str, password: str) -> Optional[dict]:
        """
        Login endpoint - authenticate user and return session token.
        
        POST /api/login
        Body: {"username": "...", "password": "..."}
        Response: {"session_token": "...", "username": "..."} or None
        """
        user = authenticate_user(username, password, self.db._users)
        if user:
            token = create_session_token(user)
            return {
                "session_token": token,
                "username": user.username,
                "email": user.email,
            }
        return None
    
    def register(self, username: str, email: str, password: str) -> Optional[dict]:
        """
        Registration endpoint - create new user.
        
        POST /api/register
        Body: {"username": "...", "email": "...", "password": "..."}
        Response: {"username": "...", "email": "..."} or error
        """
        try:
            user = self.db.create_user(username, email)
            user.set_password(password)
            return {
                "username": user.username,
                "email": user.email,
                "message": "User registered successfully",
            }
        except ValueError as e:
            return {"error": str(e)}
    
    def get_user_profile(self, username: str) -> Optional[dict]:
        """Get user profile information."""
        user = self.db.get_user(username)
        if user:
            return {
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
            }
        return None
