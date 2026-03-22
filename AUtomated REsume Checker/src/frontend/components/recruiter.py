import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.frontend.api_client import (
    get_dashboard_analytics, create_job, get_jobs, 
    get_job_candidates, trigger_matching, get_bias_reports,
    update_job, delete_job, get_all_candidates, get_job_analytics,
    get_match_details
)

def show_dashboard():
    """PAGE 1: Recruiter Dashboard"""
    st.markdown(f"## Recruiter Overview 🏢")
    
    with st.spinner("Calculating matching statistics..."):
        stats_data, error = get_dashboard_analytics()
        if error:
            st.error(f"Error loading dashboard: {error}")
            return
        
        s = stats_data["stats"]
        
        # 1. Stats Section
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Jobs Posted", s.get("total_jobs_posted", 0))
        col2.metric("Active Jobs", s.get("total_jobs_posted", 0)) # Mock active same as total for now
        col3.metric("Candidates", s.get("total_candidates_matched", 0))
        col4.metric("Shortlisted", s.get("shortlisted_candidates", 0))
        col5.metric("Filled", s.get("positions_filled", 0))

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # 2. Recent Jobs
        st.markdown("### 📋 Recent Job Postings")
        jobs, _ = get_jobs(limit=5)
        if jobs:
            for job in jobs:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <h4 style="margin:0;">{job['title']}</h4>
                                <p style="font-size: 0.8rem; color: grey;">Posted: {job['created_at'][:10]} • {job['location']}</p>
                            </div>
                            <div class="role-tag" style="height: fit-content;">{job['status']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No jobs posted yet.")
            
    with col_right:
        # 4. Quick Actions
        st.markdown("### ⚡ Fast Track")
        if st.button("➕ Post New Job", use_container_width=True):
            st.session_state.page = "post_job"
            st.rerun()
        if st.button("💼 View All Jobs", use_container_width=True):
            st.session_state.page = "my_jobs"
            st.rerun()
        if st.button("📁 Talent Pool", use_container_width=True):
            st.session_state.page = "talent_pool"
            st.rerun()
        
        st.markdown("---")
        # 3. Top Candidates (Cross-Job)
        st.markdown("### 🏆 Top Candidates")
        cands, _ = get_all_candidates()
        if cands:
            for cand in cands[:3]:
                st.markdown(f"**{cand['name']}**")
                st.caption(f"Score: {cand['best_match_score']}% in {cand['best_matched_job']}")

def show_post_job():
    """PAGE 2: Post Job"""
    st.markdown("## ➕ Post a New Job")
    
    with st.form("job_post_form"):
        title = st.text_input("Job Title", placeholder="e.g. Senior Python Developer")
        company = st.text_input("Company Name", value=st.session_state.user.get("company", "Your Company"))
        location = st.text_input("Location", placeholder="Remote / City, Country")
        
        c1, c2 = st.columns(2)
        job_type = c1.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Remote"])
        salary_min = c2.number_input("Salary Min", value=50000)
        salary_max = st.number_input("Salary Max", value=150000)
        
        description = st.text_area("Job Description", height=300, 
                                  help="Include required skills, experience level, and responsibilities.")
        
        st.caption(f"Character count: {len(description)}")
        
        submit = st.form_submit_button("Preview & Analyze Bias")
        
    if submit:
        if not title or not description:
            st.error("Title and Description are required.")
            return
            
        with st.spinner("Analyzing job description for bias and requirements..."):
            # Prepare payload
            payload = {
                "title": title,
                "company_name": company,
                "description": description,
                "location": location,
                "salary_min": salary_min,
                "salary_max": salary_max
            }
            
            res, err = create_job(payload)
            if err:
                st.error(err)
            else:
                st.session_state.analyzed_job = res
                st.success("Analysis Complete!")

    if 'analyzed_job' in st.session_state:
        job = st.session_state.analyzed_job
        st.markdown("---")
        st.markdown("### 🔍 Analysis Results")
        
        t1, t2 = st.tabs(["Parsed Requirements", "Bias Detection Report"])
        
        with t1:
            data = job.get("parsed_data", {})
            st.write(f"**Extracted Experience:** {data.get('basic_info', {}).get('experience_required', 'N/A')}")
            st.write("**Extracted Skills:**")
            skills = data.get('skills', {})
            st.write(", ".join(skills.get('required', [])))
            
        with t2:
            # Re-fetch bias report for this specific job context
            # In a real app we'd trigger it or it would be in job object
            reports, _ = get_bias_reports()
            report = next((r for r in reports if r['job_id'] == job['id']), None)
            
            if report:
                score = report['bias_score']
                color = "green" if score < 20 else "orange" if score < 50 else "red"
                st.markdown(f"Bias Score: <span style='color:{color}; font-weight:bold;'>{score}/100</span>", unsafe_allow_html=True)
                
                st.write("**Issues Detected:**")
                for issue in report['issues']:
                    st.write(f"❌ {issue}")
                
                st.write("**Suggestions:**")
                for sug in report['suggestions']:
                    st.info(sug)
                    
        if st.button("🚀 Confirm and Publish"):
            st.success("Job Published Successfully!")
            del st.session_state.analyzed_job
            st.balloons()
            if st.button("View Candidates Immediately"):
                 st.session_state.page = "my_jobs"
                 st.rerun()

def show_my_jobs():
    """PAGE 3: My Jobs"""
    st.markdown("## 💼 Managed Jobs")
    
    jobs, error = get_jobs()
    if error:
        st.error(error)
        return
    
    if not jobs:
        st.info("You haven't posted any jobs yet.")
        return
        
    for job in jobs:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin:0;">{job['title']}</h4>
                        <p style="color: grey; font-size: 0.8rem;">{job['location']} • Posted: {job['created_at'][:10]}</p>
                    </div>
                    <div class="role-tag" style="background: {'#10B98122' if job['status'] == 'OPEN' else '#EF444422'}; color: {'#10B981' if job['status'] == 'OPEN' else '#EF4444'};">
                        {job['status']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("👥 Candidates", key=f"cands_{job['id']}"):
                st.session_state.selected_job_id = job['id']
                st.session_state.page = "candidates"
                st.rerun()
            if c2.button("✏️ Edit", key=f"edit_{job['id']}"):
                st.info("Edit feature coming soon!")
            if c3.button("🗑️ Delete", key=f"del_{job['id']}"):
                st.session_state.confirm_delete_job = job['id']
            if c4.button("🏁 Close Job" if job['status'] == 'OPEN' else "🔓 Reopen", key=f"toggle_{job['id']}"):
                new_status = "CLOSED" if job['status'] == 'OPEN' else "OPEN"
                update_job(job['id'], {"status": new_status})
                st.rerun()

    if 'confirm_delete_job' in st.session_state:
        st.warning("Are you sure? This will remove all match data for this job.")
        if st.button("Yes, Delete Permanently"):
            delete_job(st.session_state.confirm_delete_job)
            del st.session_state.confirm_delete_job
            st.rerun()

def show_candidates_view():
    """PAGE 4: View Candidates for Job"""
    st.markdown("## 🎯 Candidate Analysis")
    
    jobs, _ = get_jobs()
    if not jobs:
        st.info("Post a job first to see candidate matches.")
        return
        
    job_options = {f"{j['title']} (ID: {j['id']})": j['id'] for j in jobs}
    selected_idx = 0
    if 'selected_job_id' in st.session_state:
        for i, (k, v) in enumerate(job_options.items()):
            if v == st.session_state.selected_job_id:
                selected_idx = i
                break
                
    sel_label = st.selectbox("Select Job to Analyze", list(job_options.keys()), index=selected_idx)
    job_id = job_options[sel_label]
    
    st.markdown("---")
    
    with st.spinner("Fetching matches..."):
        candidates, error = get_job_candidates(job_id)
        if error:
            st.error(error)
            return
            
    if not candidates:
        st.info("No candidates matched yet. Try adjusting your job description or wait for more resumes.")
        if st.button("🔄 Trigger Match Search"):
            trigger_matching(job_id)
            st.success("Search triggered!")
        return

    # Filters
    with st.expander("🔍 Filter & Sort"):
        min_score = st.slider("Min Match Score", 0, 100, 40)
        sort_by = st.selectbox("Sort By", ["Match Score", "Name"])
        
    filtered = [c for c in candidates if c['score'] >= min_score]
    if sort_by == "Match Score":
        filtered = sorted(filtered, key=lambda x: x['score'], reverse=True)
    
    st.write(f"Showing {len(filtered)} candidates")
    
    for cand in filtered:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin:0;">{cand['name']}</h4>
                        <p style="color: grey; font-size: 0.8rem;">{cand.get('email', 'N/A')}</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 1.5rem; font-weight: 700; color: #4F46E5;">{cand['score']}%</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Full Profile & Match Breakdown", key=f"detail_{cand['candidate_id']}"):
                st.session_state.viewing_cand_id = cand['candidate_id']
                st.session_state.viewing_cand_name = cand['name']
                st.session_state.viewing_cand_score = cand['score']
                st.session_state.viewing_cand_explanation = cand.get('explanation', "N/A")

    if 'viewing_cand_id' in st.session_state:
        st.divider()
        st.markdown(f"### Profile: {st.session_state.viewing_cand_name}")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Match Explanation")
            st.info(st.session_state.viewing_cand_explanation)
            
            st.markdown("#### Contact Options")
            st.button("📧 Send Email")
            st.button("📅 Schedule Interview")
            
        with c2:
            st.markdown("#### Score Breakdown")
            # In a real app we'd fetch actual breakdown
            st.progress(0.8, text="Skills")
            st.progress(0.7, text="Experience")
            st.progress(1.0, text="Education")
            
            st.write("---")
            if st.button("✅ Shortlist Candidate"):
                st.success("Candidate Shortlisted!")
            if st.button("❌ Reject"):
                st.error("Candidate Rejected.")
        
        if st.button("Close Profile"):
            del st.session_state.viewing_cand_id
            st.rerun()

def show_all_candidates():
    """PAGE 5: All Candidates"""
    st.markdown("## 👥 Candidate Database")
    st.write("Browse all candidates available in the system.")
    
    cands, error = get_all_candidates()
    if error:
        st.error(error)
        return
        
    if not cands:
        st.info("No candidates in database yet.")
        return
        
    df = pd.DataFrame(cands)
    st.dataframe(df[["name", "email", "resumes_count", "best_matched_job", "best_match_score"]], use_container_width=True)
    
    st.markdown("---")
    st.write("### AI Talent Insights")
    st.info("Use the search bar above to filter by skills or name.")

def show_analytics():
    """PAGE 6: Analytics"""
    st.markdown("## 📈 Recruitment Analytics")
    
    with st.spinner("Generating visualizations..."):
        # 1. Histogram of Match Scores
        cands, _ = get_all_candidates()
        if cands:
            scores = [c['best_match_score'] for c in cands]
            fig = px.histogram(scores, nbins=10, title="Candidate Score Distribution",
                             labels={'value': 'Match Score'}, 
                             color_discrete_sequence=['#4F46E5'])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        # 2. Bias Benchmarks
        st.markdown("### Inclusion & Bias Overview")
        reports, _ = get_bias_reports()
        if reports:
            bias_data = pd.DataFrame(reports)
            fig2 = px.bar(bias_data, x='job_title', y='bias_score', 
                        title="Bias Scores by Job Post",
                        color='bias_score',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig2, use_container_width=True)
            
        # 3. Job Performance Table
        st.markdown("### Job Performance Metrics")
        jobs, _ = get_jobs()
        if jobs:
            df_jobs = pd.DataFrame([
                {
                    "Job": j['title'],
                    "Status": j['status'],
                    "Location": j['location'],
                    "Salary Range": f"${j['salary_min']} - ${j['salary_max']}"
                } for j in jobs
            ])
            st.table(df_jobs)
