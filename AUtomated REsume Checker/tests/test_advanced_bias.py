from src.backend.bias_detector import BiasDetector
import json

def test_bias_detector():
    detector = BiasDetector()
    
    # 1. Bias Detection Test
    jd_text = """
    Looking for a rockstar developer who is highly competitive. 
    He should be a recent graduate from a top university. 
    Must be a native English speaker. 
    We work hard and play hard.
    """
    
    results = detector.analyze(jd_text)
    print("--- Bias Report ---")
    print(json.dumps(results, indent=2))
    
    assert results["bias_score"] > 30
    assert any(b["type"] == "Gender Bias" for b in results["biased_phrases"])
    assert any(b["type"] == "Age Bias" for b in results["biased_phrases"])
    
    # 2. Anonymization Test
    resume_data = {
        "personal_info": {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "555-0199",
            "linkedin": "linkedin.com/in/janedoe"
        },
        "education": {
            "description": "B.S. in Computer Science, 2018",
            "details": {"graduation_year": "2018"}
        },
        "work_experience": {
            "description": "Software Engineer at Google. Jane worked on search algorithms."
        },
        "raw_text": "Jane Doe is a software engineer with 5 years experience."
    }
    
    anonymized = detector.anonymize_resume(resume_data)
    print("\n--- Anonymized Resume ---")
    print(json.dumps(anonymized, indent=2))
    
    assert "[REDACTED NAME]" in anonymized["personal_info"]["name"]
    assert "[REDACTED YEAR]" in anonymized["education"]["details"]["graduation_year"]
    # check for name redaction in text if spaCy picked it up
    assert "[PERSON]" in anonymized["raw_text"] or "Jane" not in anonymized["raw_text"]

if __name__ == "__main__":
    test_bias_detector()
    print("\nBias and Anonymization tests passed!")
