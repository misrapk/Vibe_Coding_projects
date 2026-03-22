from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, JSON, LargeBinary, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"

class JobStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"

class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    parsed_data = Column(JSON)  # Entire parsed resume structure
    embedding = Column(LargeBinary) # Vector embedding stored as binary
    upload_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    matches = relationship("Match", back_populates="resume", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="resume")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    company_name = Column(String(255))
    description = Column(Text)
    parsed_data = Column(JSON) # Parsed requirements
    embedding = Column(LargeBinary)
    location = Column(String(255), index=True)
    job_type = Column(String(100)) # full-time, remote, etc.
    salary_min = Column(Float)
    salary_max = Column(Float)
    status = Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    recruiter = relationship("User", back_populates="jobs")
    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    overall_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    semantic_score = Column(Float)
    match_details = Column(JSON) # Detailed breakdown
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_viewed_by_recruiter = Column(Boolean, default=False)
    
    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("Job", back_populates="matches")
    feedbacks = relationship("Feedback", back_populates="match", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100)) # shortlist, reject, etc.
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="feedbacks")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="applications")
    job = relationship("Job", back_populates="applications")
