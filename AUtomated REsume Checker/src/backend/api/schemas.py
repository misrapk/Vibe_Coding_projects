from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
import enum

from src.backend.models import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

# Resume Schemas
class ResumeResponse(BaseModel):
    id: int
    filename: str
    upload_date: datetime
    parsed_data: dict

    class Config:
        from_attributes = True

# Job Schemas
class JobCreate(BaseModel):
    title: str
    company_name: str
    description: str
    location: Optional[str] = None
    job_type: Optional[str] = "full-time"
    salary_min: Optional[float] = 0
    salary_max: Optional[float] = 0

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None

class JobResponse(BaseModel):
    id: int
    recruiter_id: int
    title: str
    company_name: Optional[str]
    description: Optional[str]
    location: Optional[str]
    job_type: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    status: str
    created_at: datetime
    parsed_data: dict

    class Config:
        from_attributes = True

# Match Schemas
class MatchResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    semantic_score: float
    explanation: Optional[str]
    created_at: datetime
    job_details: Optional[JobResponse] = None

    class Config:
        from_attributes = True

# Feedback Schemas
class FeedbackCreate(BaseModel):
    action: str = Field(..., description="Action taken: shortlist, reject, interview, offer")
    notes: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    match_id: int
    recruiter_id: int
    action: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Analytics Schemas
class AnalyticsResponse(BaseModel):
    stats: Dict[str, Any]

class JobStats(BaseModel):
    total_applicants: int
    avg_score: float
    score_distribution: List[Dict[str, Any]]
    top_skills: List[str]
    charts_data: Dict[str, Any]

class BiasReport(BaseModel):
    job_id: int
    job_title: str
    bias_score: float
    issues: List[str]
    suggestions: List[str]

# Matching Schemas
class MatchTriggerResponse(BaseModel):
    job_started: bool
    message: str
    estimated_time: Optional[str] = None

class MatchProcessSummary(BaseModel):
    total_resumes: int
    matches_found: int
    top_candidates: List[Dict[str, Any]]

# Application Schemas
class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int

class ApplicationResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    status: str
    applied_at: datetime
    
    class Config:
        from_attributes = True

# Utility Schemas
class SkillSearchResponse(BaseModel):
    skill_name: str
    category: Optional[str] = None

class HealthStatus(BaseModel):
    status: str
    database: str
    storage: str
    timestamp: datetime
