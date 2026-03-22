from src.backend.skills_engine import SkillsEngine
import json

def test_skills_engine():
    engine = SkillsEngine()
    
    # Test text with various skills and aliases
    resume_text = """
    I am a Senior Software Engineer with expertise in Python, JS, and React. 
    I have built microservices using Node.js and deployed them on AWS using Docker and K8s. 
    I use Git for version control and Jira for project management.
    Also familiar with Postgres and SQL.
    """
    
    jd_req_skills = {"Python", "FastAPI", "AWS", "PostgreSQL", "Docker", "Git"}
    jd_pref_skills = {"Kubernetes", "Redis", "Machine Learning"}
    
    # 1. Extraction Test
    extracted = engine.extract_skills(resume_text)
    print("--- Extracted Skills ---")
    print(json.dumps(extracted, indent=2))
    
    # Flatten candidate skills for matching
    candidate_skills = set([s for cat in extracted.values() for s in cat])
    
    # 2. Matching Test
    match_results = engine.match_skills(candidate_skills, jd_req_skills, jd_pref_skills)
    print("\n--- Match Results ---")
    print(json.dumps(match_results, indent=2))
    
    assert "Python" in match_results["matched_required"]
    assert "JS" not in match_results["matched_required"] # JS is JavaScript canonical
    assert match_results["score"] > 50

if __name__ == "__main__":
    test_skills_engine()
    print("\nTests passed!")
