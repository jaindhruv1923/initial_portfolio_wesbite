"""
User database models for Kavach demo.
"""

from typing import Dict, Optional
from auth import User


class UserDatabase:
    """In-memory user database for demo purposes."""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user in the database."""
        if username in self._users:
            raise ValueError(f"User {username} already exists")
        
        user = User(username, email)
        self._users[username] = user
        return user
    
    def get_user(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        return self._users.get(username)
    
    def delete_user(self, username: str) -> bool:
        """Delete a user from the database."""
        if username in self._users:
            del self._users[username]
            return True
        return False
    
    def list_users(self) -> list[str]:
        """List all usernames in the database."""
        return list(self._users.keys())


# Global database instance
_db = UserDatabase()


def init_database() -> UserDatabase:
    """Initialize and return the database."""
    return _db
