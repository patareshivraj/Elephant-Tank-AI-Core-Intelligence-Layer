from typing import List, Dict
import re

class DocumentSegmenter:
    def segment_by_slide(self, parsed_pages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Directly translates PPT or PDF pages into distinct, LLM-friendly semantic chunks.
        """
        chunks = []
        for page in parsed_pages:
            content = page.get("content", "")
            # Filter out decorative/empty transition slides
            if len(content) > 15:  
                chunks.append({
                    "chunk_id": f"Slide_{page.get('page_number', 'Unknown')}",
                    "text": content
                })
        return chunks
        
    def semantic_chunk_text(self, text: str) -> List[Dict[str, str]]:
        """
        Splits raw continuous text into semantic chunks based on startup-specific headers.
        """
        # Split on capitalization/header markers like "PROBLEM:", "MARKET SIZING"
        sections = re.split(r'\n(?=[A-Z][A-Za-z\s]{2,30}:)', text)
        chunks = []
        for i, section in enumerate(sections):
            if section.strip():
                chunks.append({
                    "chunk_id": f"Semantic_Text_Segment_{i+1}",
                    "text": section.strip()
                })
        return chunks
