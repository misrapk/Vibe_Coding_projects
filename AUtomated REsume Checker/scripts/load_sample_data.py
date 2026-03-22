import os
import sys
import json
import numpy as np
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.backend.database import DatabaseManager
from src.backend.parser import ResumeParser
from src.backend.jd_parser import JDParser
from src.backend.skills_engine import SkillsEngine
from src.backend.semantic_matcher import SemanticMatcher
from src.backend.matching_engine import MatchingEngine
from src.backend.explanation_generator import ExplanationGenerator
from src.backend.models import User, Resume, Job, UserRole, JobStatus

def load_sample_data():
    print("Starting Sample Data Load...")
    db = DatabaseManager()
    skills_engine = SkillsEngine()
    semantic_matcher = SemanticMatcher()
    matching_engine = MatchingEngine(skills_engine, semantic_matcher)
    explanation_generator = ExplanationGenerator()
    resume_parser = ResumeParser()
    job_parser = JDParser()

    # 1. Clear Existing Sample Data (excluding admin)
    print("Clearing existing sample data...")
    db.session.query(Job).filter(Job.recruiter_id != 1).delete() # Assuming admin is 1
    db.session.query(Resume).delete()
    db.session.query(User).filter(User.email != "admin@example.com").delete()
    db.session.commit()

    # 2. Create Test Users
    print("Creating test users...")
    candidates = []
    for i in range(1, 6):
        user = db.create_user(
            email=f"candidate{i}@test.com",
            password="Password123",
            role=UserRole.CANDIDATE.value,
            first_name=f"Candidate",
            last_name=str(i)
        )
        candidates.append(user)
    
    recruiters = []
    for i in range(1, 4):
        user = db.create_user(
            email=f"recruiter{i}@test.com",
            password="Password123",
            role=UserRole.RECRUITER.value,
            first_name=f"Recruiter",
            last_name=str(i)
        )
        recruiters.append(user)

    # 3. Upload Sample Resumes
    print("Uploading and parsing resumes...")
    resume_dir = "data/samples/resumes"
    resume_files = os.listdir(resume_dir)
    db_resumes = []
    
    for idx, filename in enumerate(resume_files):
        with open(os.path.join(resume_dir, filename), "r", encoding="utf-8") as f:
            text = f.read()
            parsed = resume_parser.parse(text)
            
            # Map to a candidate (cycling if more resumes than users)
            user_id = candidates[idx % len(candidates)].id
            
            # Generate dummy embedding
            embedding = np.random.rand(384).astype(np.float32)
            
            resume = db.save_resume(
                user_id=user_id,
                filename=filename,
                file_path=f"data/storage/resumes/{filename}", # Mock path
                parsed_data=parsed,
                embedding=embedding
            )
            db_resumes.append(resume)

    # 4. Create Sample Jobs
    print("Creating sample jobs...")
    job_dir = "data/samples/jobs"
    job_files = os.listdir(job_dir)
    db_jobs = []
    
    for idx, filename in enumerate(job_files):
        with open(os.path.join(job_dir, filename), "r", encoding="utf-8") as f:
            text = f.read()
            parsed = job_parser.parse(text)
            
            # Map to a recruiter
            recruiter_id = recruiters[idx % len(recruiters)].id
            
            # Generate dummy embedding
            embedding = np.random.rand(384).astype(np.float32)
            
            job = db.create_job(
                recruiter_id=recruiter_id,
                title=filename.replace(".txt", "").replace("_", " ").title(),
                company_name="Sample Corp",
                description=text,
                parsed_data=parsed,
                location="Remote",
                salary_min=50000,
                salary_max=150000,
                embedding=embedding
            )
            db_jobs.append(job)

    # 5. Run Matching
    print("Running initial matching...")
    for job in db_jobs:
        for res in db_resumes:
            score_data = matching_engine.calculate_overall_score(res.parsed_data, job.parsed_data)
            explanation = explanation_generator.generate_match_explanation(
                res.parsed_data, job.parsed_data, score_data
            )
            
            db.save_match(
                resume_id=res.id,
                job_id=job.id,
                scores={
                    "total_score": score_data["total_score"],
                    "skills_match": score_data["breakdown"]["skills_match"],
                    "experience_match": score_data["breakdown"]["experience_match"],
                    "education_match": score_data["breakdown"]["education_match"],
                    "semantic_match": score_data["breakdown"]["semantic_match"]
                },
                details=score_data["details"],
                explanation=explanation
            )

    print("Sample data loaded successfully!")

if __name__ == "__main__":
    load_sample_data()
