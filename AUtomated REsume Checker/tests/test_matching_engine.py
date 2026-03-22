from src.backend.matching_engine import MatchingEngine
from src.backend.skills_engine import SkillsEngine
from src.backend.semantic_matcher import SemanticMatcher
import json

def test_matching_engine():
    skills_engine = SkillsEngine()
    semantic_matcher = SemanticMatcher()
    engine = MatchingEngine(skills_engine, semantic_matcher)
    
    resume_data = {
        "personal_info": {"name": "Test Candidate"},
        "skills": ["Python", "JavaScript", "React", "Docker", "SQL", "Git"],
        "work_experience": {
            "description": "Software Engineer at Tech Co from 2018 to 2022. Worked on scalable backend services with Python."
        },
        "education": {
            "description": "Bachelor of Science in Computer Science",
            "details": {"degrees": ["Bachelor"]}
        },
        "projects": "Built an AI resume matcher.",
        "certifications": "AWS Certified Developer",
        "raw_text": "Python developer with 4 years experience. Knows React and Docker."
    }
    
    jd_data = {
        "basic_info": {
            "job_title": "Senior Python Developer",
            "experience_required": "5+ years",
            "seniority": "Senior"
        },
        "skills": {
            "required": ["Python", "Docker", "FastAPI"],
            "preferred": ["Kubernetes", "Redis"]
        },
        "education": "Master's in Computer Science preferred",
        "details": {
            "responsibilities": "Lead a team of developers and build robust APIs with FastAPI."
        },
        "raw_text": "Looking for a Senior Python Developer with 5 years experience."
    }
    
    result = engine.calculate_overall_score(resume_data, jd_data)
    print(json.dumps(result, indent=2))
    
    assert "total_score" in result
    assert result["breakdown"]["skills_match"] > 0
    print("\nMatching Engine test passed!")

if __name__ == "__main__":
    test_matching_engine()
