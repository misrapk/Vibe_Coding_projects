from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.backend.database import DatabaseManager
import src.backend.models as models
from .security import SECRET_KEY, ALGORITHM
from .schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_db():
    db_manager = DatabaseManager()
    try:
        yield db_manager.session
    finally:
        db_manager.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id), role=role)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Simple in-memory cache
_cache = {}

def get_cache():
    return _cache
