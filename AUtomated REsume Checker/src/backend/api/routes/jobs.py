from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from src.backend.api.deps import get_db, get_current_user
from src.backend.api.schemas import JobCreate, JobUpdate, JobResponse
import src.backend.models as models
from src.backend.jd_parser import JDParser
from src.backend.bias_detector import BiasDetector
from src.backend.semantic_matcher import SemanticMatcher
from src.backend.matching_engine import MatchingEngine
from src.backend.skills_engine import SkillsEngine
from src.backend.explanation_generator import ExplanationGenerator
from datetime import datetime

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Initialize shared components
jd_parser = JDParser()
bias_detector = BiasDetector()
semantic_matcher = SemanticMatcher()
skills_engine = SkillsEngine()
matching_engine = MatchingEngine(skills_engine, semantic_matcher)
explanation_generator = ExplanationGenerator()

@router.post("/", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a new job posting with bias analysis and semantic embedding."""
    if current_user.role != models.UserRole.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can post jobs"
        )

    # Parse JD
    try:
        parsed_data = jd_parser.parse(job_in.description)
        # Note: We could also do a bias check here and return it in a separate field
        # but for now we follow the schema and save the job.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JD Parsing failed: {str(e)}")

    # Generate embedding
    embedding = semantic_matcher.get_text_embedding(job_in.description)

    # Save to DB
    new_job = models.Job(
        recruiter_id=current_user.id,
        title=job_in.title,
        company_name=job_in.company_name,
        description=job_in.description,
        parsed_data=parsed_data,
        location=job_in.location,
        job_type=job_in.job_type,
        salary_min=job_in.salary_min,
        salary_max=job_in.salary_max,
        embedding=embedding.tobytes()
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/", response_model=List[JobResponse])
def list_jobs(
    q: Optional[str] = Query(None, description="Search by title or description"),
    location: Optional[str] = Query(None, description="Filter by location"),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Lists active jobs with search and filtering support."""
    query = db.query(models.Job).filter(models.Job.status == models.JobStatus.ACTIVE)
    
    if q:
        query = query.filter(or_(models.Job.title.ilike(f"%{q}%"), models.Job.description.ilike(f"%{q}%")))
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(models.Job.job_type.ilike(f"%{job_type}%"))
    
    return query.order_by(models.Job.created_at.desc()).limit(limit).offset(offset).all()

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Retrieves full job details."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates a job posting. Re-parses and re-embeds if description changes."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this job")

    update_data = job_in.dict(exclude_unset=True)
    
    if "description" in update_data:
        # Re-parse and Re-embed
        job.parsed_data = jd_parser.parse(update_data["description"])
        job.embedding = semantic_matcher.get_text_embedding(update_data["description"]).tobytes()

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a job posting and its matches."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}

@router.get("/{job_id}/candidates")
def get_job_candidates(
    job_id: int,
    min_score: float = 0.0,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ranks all candidates for a specific job (Recruiter only)."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view candidates for this job")

    all_resumes = db.query(models.Resume).all()
    if not all_resumes:
        return []

    ranked = matching_engine.rank_candidates(job.parsed_data, all_resumes, threshold=min_score)
    
    # We could also save these matches to the DB if we want them to be persistent
    for res in ranked:
        # Simple persistence check/update
        existing_match = db.query(models.Match).filter(
            models.Match.job_id == job_id, 
            models.Match.resume_id == res["candidate_id"]
        ).first()
        
        # Note: res["breakdown"] contains the components.
        # res["details"] contains matched skills, gaps, etc.
        
        score_data = {
            "total_score": res["score"],
            "skills_match": res["breakdown"].get("skills_match", 0),
            "experience_match": res["breakdown"].get("experience_match", 0),
            "education_match": res["breakdown"].get("education_match", 0),
            "semantic_match": res["breakdown"].get("semantic_match", 0),
            "details": res["details"]
        }
        
        resume_obj = db.get(models.Resume, res["candidate_id"])
        explanation = explanation_generator.generate_match_explanation(
            resume_obj.parsed_data,
            job.parsed_data,
            score_data
        )

        if existing_match:
            existing_match.overall_score = res["score"]
            existing_match.explanation = explanation
            existing_match.match_details = res["details"]
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
    return ranked
