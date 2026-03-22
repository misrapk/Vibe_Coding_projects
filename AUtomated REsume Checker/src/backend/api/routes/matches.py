from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.backend.api.deps import get_db, get_current_user
from src.backend.api.schemas import (
    MatchResponse, MatchTriggerResponse, FeedbackCreate, FeedbackResponse, 
    MatchProcessSummary
)
import src.backend.models as models
from src.backend.matching_engine import MatchingEngine
from src.backend.skills_engine import SkillsEngine
from src.backend.semantic_matcher import SemanticMatcher
from src.backend.explanation_generator import ExplanationGenerator
import time

router = APIRouter(prefix="/matches", tags=["matches"])

# Shared components
skills_engine = SkillsEngine()
semantic_matcher = SemanticMatcher()
matching_engine = MatchingEngine(skills_engine, semantic_matcher)
explanation_generator = ExplanationGenerator()

def run_matching_job(job_id: int, db: Session):
    """Background task to run matching for all resumes against a job."""
    job = db.get(models.Job, job_id)
    if not job:
        return

    all_resumes = db.query(models.Resume).all()
    ranked = matching_engine.rank_candidates(job.parsed_data, all_resumes, threshold=0.0)
    
    for res in ranked:
        # Check for existing match
        existing = db.query(models.Match).filter_by(job_id=job_id, resume_id=res["candidate_id"]).first()
        
        score_data = {
            "total_score": res["score"],
            "skills_match": res["breakdown"].get("skills_match", 0),
            "experience_match": res["breakdown"].get("experience_match", 0),
            "education_match": res["breakdown"].get("education_match", 0),
            "semantic_match": res["breakdown"].get("semantic_match", 0),
            "details": res["details"]
        }
        
        resume = db.get(models.Resume, res["candidate_id"])
        explanation = explanation_generator.generate_match_explanation(
            resume.parsed_data, job.parsed_data, score_data
        )

        if existing:
            existing.overall_score = res["score"]
            existing.explanation = explanation
            existing.match_details = res["details"]
        else:
            new_match = models.Match(
                resume_id=res["candidate_id"],
                job_id=job_id,
                overall_score=res["score"],
                skills_score=score_data["skills_match"],
                experience_score=score_data["experience_match"],
                education_score=score_data["education_match"],
                semantic_score=score_data["semantic_match"],
                match_details=res["details"],
                explanation=explanation
            )
            db.add(new_match)
    
    db.commit()

@router.post("/trigger/{job_id}", response_model=MatchTriggerResponse)
async def trigger_matching(
    job_id: int, 
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Triggers the matching analysis for a specific job."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to match for this job")

    background_tasks.add_task(run_matching_job, job_id, db)
    return {"job_started": True, "message": "Matching process started in background"}

@router.get("/{match_id}", response_model=MatchResponse)
def get_match_details(
    match_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves full details for a match."""
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Check access
    job = db.query(models.Job).get(match.job_id)
    resume = db.query(models.Resume).get(match.resume_id)
    
    if current_user.role == models.UserRole.RECRUITER and job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current_user.role == models.UserRole.CANDIDATE and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return match

@router.post("/{match_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(
    match_id: int,
    feedback_in: FeedbackCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submits recruiter feedback on a match."""
    if current_user.role != models.UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Only recruiters can provide feedback")

    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    job = db.query(models.Job).get(match.job_id)
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to feedback this match")

    new_feedback = models.Feedback(
        match_id=match_id,
        recruiter_id=current_user.id,
        action=feedback_in.action,
        notes=feedback_in.notes
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback

@router.get("/{match_id}/feedback", response_model=List[FeedbackResponse])
def get_feedback_history(
    match_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves feedback history for a match."""
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Authorization checks
    job = db.query(models.Job).get(match.job_id)
    resume = db.query(models.Resume).get(match.resume_id)
    
    if current_user.role == models.UserRole.RECRUITER and job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if current_user.role == models.UserRole.CANDIDATE and resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db.query(models.Feedback).filter(models.Feedback.match_id == match_id).all()
