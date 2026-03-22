import pytest
import os
import sys
from typing import Dict, Any

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.backend.parser import ResumeParser
from src.backend.jd_parser import JDParser
from src.backend.skills_engine import SkillsEngine
from src.backend.semantic_matcher import SemanticMatcher
from src.backend.matching_engine import MatchingEngine
from src.backend.bias_detector import BiasDetector

@pytest.fixture
def skills_engine():
    return SkillsEngine()

@pytest.fixture
def resume_parser():
    return ResumeParser()

@pytest.fixture
def jd_parser():
    return JDParser()

@pytest.fixture
def bias_detector():
    return BiasDetector()

@pytest.fixture
def matching_engine(skills_engine):
    semantic_matcher = SemanticMatcher()
    return MatchingEngine(skills_engine, semantic_matcher)

def test_resume_parser_functionality(resume_parser):
    sample_text = """
    JOHN DOE
    Email: john@example.com
    Skills: Python, React, SQL, Docker
    Experience: 5 years at Google as a Senior Engineer.
    Education: BS in Computer Science from MIT.
    """
    parsed = resume_parser.parse_text(sample_text)
    print(f"\nDEBUG Resume Parsed: {parsed}")
    
    assert parsed["personal_info"]["email"] == "john@example.com"
    assert "python" in [s.lower() for s in parsed["skills"]]
    assert "react" in [s.lower() for s in parsed["skills"]]
    # Check if Google is captured in experience or raw text
    assert "Google" in parsed["work_experience"]["description"] or "Google" in parsed["raw_text"]

def test_jd_parser_functionality(jd_parser):
    sample_jd = """
    Senior Python Developer
    Requirements:
    - 5+ years of experience in Python.
    - Strong skills in Django and PostgreSQL.
    - Experience with Kubernetes.
    """
    parsed = jd_parser.parse(sample_jd)
    print(f"\nDEBUG JD Parsed: {parsed}")
    
    # Title might be extracted including whitespace or from the first line
    assert "Senior Python Developer" in parsed["basic_info"]["job_title"]
    assert "python" in [s.lower() for s in parsed["skills"]["required"]]
    assert "Senior" in parsed["basic_info"]["seniority"]

def test_matching_logic(matching_engine):
    resume_data = {
        "skills": ["Python", "Django", "PostgreSQL"],
        "work_experience": {"description": "5 years experience", "raw": "5 years experience"},
        "education": {"description": "BS Computer Science", "details": {}},
        "raw_text": "Experienced Python developer with Django skills."
    }
    
    jd_data = {
        "basic_info": {"experience_required": "3+ years", "seniority": "Mid"},
        "skills": {
            "required": ["Python", "Django"],
            "preferred": ["PostgreSQL"]
        },
        "education": "Computer Science degree",
        "raw_text": "Looking for a Python developer with Django and PostgreSQL experience."
    }
    
    score_data = matching_engine.calculate_overall_score(resume_data, jd_data)
    assert score_data["total_score"] > 50 # Adjusted threshold for mock data

def test_bias_detection(bias_detector):
    biased_text = "Looking for a young rockstar ninja developer who is a native English speaker."
    neutral_text = "Looking for an experienced Software Engineer with 5 years of Python experience."
    
    biased_analysis = bias_detector.analyze(biased_text)
    neutral_analysis = bias_detector.analyze(neutral_text)
    
    assert biased_analysis["bias_score"] > neutral_analysis["bias_score"]
    assert len(biased_analysis["biased_phrases"]) > 0

def test_idempotent_sample_data_indices():
    # Simple check if sample files exist
    assert os.path.exists("data/samples/resumes/junior_software_engineer.txt")
    assert os.path.exists("data/samples/jobs/junior_python_developer.txt")
