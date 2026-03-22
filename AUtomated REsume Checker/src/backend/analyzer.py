from typing import Dict, List, Any

class CareerAnalyzer:
    def __init__(self, skills_engine):
        self.skills_engine = skills_engine

    def generate_suggestions(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], match_results: Dict[str, Any]) -> List[str]:
        suggestions = []
        
        # 1. Skill Gaps
        missing_req = match_results.get("missing_required", [])
        if missing_req:
            suggestions.append(f"Missing key required skills: {', '.join(missing_req)}. Consider gaining basic proficiency in these.")
            
        # 2. Experience Gap
        try:
            jd_exp = float(jd_data['basic_info']['experience_required'].split('+')[0])
            # This is a bit tricky, we'd need to parse years from resume properly
            # For now, we'll just check if it's a senior role and candidate matches
            if jd_data['basic_info']['seniority'] == "Senior" and match_results['score'] < 60:
                suggestions.append("The role requires more seniority. Highlight leadership roles and complex projects you've managed.")
        except:
            pass
            
        # 3. Certification Suggestions
        # If missing a skill that has a known certification, suggest it
        if "AWS" in missing_req:
            suggestions.append("Consider earning an AWS Certified Cloud Practitioner or Solutions Architect certification.")
        if "Kubernetes" in missing_req:
            suggestions.append("Obtaining a CKA (Certified Kubernetes Administrator) could significantly boost your profile.")

        # 4. Content Optimization
        if not resume_data.get('projects'):
            suggestions.append("Your resume lacks a dedicated 'Projects' section. Adding personal or open-source projects can demonstrate hands-on experience.")
            
        if len(resume_data.get('skills', [])) < 5:
            suggestions.append("Detail your technical skills more explicitly. List specific libraries and tools you've worked with.")

        if not suggestions:
            suggestions.append("Your resume is well-aligned with this role! Consider tailor-fitting your summary to matches the company culture.")

        return suggestions

if __name__ == "__main__":
    # Test stub
    pass
