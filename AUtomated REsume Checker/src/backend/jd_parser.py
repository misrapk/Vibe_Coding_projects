import re
import spacy
from typing import Dict, List, Any, Optional
from .constants import SKILLS_LIST, SECTION_HEADERS, SENIORITY_KEYWORDS, JOB_TYPES

class JDParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7f]', r' ', text)
        return text.strip()

    def extract_skills(self, text: str) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in SKILLS_LIST:
            pattern = rf'\b{re.escape(skill.lower())}\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        return list(set(found_skills))

    def detect_seniority(self, text: str, years_required: Optional[float] = None) -> str:
        text_lower = text.lower()
        
        # Priority 1: Keyword matches (e.g., "Senior Python Dev" should be Senior regardless of years mentioned in text)
        if any(kw in text_lower for kw in SENIORITY_KEYWORDS['senior']):
            return "Senior"
        if any(kw in text_lower for kw in SENIORITY_KEYWORDS['junior']):
            return "Junior"
        
        # Priority 2: Rule based on years if available
        if years_required is not None:
            if years_required < 3:
                return "Junior"
            elif years_required < 7:
                return "Mid"
            else:
                return "Senior"
        
        return "Not Specified"

    def extract_years_experience(self, text: str) -> Optional[float]:
        # Matches patterns like "3+ years", "5-7 years", "at least 4 years"
        patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) > 1 and match.group(2):
                    # Average of range
                    return (float(match.group(1)) + float(match.group(2))) / 2
                return float(match.group(1))
        return None

    def extract_salary(self, text: str) -> Optional[str]:
        # Matches patterns like $80k, 80,000, 100-120k
        salary_pattern = r'(\$?\d{2,3}[kK]|\$?\d{2,3},\d{3})'
        matches = re.findall(salary_pattern, text)
        if matches:
            if len(matches) >= 2:
                return f"{matches[0]} - {matches[1]}"
            return matches[0]
        return None

    def extract_job_type(self, text: str) -> List[str]:
        found_types = []
        text_lower = text.lower()
        for jt in JOB_TYPES:
            if jt in text_lower:
                found_types.append(jt)
        return found_types

    def get_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        lines = text.split('\n')
        current_section = "overview"
        sections[current_section] = ""
        
        for line in lines:
            clean_line = line.strip().lower()
            found_header = False
            for section_name, headers in SECTION_HEADERS.items():
                if any(clean_line == h for h in headers) or any(clean_line.startswith(h + ":") for h in headers):
                    current_section = section_name
                    if current_section not in sections:
                        sections[current_section] = ""
                    found_header = True
                    break
            
            if not found_header:
                sections[current_section] += line + "\n"
        
        return sections

    def parse(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {"error": "Empty job description"}

        # Basic text cleaning for regex matching
        clean_jd_text = self.clean_text(text)
        
        # Segment into sections
        sections = self.get_sections(text)
        
        # Extract details
        years_exp = self.extract_years_experience(clean_jd_text)
        seniority = self.detect_seniority(clean_jd_text, years_exp)
        job_types = self.extract_job_type(clean_jd_text)
        salary = self.extract_salary(clean_jd_text)
        
        # Required vs Preferred Skills
        all_skills = self.extract_skills(clean_jd_text)
        req_text = sections.get("requirements", "") + sections.get("essential", "")
        pref_text = sections.get("preferred", "") + sections.get("bonus", "")
        
        required_skills = self.extract_skills(req_text) if req_text else all_skills
        preferred_skills = self.extract_skills(pref_text) if pref_text else []
        
        # Culture keywords
        culture_keywords = ['collaborative', 'fast-paced', 'innovative', 'startup', 'inclusive', 'mentorship']
        found_culture = [kw for kw in culture_keywords if kw in clean_jd_text.lower()]

        # Try to extract Job Title from first line
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        job_title = lines[0] if lines else "Not Found"

        return {
            "basic_info": {
                "job_title": job_title,
                "seniority": seniority,
                "experience_required": f"{years_exp}+ years" if years_exp else "Not specified",
                "job_type": job_types,
                "salary_range": salary
            },
            "skills": {
                "required": required_skills,
                "preferred": preferred_skills,
                "all_mentioned": all_skills
            },
            "details": {
                "responsibilities": sections.get("responsibilities", "").strip(),
                "benefits": sections.get("benefits", "").strip(),
                "culture": found_culture
            },
            "education": sections.get("education", "").strip() or "Not specifically mentioned",
            "raw_text": text
        }
