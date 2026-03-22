import re
import os
import pdfplumber
import docx
import spacy
from typing import Dict, List, Any, Optional
import json
from .constants import SKILLS_LIST, SECTION_HEADERS

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback if model not found, though we installed it in setup
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
        return text

    def extract_text_from_docx(self, docx_path: str) -> str:
        text = ""
        try:
            doc = docx.Document(docx_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
        return text

    def clean_text(self, text: str) -> str:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove weird characters but keep basic punctuation
        text = re.sub(r'[^\x00-\x7f]', r' ', text)
        return text.strip()

    def extract_email(self, text: str) -> Optional[str]:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        # Basic phone pattern
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None

    def extract_linkedin(self, text: str) -> Optional[str]:
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9_-]+'
        match = re.search(linkedin_pattern, text)
        return match.group(0) if match else None

    def extract_name(self, text: str) -> Optional[str]:
        # Often the name is at the start
        doc = self.nlp(text[:200]) # Look at first 200 chars
        name = None
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break
        
        if not name:
            # Fallback: first non-empty line
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if lines:
                name = lines[0]
        
        if name:
            # Clean name from any extra lines or obvious email patterns
            name = name.split('\n')[0].strip()
            name = re.split(r'[|/,]', name)[0].strip()
        
        return name

    def extract_skills(self, text: str) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in SKILLS_LIST:
            # Use word boundaries for matching skills like "r" or "c"
            pattern = rf'\b{re.escape(skill.lower())}\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        return list(set(found_skills))

    def get_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        text_lines = text.split('\n')
        current_section = "summary"
        sections[current_section] = ""
        
        for line in text_lines:
            clean_line = line.strip().lower()
            found_header = False
            for section_name, headers in SECTION_HEADERS.items():
                if any(clean_line == h for h in headers) or any(clean_line.startswith(h + ":") for h in headers):
                    current_section = section_name
                    sections[current_section] = ""
                    found_header = True
                    break
            
            if not found_header:
                sections[current_section] += line + "\n"
        
        return sections

    def extract_education_details(self, education_text: str) -> Dict[str, Any]:
        details = {"degrees": [], "gpa": None, "graduation_year": None}
        
        # Degree patterns
        degree_patterns = {
            "Bachelor": r'\b(B\.?S\.?|B\.?A\.?|Bachelor|B\.?E\.?|B\.?Tech)\b',
            "Master": r'\b(M\.?S\.?|M\.?A\.?|Master|M\.?E\.?|M\.?Tech|MBA)\b',
            "PhD": r'\b(Ph\.?D\.?|Doctor of Philosophy)\b'
        }
        
        for degree, pattern in degree_patterns.items():
            if re.search(pattern, education_text, re.IGNORECASE):
                details["degrees"].append(degree)
        
        # GPA matching
        gpa_match = re.search(r'\b[0-4]\.\d{1,2}/[0-4]\.0\b|\bGPA[:\s]+([0-4]\.\d{1,2})\b', education_text, re.IGNORECASE)
        if gpa_match:
            details["gpa"] = gpa_match.group(1) or gpa_match.group(0)

        # Graduation year (usually between 1980 and 2030)
        year_match = re.search(r'\b(19|20)\d{2}\b', education_text)
        if year_match:
            details["graduation_year"] = year_match.group(0)
            
        return details

    def parse(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            raw_text = self.extract_text_from_pdf(file_path)
        elif ext == '.docx':
            raw_text = self.extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        else:
            return {"error": "Unsupported file format"}
            
        return self.parse_text(raw_text)

    def parse_text(self, raw_text: str) -> Dict[str, Any]:
        if not raw_text.strip():
            return {"error": "No text provided"}

        # Extraction logic
        email = self.extract_email(raw_text)
        phone = self.extract_phone(raw_text)
        linkedin = self.extract_linkedin(raw_text)
        name = self.extract_name(raw_text)
        skills = self.extract_skills(raw_text)
        
        sections = self.get_sections(raw_text)
        
        # Further refine education
        education_text = sections.get("education", "")
        education_details = self.extract_education_details(education_text)
        
        # Structure the results
        parsed_data = {
            "personal_info": {
                "name": name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
            },
            "skills": skills,
            "work_experience": {
                "description": sections.get("experience", "").strip(),
                "raw": sections.get("experience", "").strip()
            },
            "education": {
                "description": education_text.strip(),
                "details": education_details
            },
            "projects": sections.get("projects", "").strip(),
            "certifications": sections.get("certifications", "").strip(),
            "raw_text": raw_text 
        }
        
        return parsed_data

if __name__ == "__main__":
    # Test stub
    parser = ResumeParser()
    # print(json.dumps(parser.parse("path/to/resume.pdf"), indent=2))
