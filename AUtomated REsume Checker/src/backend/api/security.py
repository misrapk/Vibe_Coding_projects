import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 # 24 hours

def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a hashed one."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user_id: int, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generates a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(user_id),
        "role": role
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decodes a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
