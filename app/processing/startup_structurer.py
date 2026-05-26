import os
import logging
from groq import Groq
from app.validation.json_repair import RobustJSONParser

logger = logging.getLogger("ElephantTank.Processing.Structurer")

class StartupStructurer:
    @staticmethod
    def structure_startup_text(raw_text: str) -> dict:
        """
        Uses Groq to ingest unstructured clean text and output the 
        standardized JSON expected by the evaluation engine.
        """
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
            
        client = Groq(api_key=groq_api_key)
        
        system_prompt = """
        You are an Extraction Structurer for Elephant Tank AI.
        Your job is to read unstructured text from Pitch Decks or Startup documents and structure it into JSON.
        
        Extract:
        1. startup_name
        2. startup_description (Summarize the problem, solution, market, traction and business model. At least 50 words)
        3. target_stage (Infer if missing: Pre-seed, Seed, Series A)
        4. founder_data (Names, backgrounds, achievements)
        
        If information is missing, explicitly state 'Not specified in document'. Do not invent details.
        
        Return ONLY valid JSON:
        {
            "startup_name": "string",
            "startup_description": "string",
            "target_stage": "string",
            "founder_data": "string"
        }
        """
        
        try:
            # Chunking protection: limit input to ~25k characters to avoid token limits
            safe_text = raw_text[:25000]
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"EXTRACTED DOCUMENT TEXT:\n{safe_text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.0
            )
            raw_json = response.choices[0].message.content
            return RobustJSONParser.parse_and_repair(raw_json)
        except Exception as e:
            logger.error(f"Failed to structure startup text: {e}")
            raise ValueError("LLM Structuring Extraction Failed.")
