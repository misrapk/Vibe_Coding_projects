import re
from typing import Dict, List, Any, Set
from .skills_data import SKILLS_DB

class SkillsEngine:
    def __init__(self):
        self.skills_db = SKILLS_DB
        self._reverse_alias_map = self._build_alias_map()

    def _build_alias_map(self) -> Dict[str, str]:
        """Maps aliases to the canonical skill name."""
        alias_map = {}
        for skill_name, data in self.skills_db.items():
            # Canonical name itself is an alias
            alias_map[skill_name.lower()] = skill_name
            for alias in data.get("aliases", []):
                alias_map[alias.lower()] = skill_name
        return alias_map

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extracts skills and organizes them by category."""
        text_lower = text.lower()
        found_canonical_names = set()

        # Simple pattern matching for aliases
        for alias, canonical_name in self._reverse_alias_map.items():
            # Use word boundaries to avoid partial matches (e.g., 'c' in 'cat')
            pattern = rf'\b{re.escape(alias)}\b'
            if re.search(pattern, text_lower):
                found_canonical_names.add(canonical_name)

        # Organize by category
        categorized = {}
        for skill in found_canonical_names:
            category = self.skills_db[skill]["category"]
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill)
        
        return categorized

    def match_skills(self, candidate_skills: Set[str], required_skills: Set[str], preferred_skills: Set[str] = None) -> Dict[str, Any]:
        """Matches candidate skills against JD requirements."""
        if preferred_skills is None:
            preferred_skills = set()

        # Canonicalize all sets
        candidate_set = {s for s in candidate_skills}
        required_set = {s for s in required_skills}
        preferred_set = {s for s in preferred_skills}

        # 1. Exact Matches (Required)
        matched_required = candidate_set.intersection(required_set)
        
        # 2. Missing Required
        missing_required = required_set - candidate_set

        # 3. Preferred Matches
        matched_preferred = candidate_set.intersection(preferred_set)
        
        # 4. Bonus Skills (skills the candidate has that aren't specifically requested)
        bonus_skills = candidate_set - (required_set | preferred_set)

        # 5. Partial Matches (Related Skills)
        # For missing required skills, check if candidate has a related skill
        partial_matches = {}
        for missing in missing_required:
            related = set(self.skills_db.get(missing, {}).get("related", []))
            related_found = candidate_set.intersection(related)
            if related_found:
                partial_matches[missing] = list(related_found)

        # Scoring Logic
        total_req = len(required_set)
        if total_req == 0:
            score = 100 # Or based on preferred/bonus
        else:
            # Base score from required matches
            exact_match_score = (len(matched_required) / total_req) * 80
            
            # Partial match bonus (worth 50% of an exact match)
            partial_bonus = (len(partial_matches) / total_req) * 40
            
            # Cap the score from required/partial at 80
            req_score = min(80, exact_match_score + partial_bonus)
            
            # Preferred skills bonus (up to 15%)
            pref_bonus = 0
            if preferred_set:
                pref_bonus = (len(matched_preferred) / len(preferred_set)) * 15
            
            # Bonus skills (vibe check - up to 5%)
            vibe_bonus = min(5, len(bonus_skills) * 0.5)
            
            score = req_score + pref_bonus + vibe_bonus

        return {
            "score": round(min(100, score), 1),
            "matched_required": list(matched_required),
            "missing_required": list(missing_required),
            "partial_matches": partial_matches,
            "matched_preferred": list(matched_preferred),
            "bonus_skills": list(bonus_skills)
        }

if __name__ == "__main__":
    # Test
    engine = SkillsEngine()
    resume_text = "I am a Python developer with experience in Django, AWS, and Git. I also know SQL."
    jd_text = "Looking for a Python developer with knowledge of FastAPI, AWS, and PostgreSQL."
    
    candidate_cats = engine.extract_skills(resume_text)
    candidate_skills = set([s for cat in candidate_cats.values() for s in cat])
    
    # Mocking JD extraction
    req_skills = {"Python", "FastAPI", "AWS", "PostgreSQL"}
    
    results = engine.match_skills(candidate_skills, req_skills)
    import json
    print(json.dumps(results, indent=2))
