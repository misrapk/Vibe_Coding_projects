import subprocess
import sys
import os

def main():
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        
    print("Starting AI Resume Screening and Job Matching System...")
    print("Everything is running locally and for FREE.")
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "src/frontend/app.py"
        ])
    except KeyboardInterrupt:
        print("\nStopping application...")

if __name__ == "__main__":
    main()
