from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import src.backend.models as models
from src.backend.api.schemas import UserRegister, UserResponse, Token
from src.backend.api.security import hash_password, verify_password, create_access_token
from src.backend.api.deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Registers a new user."""
    # Check if email exists
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists"
        )
    
    # Hash password and create user
    hashed = hash_password(user_in.password)
    user = models.User(
        email=user_in.email,
        password_hash=hashed,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        role=models.UserRole(user_in.role)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticates a user and returns a JWT token."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user_id=user.id, role=user.role.value)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Returns the current user details."""
    return current_user
