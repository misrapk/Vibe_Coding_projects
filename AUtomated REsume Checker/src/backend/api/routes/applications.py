from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.backend.api.deps import get_db, get_current_user
from src.backend.api.schemas import ApplicationCreate, ApplicationResponse
import src.backend.models as models

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=ApplicationResponse)
def apply_to_job(
    application_in: ApplicationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submits a job application for a candidate."""
    if current_user.role != models.UserRole.CANDIDATE:
        raise HTTPException(status_code=403, detail="Only candidates can apply to jobs")

    # Verify resume ownership
    resume = db.query(models.Resume).filter(
        models.Resume.id == application_in.resume_id,
        models.Resume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found or not owned by you")

    # Verify job existence
    job = db.query(models.Job).filter(models.Job.id == application_in.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check for existing application
    existing = db.query(models.Application).filter(
        models.Application.resume_id == application_in.resume_id,
        models.Application.job_id == application_in.job_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already applied to this job with this resume")

    new_app = models.Application(
        resume_id=application_in.resume_id,
        job_id=application_in.job_id,
        status=models.ApplicationStatus.PENDING
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    return new_app

@router.get("/my", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns all applications submitted by the current user."""
    # Applications are linked to resumes, which are linked to users.
    resume_ids = [r.id for r in db.query(models.Resume.id).filter(models.Resume.user_id == current_user.id).all()]
    return db.query(models.Application).filter(models.Application.resume_id.in_(resume_ids)).all()
