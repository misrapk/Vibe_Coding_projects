import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.backend.api.deps import get_db, get_current_user
from src.backend.api.schemas import ResumeResponse, MatchResponse
import src.backend.models as models
from src.backend.parser import ResumeParser
from src.backend.semantic_matcher import SemanticMatcher
from datetime import datetime

router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = "data/uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize shared components
resume_parser = ResumeParser()
semantic_matcher = SemanticMatcher()

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Uploads, parses, and indexes a resume."""
    if current_user.role != models.UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can upload resumes"
        )

    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )

    # Parse resume
    try:
        parsed_data = resume_parser.parse(file_path)
        if "error" in parsed_data:
             raise Exception(parsed_data["error"])
    except Exception as e:
        os.remove(file_path) # Cleanup
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Parsing error: {str(e)}"
        )

    # Generate embedding
    embedding = semantic_matcher.get_text_embedding(parsed_data.get("raw_text", ""))

    # Save to DB
    new_resume = models.Resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        parsed_data=parsed_data,
        embedding=embedding.tobytes()
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return new_resume

@router.get("/my", response_model=List[ResumeResponse])
def get_my_resumes(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns all resumes belonging to the current user."""
    return db.query(models.Resume).filter(models.Resume.user_id == current_user.id).all()

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves a specific resume if owned by the user or if viewed by a recruiter."""
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Recruiter can view any resume, Candidate can only view their own
    if current_user.role == models.UserRole.CANDIDATE and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this resume")
    
    return resume

@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a resume and its associated file."""
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this resume")

    # Remove file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)

    db.delete(resume)
    db.commit()
    return {"message": "Resume deleted successfully"}

@router.get("/{resume_id}/matches", response_model=List[MatchResponse])
def get_resume_matches(
    resume_id: int,
    limit: int = 10,
    offset: int = 0,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns top job matches for a specific resume."""
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view matches for this resume")

    matches = db.query(models.Match).filter(models.Match.resume_id == resume_id).order_by(models.Match.overall_score.desc()).limit(limit).offset(offset).all()
    
    # We might want to attach job title/company to the response
    # This is handled by SQLAlchemy relationships in the schema's from_attributes
    return matches
