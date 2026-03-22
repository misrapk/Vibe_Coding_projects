import streamlit as st
import pandas as pd
from datetime import datetime
from src.frontend.api_client import (
    get_dashboard_analytics, upload_resume, get_my_resumes, 
    delete_resume, get_jobs, apply_to_job, get_my_applications
)

def show_dashboard():
    """PAGE 1: Candidate Dashboard"""
    user = st.session_state.user
    st.markdown(f"## Welcome back, {user['first_name']}! 👋")
    
    with st.spinner("Loading your career overview..."):
        stats_data, error = get_dashboard_analytics()
        if error:
            st.error(f"Error loading dashboard: {error}")
            return
        
        s = stats_data["stats"]
        
        # 1. Quick Stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Resumes", s.get("total_resumes", 0))
        col2.metric("Matches", s.get("total_matches", 0))
        col3.metric("Applications", s.get("applications_submitted", 0))
        col4.metric("Avg Match", f"{s.get('avg_match_score', 0)}%")

    st.markdown("---")
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        # 2. Recommendations
        st.markdown("### 🎯 Jobs you might be interested in")
        jobs, j_error = get_jobs(limit=5)
        if j_error:
            st.error(j_error)
        elif not jobs:
            st.info("No job recommendations yet. Upload a resume to get started!")
        else:
            for job in jobs:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin:0;">{job['title']}</h4>
                                <p style="color: grey; font-size: 0.9rem;">{job['company_name']} • {job['location']}</p>
                            </div>
                            <div class="role-tag" style="background: rgba(79, 70, 229, 0.1); color: #4F46E5;">
                                NEW
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
    with col_side:
        # 3. Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("📤 Upload New Resume"):
            st.session_state.page = "upload_resume"
            st.rerun()
        if st.button("💼 Browse All Jobs"):
            st.session_state.page = "browse_jobs"
            st.rerun()
        if st.button("🎯 View My Matches"):
            st.session_state.page = "job_matches"
            st.rerun()

def show_upload():
    """PAGE 2: Upload Resume"""
    st.markdown("## 📤 Upload Your Resume")
    st.markdown("Get instant AI analysis and unlock tailored job matches.")
    
    uploaded_file = st.file_uploader("Choose a file (PDF or DOCX, max 5MB)", type=["pdf", "docx"])
    
    if uploaded_file:
        if uploaded_file.size > 5 * 1024 * 1024:
            st.error("File size exceeds 5MB limit.")
            return

        if st.button("🚀 Analyze My Resume"):
            with st.status("Processing your career profile...") as status:
                st.write("📤 Uploading to server...")
                result, error = upload_resume(uploaded_file)
                
                if error:
                    status.update(label="Upload Failed", state="error")
                    st.error(error)
                else:
                    st.session_state.last_upload = result
                    status.update(label="Analysis Complete!", state="complete")
                    st.balloons()

    if 'last_upload' in st.session_state:
        res = st.session_state.last_upload
        data = res['parsed_data']
        
        st.success("✅ Resume parsed successfully! Preview the details below.")
        
        with st.expander("👤 Personal Information", expanded=True):
            info = data.get('personal_info', {})
            c1, c2 = st.columns(2)
            c1.text_input("Name", info.get('name', 'N/A'))
            c2.text_input("Email", info.get('email', 'N/A'))
            st.text_input("Phone", info.get('phone', 'N/A'))
            
        with st.expander("💼 Work Experience"):
            for idx, exp in enumerate(data.get('work_experience', [])):
                st.markdown(f"**Experience {idx+1}**")
                st.write(exp.get('description', 'No description found.'))
                st.divider()

        with st.expander("🛠️ Skills"):
            skills = data.get('skills', [])
            if skills:
                st.markdown(" ".join([f'<span class="role-tag" style="margin-right:5px;">{s}</span>' for s in skills]), unsafe_allow_html=True)
            else:
                st.write("No specific skills detected.")

        if st.button("💾 Save and Find Matches"):
            st.session_state.page = "job_matches"
            del st.session_state.last_upload
            st.rerun()

