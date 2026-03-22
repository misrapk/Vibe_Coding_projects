import streamlit as st
import os
import sys

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from src.frontend.api_client import get_me

# Page configuration
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'token' not in st.session_state:
    st.session_state.token = None
if 'page' not in st.session_state:
    st.session_state.page = "browse_jobs"

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-image: linear-gradient(180deg, rgba(79, 70, 229, 0.05) 0%, rgba(244, 63, 94, 0.05) 100%);
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }
    
    /* Premium Cards */
    .card {
        background: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: rgba(79, 70, 229, 0.3);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: var(--text-color);
        font-weight: 700 !important;
    }
    
    .stMarkdown p {
        color: var(--text-color);
        opacity: 0.9;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338CA 0%, #6D28D9 100%);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
    }

    /* Status Indicators */
    .role-tag {
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    /* Hide Streamlit default link icon */
    .stMarkdown a {
        text-decoration: none;
        color: #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# Navigation sidebar logic
def sidebar_nav():
    with st.sidebar:
        st.markdown(f"### 🚀 AI Matcher")
        
        if st.session_state.authenticated:
            user = st.session_state.user
            st.markdown(f"**{user['first_name']} {user['last_name']}**")
            st.markdown(f'<span class="role-tag">{user["role"].upper()}</span>', unsafe_allow_html=True)
            st.write("---")
            
            nav_options = {
                "🏠 Dashboard": "dashboard",
                "💼 Browse Jobs": "browse_jobs",
                "📄 Upload Resume": "upload_resume" if user['role'] == 'candidate' else None,
                "📋 My Resumes": "my_resumes" if user['role'] == 'candidate' else None,
                "🎯 Job Matches": "job_matches" if user['role'] == 'candidate' else None,
                "➕ Post Job": "post_job" if user['role'] == 'recruiter' else None,
                "💼 My Jobs": "my_jobs" if user['role'] == 'recruiter' else None,
                "👥 Candidates": "candidates" if user['role'] == 'recruiter' else None,
                "📁 Talent Pool": "talent_pool" if user['role'] == 'recruiter' else None,
                "📊 Analytics": "analytics" if user['role'] == 'recruiter' else None,
                "👤 Profile": "profile",
            }
            
            # Filter None values
            nav_options = {k: v for k, v in nav_options.items() if v is not None}
            
            selection = st.radio("Navigation", list(nav_options.keys()), index=list(nav_options.keys()).index(next(k for k, v in nav_options.items() if v == st.session_state.page)) if st.session_state.page in nav_options.values() else 0)
            st.session_state.page = nav_options[selection]
            
            st.write("---")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.token = None
                st.session_state.page = "browse_jobs" # Reset page on logout
                st.rerun()
        else:
            # Determine initial selection for unauthenticated users
            initial_selection_index = 0
            if st.session_state.page == "login":
                initial_selection_index = 1
            elif st.session_state.page == "register":
                initial_selection_index = 2

            selection = st.radio("Navigation", ["Browse Jobs", "Login", "Register"], index=initial_selection_index)
            st.session_state.page = selection.lower().replace(" ", "_")

# Main entry point
def main():
    sidebar_nav()
    
    # Import components here to avoid circular imports if needed
    from src.frontend.components import auth, candidate, recruiter, common
    
    page = st.session_state.page
    
    if not st.session_state.authenticated:
        if page == "login":
            auth.show_login()
        elif page == "register":
            auth.show_register()
        else:  # browse_jobs
            common.show_browse_jobs()
    else:
        # Authenticated user routing
        if page == "dashboard":
            if st.session_state.user['role'] == 'candidate':
                candidate.show_dashboard()
            else:
                recruiter.show_dashboard()
        elif page == "browse_jobs":
            common.show_browse_jobs()
        elif page == "upload_resume":
            candidate.show_upload()
        elif page == "my_resumes":
            candidate.show_resumes()
        elif page == "job_matches":
            candidate.show_matches()
        elif page == "post_job":
            recruiter.show_post_job()
        elif page == "my_jobs":
            recruiter.show_my_jobs()
        elif page == "candidates":
            recruiter.show_candidates_view()
        elif page == "talent_pool":
            recruiter.show_all_candidates()
        elif page == "analytics":
            recruiter.show_analytics()
        elif page == "profile":
            if st.session_state.user['role'] == 'candidate':
                candidate.show_profile()
            else:
                common.show_profile()

if __name__ == "__main__":
    main()
