import os
import bcrypt
import json
import numpy as np
from sqlalchemy import create_engine, or_, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, User, Resume, Job, Match, Feedback, Application, UserRole, JobStatus
from typing import List, Dict, Any, Optional

# Shared engine and sessionmaker
_engine = None
_SessionLocal = None

class DatabaseManager:
    def __init__(self, db_path: str = None):
        global _engine, _SessionLocal
        
        if _engine is None:
            if db_path is None:
                db_path = os.getenv("DATABASE_PATH", "data/resume_checker.db")
            db_url = f"sqlite:///{db_path}"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            _engine = create_engine(db_url, connect_args={"check_same_thread": False})
            _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
            
            # Initialize tables once
            Base.metadata.create_all(bind=_engine)
            
            # Seed default admin
            temp_session = scoped_session(_SessionLocal)
            if temp_session.query(User).count() == 0:
                self._seed_admin_internal(temp_session)
            temp_session.remove()

        self.session = scoped_session(_SessionLocal)

    def _seed_admin_internal(self, session):
        """Internal seeding logic using a provided session."""
        hashed = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(
            email="admin@example.com",
            password_hash=hashed,
            role=UserRole.RECRUITER,
            first_name="System",
            last_name="Admin"
        )
        session.add(user)
        session.commit()

    # --- User Management ---
    def create_user(self, email: str, password: str, role: str, first_name: str = "", last_name: str = "") -> User:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(
            email=email,
            password_hash=hashed,
            role=UserRole(role),
            first_name=first_name,
            last_name=last_name
        )
        self.session.add(user)
        self.session.commit()
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.session.query(User).filter(User.email == email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    # --- Resume Operations ---
    def save_resume(self, user_id: int, filename: str, file_path: str, parsed_data: Dict[str, Any], embedding: np.ndarray = None) -> Resume:
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            parsed_data=parsed_data,
            embedding=embedding.tobytes() if embedding is not None else None
        )
        self.session.add(resume)
        self.session.commit()
        return resume

    def get_user_resumes(self, user_id: int) -> List[Resume]:
        return self.session.query(Resume).filter(Resume.user_id == user_id).all()

    def get_all_resumes_for_engine(self) -> List[Dict[str, Any]]:
        resumes = self.session.query(Resume).all()
        return [
            {
                "id": r.id, 
                "data": r.parsed_data, 
                "name": r.parsed_data.get("personal_info", {}).get("name", "Unknown"),
                "email": r.parsed_data.get("personal_info", {}).get("email", "")
            } for r in resumes
        ]

    # --- Job Operations ---
    def create_job(self, recruiter_id: int, title: str, description: str, parsed_data: Dict[str, Any], 
                   company_name: str = "", location: str = "", job_type: str = "Full-time", 
                   salary_min: float = 0, salary_max: float = 0, embedding: np.ndarray = None) -> Job:
        job = Job(
            recruiter_id=recruiter_id,
            title=title,
            company_name=company_name,
            description=description,
            parsed_data=parsed_data,
            location=location,
            job_type=job_type,
            salary_min=salary_min,
            salary_max=salary_max,
            embedding=embedding.tobytes() if embedding is not None else None
        )
        self.session.add(job)
        self.session.commit()
        return job

    def get_all_jobs_for_engine(self) -> List[Dict[str, Any]]:
        jobs = self.session.query(Job).filter(Job.status == JobStatus.ACTIVE).all()
        return [{"id": j.id, "title": j.title, "data": j.parsed_data, "embedding": j.embedding} for j in jobs]

    def search_jobs(self, query: str = None, location: str = None) -> List[Job]:
        filters = [Job.status == JobStatus.ACTIVE]
        if query:
            filters.append(or_(Job.title.ilike(f"%{query}%"), Job.description.ilike(f"%{query}%")))
        if location:
            filters.append(Job.location.ilike(f"%{location}%"))
        
        return self.session.query(Job).filter(and_(*filters)).all()

    def get_recruiter_jobs_with_stats(self, recruiter_id: int) -> List[Dict[str, Any]]:
        jobs = self.session.query(Job).filter(Job.recruiter_id == recruiter_id).all()
        result = []
        for job in jobs:
            match_count = self.session.query(Match).filter(Match.job_id == job.id).count()
            result.append({
                "job": job,
                "match_count": match_count
            })
        return result

    # --- Match Operations ---
    def save_match(self, resume_id: int, job_id: int, scores: Dict[str, float], details: Dict[str, Any], explanation: str) -> Match:
        existing = self.session.query(Match).filter(Match.resume_id == resume_id, Match.job_id == job_id).first()
        if existing:
            existing.overall_score = scores.get("total_score")
            existing.skills_score = scores.get("skills_match")
            existing.experience_score = scores.get("experience_match")
            existing.education_score = scores.get("education_match")
            existing.semantic_score = scores.get("semantic_match")
            existing.match_details = details
            existing.explanation = explanation
            existing.created_at = func.now()
            match = existing
        else:
            match = Match(
                resume_id=resume_id,
                job_id=job_id,
                overall_score=scores.get("total_score"),
                skills_score=scores.get("skills_match"),
                experience_score=scores.get("experience_match"),
                education_score=scores.get("education_match"),
                semantic_score=scores.get("semantic_match"),
                match_details=details,
                explanation=explanation
            )
            self.session.add(match)
        
        self.session.commit()
        return match

    def get_job_matches(self, job_id: int, limit: int = 5) -> List[Match]:
        return self.session.query(Match).filter(Match.job_id == job_id).order_by(Match.overall_score.desc()).limit(limit).all()

    # --- Analytics ---
    def get_analytics(self) -> Dict[str, Any]:
        return {
            "total_users": self.session.query(User).count(),
            "candidate_count": self.session.query(User).filter(User.role == UserRole.CANDIDATE).count(),
            "recruiter_count": self.session.query(User).filter(User.role == UserRole.RECRUITER).count(),
            "active_jobs": self.session.query(Job).filter(Job.status == JobStatus.ACTIVE).count(),
            "total_resumes": self.session.query(Resume).count(),
            "total_matches": self.session.query(Match).count()
        }

    def close(self):
        self.session.remove()
