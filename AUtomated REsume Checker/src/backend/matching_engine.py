import numpy as np
from typing import Dict, List, Any, Set, Tuple
from .skills_engine import SkillsEngine
from .semantic_matcher import SemanticMatcher

class MatchingEngine:
    def __init__(self, skills_engine: SkillsEngine, semantic_matcher: SemanticMatcher):
        self.skills_engine = skills_engine
        self.semantic_matcher = semantic_matcher

    def calculate_skills_match(self, candidate_skills: List[str], required_skills: List[str], preferred_skills: List[str]) -> Tuple[float, Dict[str, Any]]:
        """Component 1: Skills Match (40 points)"""
        cand_set = set(candidate_skills)
        req_set = set(required_skills)
        pref_set = set(preferred_skills)

        # Required skills (30 pts)
        req_score = 0
        matched_req = cand_set.intersection(req_set)
        if req_set:
            req_score = (len(matched_req) / len(req_set)) * 30
        else:
            req_score = 30 # No requirements means full points? Or 0? Let's assume 30 for baseline.

        # Preferred skills (10 pts)
        pref_score = 0
        matched_pref = cand_set.intersection(pref_set)
        if pref_set:
            pref_score = (len(matched_pref) / len(pref_set)) * 10
        
        # Bonus for extra relevant skills (up to 5 pts)
        # We calculate this based on skills in the same category but not requested
        all_requested = req_set.union(pref_set)
        bonus_skills = cand_set - all_requested
        bonus_score = min(5, len(bonus_skills) * 0.5)

        total_skills_score = req_score + pref_score + bonus_score
        
        details = {
            "matched_required_skills": list(matched_req),
            "missing_required_skills": list(req_set - cand_set),
            "matched_preferred_skills": list(matched_pref),
            "bonus_skills_count": len(bonus_skills)
        }
        
        return min(45, total_skills_score), details # Max 40 + 5 bonus

    def calculate_experience_match(self, candidate_exp_years: float, required_exp_years: float, 
                                  candidate_exp_text: str, job_responsibilities: str) -> Tuple[float, str]:
        """Component 2: Experience Match (30 points)"""
        # 1. Years alignment (15 pts)
        years_score = 0
        if candidate_exp_years >= required_exp_years - 1:
            years_score = 15
        else:
            # Proportional reduction
            years_score = (candidate_exp_years / max(1, required_exp_years)) * 15
        
        # 2. Relevance (15 pts)
        # Use semantic similarity between experience text and job responsibilities
        relevance_score = self.semantic_matcher.calculate_match_score(candidate_exp_text, job_responsibilities)
        # Scale 0-100 to 0-15
        relevance_points = (relevance_score / 100) * 15
        
        total_exp_score = years_score + relevance_points
        
        gap_desc = "Experience aligned" if candidate_exp_years >= required_exp_years else f"{required_exp_years - candidate_exp_years} years less than required"
        
        return total_exp_score, gap_desc

    def calculate_education_match(self, candidate_edu: Dict[str, Any], required_edu_text: str) -> Tuple[float, str]:
        """Component 3: Education Match (15 points)"""
        # This is rule-based
        score = 0
        details = "Unrelated"
        
        # Degree Level (10 pts)
        cand_degrees = candidate_edu.get("details", {}).get("degrees", [])
        
        # Simple hierarchy
        hierarchy = {"PhD": 3, "Master": 2, "Bachelor": 1}
        
        # Find highest candidate degree
        cand_max = 0
        for d in cand_degrees:
            cand_max = max(cand_max, hierarchy.get(d, 0))
            
        # Detect required degree from text
        req_max = 0
        if any(x in required_edu_text.lower() for x in ["phd", "doctor"]): req_max = 3
        elif any(x in required_edu_text.lower() for x in ["master", "m.s", "m.tech"]): req_max = 2
        elif any(x in required_edu_text.lower() for x in ["bachelor", "b.s", "b.tech"]): req_max = 1
        
        if cand_max >= req_max and req_max > 0:
            score += 10
            details = "Exact or higher match"
        elif cand_max < req_max and req_max > 0:
            score += (cand_max / req_max) * 10
            details = "Lower degree than required"
        else:
            score += 5 # Neutral if not specified
            details = "Education level not specified in JD"

        # Field of Study (5 pts)
        # Check for keywords like "Computer Science", "Engineering" etc.
        relevant_fields = ["computer science", "engineering", "it", "information technology", "mathematics", "physics"]
        found_relevant = any(f in candidate_edu.get("description", "").lower() for f in relevant_fields)
        if found_relevant:
            score += 5
            details += ", Relevant field"
            
        return score, details

    def calculate_overall_score(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Final Score Calculation: 100 points maximum"""
        
        # 1. Skills (40+5 pts)
        skills_score, skills_details = self.calculate_skills_match(
            resume_data.get("skills", []),
            jd_data["skills"]["required"],
            jd_data["skills"]["preferred"]
        )
        
        # 2. Experience (30 pts)
        # We need to extract years from resume first - let's approximate or use a parser if updated
        # For now, let's assume Parser gives us numeric years if we add it, or default to 0
        try:
            # Need a way to extract years from resume. Let's add a helper to parser.
            cand_years = self._estimate_years(resume_data.get("work_experience", {}).get("description", ""))
            req_years = self._parse_years(jd_data["basic_info"]["experience_required"])
        except:
            cand_years, req_years = 0, 0
            
        exp_score, exp_gap = self.calculate_experience_match(
            cand_years, req_years,
            resume_data.get("work_experience", {}).get("description", ""),
            jd_data.get("details", {}).get("responsibilities", "")
        )
        
        # 3. Education (15 pts)
        edu_score, edu_details = self.calculate_education_match(
            resume_data.get("education", {}),
            jd_data.get("education", "")
        )
        
        # 4. Semantic Match (10 pts)
        semantic_score_raw = self.semantic_matcher.calculate_match_score(
            resume_data.get("raw_text", ""),
            jd_data.get("raw_text", "")
        )
        semantic_score = (semantic_score_raw / 100) * 10
        
        # 5. Other Factors (5 pts)
        other_score = 0
        # Projects relevance
        if resume_data.get("projects"): other_score += 2
        # Certifications
        if resume_data.get("certifications"): other_score += 3
        
        total_score = skills_score + exp_score + edu_score + semantic_score + other_score
        
        return {
            "total_score": round(min(100, total_score), 1),
            "breakdown": {
                "skills_match": round(skills_score, 1),
                "experience_match": round(exp_score, 1),
                "education_match": round(edu_score, 1),
                "semantic_match": round(semantic_score, 1),
                "other_factors": round(other_score, 1)
            },
            "details": {
                **skills_details,
                "experience_gap": exp_gap,
                "education_match": edu_details
            }
        }

    def _parse_years(self, years_str: str) -> float:
        import re
        match = re.search(r'(\d+)', years_str)
        return float(match.group(1)) if match else 0.0

    def _estimate_years(self, text: str) -> float:
        # Very simple estimator based on date ranges in text
        import re
        years = re.findall(r'(20\d{2}|19\d{2})', text)
        if len(years) >= 2:
            years = sorted([int(y) for y in years])
            return float(years[-1] - years[0])
        return 0.0

    def rank_candidates(self, jd_data: Dict[str, Any], candidates: List[Any], threshold: float = 40.0) -> List[Dict[str, Any]]:
        ranked = []
        for cand in candidates:
            # Handle both dicts and SQLAlchemy ORM objects
            data = cand.parsed_data if hasattr(cand, 'parsed_data') else cand.get("data")
            cid = cand.id if hasattr(cand, 'id') else cand.get("id")
            
            # Estimate candidate email/name if missing
            name = data.get("personal_info", {}).get("name", "Unknown")
            email = data.get("personal_info", {}).get("email", "")

            score_data = self.calculate_overall_score(data, jd_data)
            if score_data["total_score"] >= threshold:
                ranked.append({
                    "candidate_id": cid,
                    "name": name,
                    "email": email,
                    "score": score_data["total_score"],
                    "breakdown": score_data["breakdown"],
                    "details": score_data["details"]
                })
        
        return sorted(ranked, key=lambda x: x["score"], reverse=True)