def show_resumes():
    """PAGE 3: My Resumes"""
    st.markdown("## 📋 My Resumes")
    
    resumes, error = get_my_resumes()
    if error:
        st.error(error)
        return
    
    if not resumes:
        st.info("You haven't uploaded any resumes yet.")
        if st.button("Upload Now"):
            st.session_state.page = "upload_resume"
            st.rerun()
        return

    for res in resumes:
        with st.container():
            col_text, col_actions = st.columns([3, 1])
            with col_text:
                st.markdown(f"""
                <div class="card">
                    <h4 style="margin:0;">📄 {res['filename']}</h4>
                    <p style="font-size: 0.8rem; color: grey;">Uploaded on: {res['upload_date'][:10]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_actions:
                if st.button("🔍 Matches", key=f"view_{res['id']}"):
                    st.session_state.selected_resume_id = res['id']
                    st.session_state.page = "job_matches"
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"del_{res['id']}"):
                    st.session_state.confirm_delete = res['id']
    
    if 'confirm_delete' in st.session_state:
        st.warning("⚠️ Are you sure you want to delete this resume? This action cannot be undone.")
        c1, c2 = st.columns(2)
        if c1.button("Yes, Delete"):
            _, err = delete_resume(st.session_state.confirm_delete)
            if err:
                st.error(err)
            else:
                st.success("Deleted!")
                del st.session_state.confirm_delete
                st.rerun()
        if c2.button("Cancel"):
            del st.session_state.confirm_delete
            st.rerun()

def show_matches():
    """PAGE 4: Job Matches"""
    st.markdown("## 🎯 AI Job Matches")
    
    # Simple selector if multiple resumes exist
    resumes, _ = get_my_resumes()
    if not resumes:
        st.info("Please upload a resume first.")
        return
    
    resume_options = {f"{r['filename']} ({r['upload_date'][:10]})": r['id'] for r in resumes}
    selected_idx = 0
    if 'selected_resume_id' in st.session_state:
        for i, (k, v) in enumerate(resume_options.items()):
            if v == st.session_state.selected_resume_id:
                selected_idx = i
                break

    res_label = st.selectbox("Analyze matches for:", list(resume_options.keys()), index=selected_idx)
    resume_id = resume_options[res_label]
    
    st.markdown("---")
    
    # In this demo, we browse available jobs and calculate score on the fly or from persistent matches
    # For now, let's fetch jobs and show them
    jobs, j_error = get_jobs()
    if j_error:
        st.error(j_error)
        return

    for job in jobs:
        # Mocking match score for visual representation if not persistent
        # In real app, we fetch /resumes/{id}/matches
        score = 85 # Mock
        
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin:0;">{job['title']}</h4>
                        <p style="color: grey; margin: 2px 0;">{job['company_name']} • {job['location']}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.2rem; font-weight: 700; color: #4F46E5;">{score}%</span>
                        <p style="font-size: 0.7rem; color: grey;">MATCH SCORE</p>
                    </div>
                </div>
                <div style="margin-top: 10px;">
                    <progress value="{score}" max="100" style="width: 100%; height: 8px; border-radius: 5px;"></progress>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Detail & Apply", key=f"job_{job['id']}"):
                st.session_state.viewing_job_id = job['id']
                st.session_state.viewing_score = score
                
    if 'viewing_job_id' in st.session_state:
        st.divider()
        jid = st.session_state.viewing_job_id
        job = next(j for j in jobs if j['id'] == jid)
        
        st.markdown(f"### Detailed Analysis: {job['title']}")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Why you're a good fit")
            st.info("• Your experience with Python matches the requirements.\n• Your education background aligns perfectly with the role.\n• Relevant project work detected.")
            
            st.markdown("#### Areas to improve")
            st.warning("• Missing cloud certifications (AWS/Azure).\n• Limited experience with Docker mentioned in resume.")
        
        with c2:
            st.markdown("#### Match Breakdown")
            st.progress(0.9, text="Skills Match")
            st.progress(0.7, text="Experience")
            st.progress(1.0, text="Education")
            
        if st.button("🚀 Apply Now", key="apply_btn"):
            res, err = apply_to_job(resume_id, jid)
            if err:
                st.error(err)
            else:
                st.success("Successfully applied!")
                st.balloons()
        
        if st.button("Close Details"):
            del st.session_state.viewing_job_id
            st.rerun()

def show_profile():
    """PAGE 5: Profile & Settings"""
    from src.frontend.components.common import show_profile as common_profile
    common_profile()
    
    st.markdown("### ⚙️ Preferences")
    st.checkbox("Receive daily match alerts via email", value=True)
    st.checkbox("Show my profile to verified recruiters", value=True)
    
    if st.button("Save Preferences"):
        st.success("Preferences updated!")
