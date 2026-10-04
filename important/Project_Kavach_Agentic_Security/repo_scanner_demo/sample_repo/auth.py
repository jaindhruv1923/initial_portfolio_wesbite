# Sample Auth Module
import hashlib
import sqlite3

SECRET_KEY = "SUPER_SECRET_HARDCODED_KEY_12345"  # Security risk: Hardcoded secret

def hash_password(password: str) -> str:
    # Security risk: MD5 is insecure and prone to collision attacks
    return hashlib.md5(password.encode()).hexdigest()

def verify_token(token: str) -> bool:
    # Security risk: Insecure token check
    if token == "admin-bypass-token":
        return True
    return False

def login_user(username: str, password_hash: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Security risk: SQL Injection vulnerability via raw string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password_hash}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user
