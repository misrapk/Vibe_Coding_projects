import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

def api_call(method, endpoint, data=None, files=None, params=None, use_json=True):
    """Make API call with authentication"""
    headers = {}
    if 'token' in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, files=files, data=data, params=params)
            elif use_json:
                response = requests.post(url, headers=headers, json=data, params=params)
            else:
                response = requests.post(url, headers=headers, data=data, params=params)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, params=params)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, params=params)
        else:
            return None, f"Unsupported method: {method}"
        
        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            try:
                error_msg = response.json().get("detail", "An error occurred")
            except:
                error_msg = f"HTTP {response.status_code}: {response.text}"
            return None, error_msg
    except Exception as e:
        return None, str(e)

# --- Authentication ---

def login(email, password):
    # FastAPI OAuth2 uses form data for login
    data = {"username": email, "password": password}
    return api_call("POST", "/auth/login", data=data, use_json=False)

def register(email, password, first_name, last_name, role):
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role
    }
    return api_call("POST", "/auth/register", data=payload)

def get_me():
    return api_call("GET", "/auth/me")

# --- Resumes ---

def upload_resume(file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    return api_call("POST", "/resumes/upload", files=files)

def get_my_resumes():
    return api_call("GET", "/resumes/my")

def delete_resume(resume_id):
    return api_call("DELETE", f"/resumes/{resume_id}")

# --- Jobs ---

def create_job(job_data):
    return api_call("POST", "/jobs/", data=job_data)

def get_jobs(skip=0, limit=100):
    return api_call("GET", "/jobs/", params={"skip": skip, "limit": limit})

def update_job(job_id, job_data):
    return api_call("PUT", f"/jobs/{job_id}", data=job_data)

def delete_job(job_id):
    return api_call("DELETE", f"/jobs/{job_id}")

def get_job_candidates(job_id, min_score=0.0):
    return api_call("GET", f"/jobs/{job_id}/candidates", params={"min_score": min_score})

# --- Matching & Feedback ---

def trigger_matching(job_id):
    return api_call("POST", f"/matches/trigger/{job_id}")

def get_match_details(match_id):
    return api_call("GET", f"/matches/{match_id}")

def submit_feedback(match_id, action, notes):
    payload = {"action": action, "notes": notes}
    return api_call("POST", f"/matches/{match_id}/feedback", data=payload)

# --- Analytics ---

def get_dashboard_analytics():
    return api_call("GET", "/analytics/dashboard")

def get_job_analytics(job_id):
    return api_call("GET", f"/analytics/jobs/{job_id}/stats")

def get_bias_reports():
    return api_call("GET", "/analytics/bias-reports")

# --- Applications ---

def apply_to_job(resume_id, job_id):
    payload = {"resume_id": resume_id, "job_id": job_id}
    return api_call("POST", "/applications/", data=payload)

def get_my_applications():
    return api_call("GET", "/applications/my")

def get_all_candidates():
    # In this simplified version, candidates are users with the CANDIDATE role
    # but specifically those who have uploaded resumes.
    return api_call("GET", "/analytics/candidates/all")

# --- Utilities ---

def get_health():
    return api_call("GET", "/health")

def search_skills(query, limit=10):
    return api_call("GET", "/skills/search", params={"q": query, "limit": limit})
