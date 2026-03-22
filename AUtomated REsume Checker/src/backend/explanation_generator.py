from typing import Dict, List, Any, Optional

class ExplanationGenerator:
    def __init__(self):
        # Resource mapping for suggestions
        self.skill_resources = {
            "python": "Consider Python courses on Coursera, Udemy, or freeCodeCamp. Practice on LeetCode.",
            "aws": "AWS offers a Free Tier and training at AWS Skill Builder. Look for 'AWS Cloud Practitioner' resources.",
            "docker": "Docker's official documentation has great 'Getting Started' guides.",
            "kubernetes": "Check out 'Kubernetes for Beginners' on YouTube or official tutorials (Minikube).",
            "react": "React official docs (React.dev) and freeCodeCamp are excellent for learning React.",
            "sql": "Practice SQL on Mode Analytics or SQLZoo.",
            "machine learning": "Andrew Ng's Machine Learning Specialization on Coursera is a gold standard.",
            "django": "The official Django tutorial is very comprehensive for building web apps.",
            "fastapi": "FastAPI's interactive docs are the best place to start learning.",
            "git": "Learn Git workflows via 'Git Immersion' or GitHub's interactive guides."
        }

    def generate_match_explanation(self, candidate_data: Dict[str, Any], jd_data: Dict[str, Any], score_details: Dict[str, Any]) -> str:
        """Generates a high-level verbal explanation of the match score."""
        score = score_details["total_score"]
        name = candidate_data.get("personal_info", {}).get("name", "The candidate")
        matched_req = score_details["details"].get("matched_required_skills", [])
        missing_req = score_details["details"].get("missing_required_skills", [])
        exp_gap = score_details["details"].get("experience_gap", "")
        
        # Determine match level
        if score >= 80:
            summary = f"**{name}** is an **excellent match** for this position with high alignment across all key criteria."
            points = [
                f"Matches {len(matched_req)} out of {len(matched_req) + len(missing_req)} required skills, including key strengths in {', '.join(matched_req[:3])}.",
                f"Work experience is highly relevant and {exp_gap.lower()}.",
                f"Education background solidifies their technical foundations for this role."
            ]
        elif score >= 60:
            summary = f"**{name}** is a **good match** with a strong foundation, though there are a few areas for development."
            points = [
                f"Demonstrates proficiency in {', '.join(matched_req[:3]) if matched_req else 'several key areas'}.",
                f"Most relevant strengths identified: {', '.join(matched_req[:5]) if matched_req else 'N/A'}.",
                f"Areas to develop: Consider building expertise in {', '.join(missing_req[:3]) if missing_req else 'specialized tools requested'}."
            ]
        else:
            summary = f"**{name}** may not be the optimal fit at this time, but shows potential in specific areas."
            points = [
                f"Strengths identified in {', '.join(matched_req[:3]) if matched_req else 'fundamental areas'}.",
                f"Primary gaps: Missing specific requirements in {', '.join(missing_req[:3]) if missing_req else 'key technologies'}.",
                f"Suggested focus: Targeted learning in missing required skills and hands-on projects."
            ]

        explanation = summary + "\n\n" + "\n".join([f"- {p}" for p in points])
        return explanation

    def generate_detailed_analysis(self, score_details: Dict[str, Any]) -> Dict[str, str]:
        """Generates formatted sections for detailed analysis."""
        details = score_details["details"]
        breakdown = score_details["breakdown"]
        
        skills_text = f"""**Skills Match: {breakdown['skills_match']}/45**
✓ Matched Required: {', '.join(details['matched_required_skills']) or 'None'}
✗ Missing Required: {', '.join(details['missing_required_skills']) or 'None'}
★ Bonus Strengths: {details.get('bonus_skills_count', 0)} additional relevant skills found"""

        exp_text = f"""**Experience Match: {breakdown['experience_match']}/30**
- Status: {details['experience_gap']}
- Relevance: Based on semantic analysis, the previous experience has {breakdown['semantic_match'] / 10 * 100:.1f}% alignment with job responsibilities."""

        edu_text = f"""**Education Match: {breakdown['education_match']}/15**
- Status: {details['education_match']}"""

        return {
            "skills": skills_text,
            "experience": exp_text,
            "education": edu_text
        }

    def generate_improvement_suggestions(self, score_details: Dict[str, Any]) -> List[str]:
        """Generates personalized actionable suggestions."""
        suggestions = []
        missing_req = score_details["details"].get("missing_required_skills", [])
        
        # Skill-based resources
        for skill in missing_req:
            skill_lower = skill.lower()
            if skill_lower in self.skill_resources:
                suggestions.append(f"**Learn {skill}:** {self.skill_resources[skill_lower]}")
            else:
                suggestions.append(f"**Gain proficiency in {skill}:** Look for introductory tutorials or documentation to understand core concepts.")

        # Experience gap
        exp_gap = score_details["details"].get("experience_gap", "")
        if "less than" in exp_gap.lower():
            suggestions.append("**Bridge the Experience Gap:** Consider contributing to open-source projects or building a comprehensive portfolio project using the required tech stack.")

        # If nothing specific
        if not suggestions:
            suggestions.append("Your profile is very competitive! Focus on tailoring your cover letter to highlight your cultural fit.")

        return suggestions

    def generate_comparison_report(self, cand1_name: str, cand1_score: float, cand2_name: str, cand2_score: float, common_skills: List[str]) -> str:
        """Simple side-by-side comparison summary."""
        diff = abs(cand1_score - cand2_score)
        leader = cand1_name if cand1_score > cand2_score else cand2_name
        
        report = f"""### Comparison Summary
- **{cand1_name}** ({cand1_score}%) vs **{cand2_name}** ({cand2_score}%)
- **Primary Leader:** {leader} (Difference of {diff:.1f}%)
- **Common Strengths:** {', '.join(common_skills) or 'Varied backgrounds'}
- **Recommendation:** Choose {leader} for immediate technical fit, or evaluate {cand1_name if leader == cand2_name else cand2_name} for long-term potential if the gap is small."""
        return report

    def generate_recruiter_summary(self, candidates_list: List[Dict[str, Any]], job_title: str) -> str:
        """Generates a summary of the talent pool for a specific job."""
        count = len(candidates_list)
        if count == 0:
            return f"No candidates have applied for the **{job_title}** role yet."
            
        avg_score = sum(c['score'] for c in candidates_list) / count
        top_cand = candidates_list[0]['name']
        
        summary = f"""### Recruitment Summary: {job_title}
- **Total Candidates Analyzed:** {count}
- **Average Match Score:** {avg_score:.1f}%
- **Top Talent:** {top_cand} is currently the strongest fit.
- **Talent Pool Status:** {"High alignment found" if avg_score > 70 else "Moderately aligned pool" if avg_score > 50 else "Significant skill gaps detected in current candidates"}.
- **Action Item:** Focus interviews on top {min(3, count)} candidates for maximum efficiency."""
        return summary
