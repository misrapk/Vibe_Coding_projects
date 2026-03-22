from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Dict, Any
from src.backend.api.deps import get_db, get_current_user
from src.backend.api.schemas import AnalyticsResponse, JobStats, BiasReport
import src.backend.models as models
from src.backend.bias_detector import BiasDetector

router = APIRouter(prefix="/analytics", tags=["analytics"])

bias_detector = BiasDetector()

@router.get("/dashboard", response_model=AnalyticsResponse)
def get_dashboard_analytics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns analytics based on user role."""
    stats = {}
    
    if current_user.role == models.UserRole.CANDIDATE:
        # Candidate Stats
        total_resumes = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).count()
        resume_ids = [r.id for r in db.query(models.Resume.id).filter(models.Resume.user_id == current_user.id).all()]
        
        matches_query = db.query(models.Match).filter(models.Match.resume_id.in_(resume_ids))
        total_matches = matches_query.count()
        avg_score = db.query(func.avg(models.Match.overall_score)).filter(models.Match.resume_id.in_(resume_ids)).scalar() or 0
        
        applications = db.query(models.Application).filter(models.Application.resume_id.in_(resume_ids))
        app_count = applications.count()
        
        status_breakdown = dict(db.query(
            models.Application.status, func.count(models.Application.id)
        ).filter(models.Application.resume_id.in_(resume_ids)).group_by(models.Application.status).all())
        # Convert enum keys to strings
        status_breakdown = {str(k.value): v for k, v in status_breakdown.items()}

        stats = {
            "role": "candidate",
            "total_resumes": total_resumes,
            "total_matches": total_matches,
            "avg_match_score": round(avg_score, 1),
            "applications_submitted": app_count,
            "status_breakdown": status_breakdown
        }
        
    else:
        # Recruiter Stats
        jobs_query = db.query(models.Job).filter(models.Job.recruiter_id == current_user.id)
        job_ids = [j.id for j in db.query(models.Job.id).filter(models.Job.recruiter_id == current_user.id).all()]
        
        total_jobs = jobs_query.count()
        total_candidates = db.query(models.Match).filter(models.Match.job_id.in_(job_ids)).count()
        avg_quality = db.query(func.avg(models.Match.overall_score)).filter(models.Match.job_id.in_(job_ids)).scalar() or 0
        
        shortlisted = db.query(models.Feedback).filter(
            models.Feedback.recruiter_id == current_user.id,
            models.Feedback.action == "shortlist"
        ).count()
        
        filled = db.query(models.Job).filter(
            models.Job.recruiter_id == current_user.id,
            models.Job.status == models.JobStatus.CLOSED
        ).count()

        stats = {
            "role": "recruiter",
            "total_jobs_posted": total_jobs,
            "total_candidates_matched": total_candidates,
            "avg_match_quality": round(avg_quality, 1),
            "shortlisted_candidates": shortlisted,
            "positions_filled": filled
        }
        
    return {"stats": stats}

@router.get("/jobs/{job_id}/stats", response_model=JobStats)
def get_job_analytics(
    job_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Statistics for a specific job."""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    matches = db.query(models.Match).filter(models.Match.job_id == job_id).all()
    total_applicants = len(matches)
    avg_score = sum(m.overall_score for m in matches) / total_applicants if total_applicants > 0 else 0
    
    # Score distribution for histogram
    bins = [0, 20, 40, 60, 80, 100]
    hist = {f"{bins[i]}-{bins[i+1]}": 0 for i in range(len(bins)-1)}
    for m in matches:
        for i in range(len(bins)-1):
            if bins[i] <= m.overall_score < bins[i+1]:
                hist[f"{bins[i]}-{bins[i+1]}"] += 1
                break
        if m.overall_score == 100:
            hist["80-100"] += 1

    # Extract top skills in pool
    # This is a bit complex since skills are in JSON. We'll simulate for now or do a light pass.
    # In a real app, we'd have a mapping table.
    pool_skills = []
    for m in matches:
        resume = db.get(models.Resume, m.resume_id)
        if resume:
            pool_skills.extend(resume.parsed_data.get("skills", []))
    
    from collections import Counter
    top_skills = [s for s, c in Counter(pool_skills).most_common(5)]

    return {
        "total_applicants": total_applicants,
        "avg_score": round(avg_score, 1),
        "score_distribution": [{"range": k, "count": v} for k, v in hist.items()],
        "top_skills": top_skills,
        "charts_data": {"histogram": hist}
    }

@router.get("/bias-reports", response_model=List[BiasReport])
def get_bias_reports(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns bias analysis for all recruiter's jobs."""
    if current_user.role != models.UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Only recruiters can view bias reports")

    jobs = db.query(models.Job).filter(models.Job.recruiter_id == current_user.id).all()
    reports = []
    
    for job in jobs:
        analysis = bias_detector.analyze(job.description)
        reports.append({
            "job_id": job.id,
            "job_title": job.title,
            "bias_score": analysis.get("bias_score", 0),
            "issues": [f"{cat}: {len(items)} flag(s)" for cat, items in analysis.get("analysis", {}).items() if items],
            "suggestions": analysis.get("suggestions", [])
        })
        
    return reports
@router.get("/candidates/all")
def get_all_candidates_cross_job(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Returns all candidates in the system for recruiters."""
    if current_user.role != models.UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Only recruiters can view all candidates")
    
    # Get all users with CANDIDATE role who have at least one resume
    candidates = db.query(models.User).filter(
        models.User.role == models.UserRole.CANDIDATE
    ).join(models.Resume, isouter=False).distinct().all()
    
    result = []
    for cand in candidates:
        # For each candidate, find their best match across all jobs
        best_match = db.query(models.Match).join(models.Resume).filter(
            models.Resume.user_id == cand.id
        ).order_by(models.Match.overall_score.desc()).first()
        
        best_score = best_match.overall_score if best_match else 0
        best_job = db.get(models.Job, best_match.job_id).title if best_match else "None"
        
        result.append({
            "id": cand.id,
            "name": f"{cand.first_name} {cand.last_name}",
            "email": cand.email,
            "best_match_score": best_score,
            "best_matched_job": best_job,
            "resumes_count": len(cand.resumes)
        })
        
    return sorted(result, key=lambda x: x["best_match_score"], reverse=True)
