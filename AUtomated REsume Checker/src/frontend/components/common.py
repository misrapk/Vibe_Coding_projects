import streamlit as st
from src.frontend.api_client import get_jobs, get_me

def show_browse_jobs():
    st.subheader("Available Opportunities")
    st.write("Browse current job openings in the system.")
    
    jobs, error = get_jobs()
    if error:
        st.error(f"Could not load jobs: {error}")
    elif not jobs:
        st.info("No active job postings available at the moment.")
    else:
        for job in jobs:
            st.markdown(f"""
            <div class="card">
                <h3 style="margin-top:0;">{job['title']}</h3>
                <p style="font-size: 0.9rem; opacity: 0.8;">
                    🏢 <strong>{job['company_name']}</strong> | 📍 {job['location']}
                </p>
                <p style="margin: 1rem 0;">{job['description'][:200]}...</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #4F46E5;">
                        💰 ${job['salary_min']:,} - ${job['salary_max']:,}
                    </span>
                    <span class="role-tag" style="background: rgba(79, 70, 229, 0.1); color: #4F46E5; border-color: rgba(79, 70, 229, 0.2);">
                        {job.get('status', 'ACTIVE').upper()}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.authenticated:
                st.caption("Login to apply and see match details.")

def show_profile():
    st.subheader("User Profile")
    
    user = st.session_state.user
    if not user:
        st.warning("Please log in to view your profile")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**First Name:** {user['first_name']}")
        st.write(f"**Last Name:** {user['last_name']}")
    with col2:
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** {user['role'].capitalize()}")
    
    st.divider()
    st.write("### Account Settings")
    if st.button("Change Password"):
        st.info("Password change feature coming soon!")
