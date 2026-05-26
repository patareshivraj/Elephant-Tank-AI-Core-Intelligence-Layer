import os
import logging
from groq import Groq
from app.validation.json_repair import RobustJSONParser

logger = logging.getLogger("ElephantTank.Ingestion.Resume")

class ResumeExtractor:
    @staticmethod
    def extract_founder_intelligence(raw_text: str) -> dict:
        """
        Uses Groq to ingest an unstructured resume and output a 
        standardized JSON representing the founder's intelligence.
        """
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
            
        client = Groq(api_key=groq_api_key)
        
        system_prompt = """
        You are a Venture Capital Resume Parser.
        Extract founder intelligence from the provided resume text.
        
        Extract:
        1. founder_name
        2. technical_skills
        3. domain_expertise
        4. startup_history
        5. leadership_indicators
        
        Return ONLY valid JSON:
        {
            "founder_name": "string",
            "technical_skills": ["string"],
            "domain_expertise": ["string"],
            "startup_history": ["string"],
            "leadership_indicators": ["string"],
            "founder_summary": "string"
        }
        """
        
        try:
            safe_text = raw_text[:15000]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"RESUME TEXT:\n{safe_text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            raw_json = response.choices[0].message.content
            return RobustJSONParser.parse_and_repair(raw_json)
        except Exception as e:
            logger.error(f"Failed to extract resume intelligence: {e}")
            raise ValueError("LLM Resume Extraction Failed.")
