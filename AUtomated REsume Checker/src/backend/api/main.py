from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.routes import auth, resumes, jobs, matches, analytics, utils, applications

app = FastAPI(
    title="AI Resume Matcher API",
    description="Backend API with JWT Authentication for AI-powered resume screening.",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:8501", # Streamlit default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(matches.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(utils.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Resume Matcher API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
