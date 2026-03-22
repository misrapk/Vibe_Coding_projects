from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from src.backend.api.deps import get_db
from src.backend.api.schemas import HealthStatus, SkillSearchResponse
from src.backend.skills_engine import SkillsEngine
from datetime import datetime
import os

router = APIRouter(prefix="", tags=["utility"])

skills_engine = SkillsEngine()

@router.get("/health", response_model=HealthStatus)
def health_check(db: Session = Depends(get_db)):
    """Checks the health of various system components."""
    # Check DB
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Storage
    upload_dir = "data/uploads/resumes"
    storage_status = "ok" if os.path.exists(upload_dir) and os.access(upload_dir, os.W_OK) else "error: no write access"
    
    status = "healthy" if db_status == "ok" and storage_status == "ok" else "degraded"
    
    return {
        "status": status,
        "database": db_status,
        "storage": storage_status,
        "timestamp": datetime.utcnow()
    }

@router.get("/skills/search", response_model=List[SkillSearchResponse])
def search_skills(q: str = Query(..., min_length=1)):
    """Simple skill search for autocompletion."""
    # In a real app, this would query a skills database.
    # Here we'll search through our engine's known skills or extracted skills.
    # For now, let's use the SkillsEngine's knowledge base.
    q_lower = q.lower()
    matches = []
    
    # Simulate a search across known skill categories
    # This is a bit of a hack since SkillsEngine doesn't export the full list easily
    # But we can simulate with a set of common skills.
    common_skills = [
        "Python", "Java", "Javascript", "React", "Angular", "Vue", "Node.js", "Express", 
        "Django", "Flask", "FastAPI", "SQL", "PostgreSQL", "MongoDB", "Redis", "Docker", 
        "Kubernetes", "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning", "NLP",
        "Data Science", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch",
        "CI/CD", "Git", "GitHub", "Jira", "Agile", "Scrum", "TDD", "Unit Testing"
    ]
    
    for skill in common_skills:
        if q_lower in skill.lower():
            matches.append({"skill_name": skill, "category": "General Tech"})
            
    return matches[:10]
