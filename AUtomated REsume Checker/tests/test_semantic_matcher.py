from src.backend.semantic_matcher import SemanticMatcher
import json

def test_semantic_matcher():
    matcher = SemanticMatcher()
    
    # Sample Resumes
    resumes = [
        ("res1", "Experienced Python developer with a strong background in Machine Learning and Data Science. Proficient in TensorFlow, PyTorch, and NLP.", {"name": "Alice ML"}),
        ("res2", "Web Developer specializing in Frontend technologies like React, Vue, and Tailwind CSS. Deep knowledge of JavaScript and UI/UX design.", {"name": "Bob Frontend"}),
        ("res3", "DevOps Engineer with 10 years of experience in AWS, Kubernetes, and Docker. Expert in CI/CD pipelines and infrastructure as code.", {"name": "Charlie DevOps"})
    ]
    
    for rid, text, meta in resumes:
        matcher.add_resume(rid, text, meta)
        
    # Sample Jobs
    jobs = [
        ("job1", "Looking for an AI Engineer to build NLP models using Python and PyTorch."),
        ("job2", "Fullstack Developer needed for React and Node.js projects."),
        ("job3", "Senior DevOps Specialist for AWS cloud management.")
    ]
    
    for jid, text in jobs:
        matcher.add_job(jid, text)
        
    # Test 1: Search Resumes for AI Job
    print("--- Searching Resumes for AI Job (job1) ---")
    results = matcher.search_resumes(jobs[0][1], top_k=2)
    print(json.dumps(results, indent=2))
    assert results[0]["resume_id"] == "res1"
    
    # Test 2: Search Jobs for Bob (Frontend)
    print("\n--- Searching Jobs for Bob Frontend (res2) ---")
    results = matcher.search_jobs(resumes[1][1], top_k=2)
    print(json.dumps(results, indent=2))
    assert results[0]["job_id"] == "job2"
    
    # Test 3: Direct Match Score
    score = matcher.calculate_match_score(resumes[2][1], jobs[2][1])
    print(f"\n--- Direct Match Score (Charlie vs Job3): {score} ---")
    assert score > 70

if __name__ == "__main__":
    test_semantic_matcher()
    print("\nSemantic Matcher tests passed!")
