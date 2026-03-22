from src.backend.jd_parser import JDParser
import json

def test_jd_parser():
    jd_text = """
Senior Python Developer
We are looking for a Senior Python Developer to join our fast-paced Startup.

Responsibilities:
- Build scalable backend services with Django and FastAPI.
- Collaborate with frontend teams using React.
- Mentor junior developers.

Requirements:
- 5+ years of experience in Python development.
- Strong knowledge of PostgreSQL and Redis.
- Experience with AWS and Docker.
- Must have a Bachelor's degree in Computer Science.

Preferred:
- Experience with Kubernetes is a plus.
- Knowledge of Machine Learning.

Benefits:
- Competitive salary: $120k - $150k
- Remote work options.
- Health insurance.
    """
    
    parser = JDParser()
    result = parser.parse(jd_text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_jd_parser()
