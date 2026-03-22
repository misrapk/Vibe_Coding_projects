import re
import spacy
from typing import Dict, List, Any

class BiasDetector:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # 1. Bias Dictionary & Suggestions
        self.bias_data = {
            "Gender Bias": {
                "masculine": {
                    "terms": ['competitive', 'dominant', 'aggressive', 'rockstar', 'ninja', 'guru', 'hustler', 'challenging', 'driven', 'fearless'],
                    "explanation": "Masculine-coded language may discourage female applicants.",
                    "suggestion": "Use more balanced or neutral alternatives like 'exceptional', 'highly skilled', or 'results-oriented'."
                },
                "feminine": {
                    "terms": ['support', 'collaborate', 'nurture', 'helpful', 'cooperative', 'dependable', 'interpersonal'],
                    "explanation": "Highly feminine-coded language may subtly skew candidate perceptions.",
                    "suggestion": "Balance with neutral technical expectations."
                },
                "pronouns": {
                    "terms": [r'\bhe\b', r'\bshe\b', r'\bhis\b', r'\bher\b'],
                    "explanation": "Gendered pronouns assume a specific gender for the role.",
                    "suggestion": "Use gender-neutral pronouns like 'they' or 'them', or refer to 'the candidate'."
                }
            },
            "Age Bias": {
                "young": {
                    "terms": ['recent graduate', 'digital native', 'energetic', 'young', 'fresh', 'early career'],
                    "explanation": "May discourage or exclude experienced professionals.",
                    "suggestion": "Focus on the required skill level rather than years since graduation (e.g., 'all experience levels welcome')."
                },
                "older_exclusion": {
                    "terms": ['overqualified', 'senior leader', 'well-seasoned'], # senior is often okay, but 'overqualified' is a bias indicator
                    "explanation": "Can be code for excluding candidates based on age or perceived higher cost.",
                    "suggestion": "Define specific role responsibilities rather than using exclusionary labels."
                }
            },
            "Educational Bias": {
                "prestige": {
                    "terms": ['top university', 'ivy league', 'top-tier school'],
                    "explanation": "Excludes qualified candidates from non-traditional or diverse educational backgrounds.",
                    "suggestion": "Focus on the specific knowledge or skills required rather than university prestige."
                },
                "over_credentialing": {
                    "terms": ['phd required', 'doctorate essential'], # Only biased if job doesn't strictly need it
                    "explanation": "May create unnecessary barriers for highly qualified candidates with masters or bachelors degrees.",
                    "suggestion": "Consider 'PhD preferred' or 'equivalent practical experience'."
                }
            },
            "Cultural/Racial Bias": {
                "language": {
                    "terms": ['native english speaker', 'natural english'],
                    "explanation": "Discrimates against non-native but fully proficient speakers.",
                    "suggestion": "Use 'excellent English communication skills' or 'proficient in English'."
                },
                "fit": {
                    "terms": ['cultural fit'],
                    "explanation": "Often used as a proxy for unconscious bias or discrimination against those who are 'different'.",
                    "suggestion": "Use 'cultural add' or define specific values alignment (e.g., 'aligns with our value of transparency')."
                }
            },
            "Disability Bias": {
                "physical": {
                    "terms": ['must be able to lift 50 lbs', 'perfect vision'],
                    "explanation": "May exclude candidates with disabilities if the requirement isn't essential to the job functions.",
                    "suggestion": "Only include physical requirements that are strictly necessary and cannot be accommodated."
                }
            },
            "Other Biases": {
                "lifestyle": {
                    "terms": ['work hard play hard', 'available 24/7', 'unlimited bandwidth'],
                    "explanation": "May exclude parents, caregivers, or those needing a healthy work-life balance.",
                    "suggestion": "Highlight work-life balance or focus on project-based delivery."
                }
            }
        }

        # Neutral Alternatives Database
        self.replacements = {
            "rockstar": "exceptional",
            "ninja": "highly skilled",
            "guru": "expert",
            "recent graduate": "early career",
            "digital native": "tech-savvy professional",
            "native english speaker": "excellent English communication skills",
            "work hard play hard": "balanced and dynamic work environment",
            "cultural fit": "values alignment",
            "he": "the candidate / they",
            "she": "the candidate / they"
        }

    def detect_bias(self, text: str) -> List[Dict[str, Any]]:
        found_biases = []
        text_lower = text.lower()
        
        for category, sub_cats in self.bias_data.items():
            for sub_name, data in sub_cats.items():
                for term in data["terms"]:
                    # Handle regex for pronouns
                    is_regex = term.startswith(r'\b')
                    if is_regex:
                        matches = re.finditer(term, text_lower)
                    else:
                        matches = re.finditer(rf'\b{re.escape(term)}\b', text_lower)
                    
                    for match in matches:
                        phrase = match.group(0)
                        # Find suggestion if exists
                        suggestion = self.replacements.get(phrase.lower(), data["suggestion"])
                        
                        found_biases.append({
                            "phrase": phrase,
                            "type": category,
                            "sub_type": sub_name,
                            "explanation": data["explanation"],
                            "suggestion": suggestion,
                            "start": match.start(),
                            "end": match.end()
                        })
        
        # De-duplicate matches at the same position (longer matches preferred)
        found_biases = sorted(found_biases, key=lambda x: (x["start"], -(x["end"] - x["start"])))
        unique_biases = []
        last_end = -1
        for b in found_biases:
            if b["start"] >= last_end:
                unique_biases.append(b)
                last_end = b["end"]
                
        return unique_biases

    def calculate_bias_score(self, biased_phrases: List[Dict[str, Any]], text_length: int) -> float:
        """Calculates bias score 0-100. Lower is better."""
        if text_length == 0: return 0
        
        # Count severity/frequency
        count = len(biased_phrases)
        # Normalize by length (phrases per 100 words approx)
        density = (count / (text_length / 6)) * 100 # Assuming avg word length 6
        
        # Base score on count and diversity of bias types
        unique_types = len(set([b["type"] for b in biased_phrases]))
        
        score = (count * 5) + (unique_types * 10)
        return min(100, score)

    def analyze(self, text: str) -> Dict[str, Any]:
        biased_phrases = self.detect_bias(text)
        score = self.calculate_bias_score(biased_phrases, len(text))
        
        status = "Minimal Bias"
        if score > 50: status = "High Bias"
        elif score > 20: status = "Moderate Bias"
        
        # General recommendations
        recommendations = [
            "Use gender-neutral language throughout the posting.",
            "Focus on essential skills and outcomes rather than pedigree.",
            "Avoid idiomatic expressions (like 'rockstar') that might alienate certain demographics."
        ]
        
        return {
            "bias_score": round(score, 1),
            "status": status,
            "biased_phrases": biased_phrases,
            "recommendations": recommendations,
            "summary": f"This job description has a {status.lower()} ({score:.1f}/100). {len(biased_phrases)} potentially biased phrases were detected."
        }

    def anonymize_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Redacts identifying information from a resume."""
        anonymized = resume_data.copy()
        
        # Redact Personal Info
        anonymized["personal_info"] = {
            "name": "[REDACTED NAME]",
            "email": "[REDACTED EMAIL]",
            "phone": "[REDACTED PHONE]",
            "linkedin": "[REDACTED LINKEDIN]"
        }
        
        # Generalize Education (remove years)
        if "education" in anonymized and "details" in anonymized["education"]:
            anonymized["education"]["details"]["graduation_year"] = "[REDACTED YEAR]"
            # Also clean the description of years
            desc = anonymized["education"].get("description", "")
            anonymized["education"]["description"] = re.sub(r'\b(19|20)\d{2}\b', '[YEAR]', desc)

        # Clean work experience and raw text of obvious identifiers
        # This is a bit harder, but we can try to find names using spaCy and redact
        def redact_text(text: str) -> str:
            doc = self.nlp(text)
            redacted = text
            for ent in reversed(doc.ents):
                if ent.label_ in ["PERSON", "EMAIL", "PHONE", "GPE"]: # GPE for addresses
                    redacted = redacted[:ent.start_char] + f"[{ent.label_}]" + redacted[ent.end_char:]
            return redacted

        if "work_experience" in anonymized:
            anonymized["work_experience"]["description"] = redact_text(anonymized["work_experience"].get("description", ""))
        
        if "raw_text" in anonymized:
            anonymized["raw_text"] = redact_text(anonymized["raw_text"])

        return anonymized

if __name__ == "__main__":
    detector = BiasDetector()
    sample = "Looking for a rockstar developer. He should be a recent graduate from a top university. Native English speaker required."
    print(detector.analyze(sample))
