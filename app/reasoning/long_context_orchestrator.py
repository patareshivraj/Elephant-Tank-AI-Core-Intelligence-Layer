import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Reasoning.LongContextOrchestrator")

class LongContextOrchestrator:
    """
    Long-Context Orchestrator.
    Merges multi-source startup documents (pitch decks, resumes, market notes),
    optimizes token usage, maintains semantic continuity, and prevents reasoning fragmentation.
    """
    
    @classmethod
    def clean_and_normalize_content(cls, raw_text: str) -> str:
        """
        Removes excessive whitespaces, page headers/footers, and duplicate line dividers
        to maximize token efficiency.
        """
        if not raw_text:
            return ""
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        # Filter out obvious header/footer artifacts
        filtered_lines = []
        for line in lines:
            lower = line.lower()
            if any(p in lower for p in ["page", "confidential", "all rights reserved", "slide "]):
                continue
            filtered_lines.append(line)
        return " ".join(filtered_lines)

    @classmethod
    def orchestrate_context(cls, document_sources: List[Dict[str, Any]], token_limit: int = 8000) -> Dict[str, Any]:
        """
        Merges startup intelligence across multiple documents.
        Maintains chronological priority and source reliability weights.
        """
        logger.info(f"Orchestrating long context across {len(document_sources)} sources...")
        start_time = time.time()
        
        merged_sections = {
            "startup_pitch": "",
            "founder_profiles": [],
            "market_notes": [],
            "raw_text_corpus": ""
        }
        
        total_chars = 0
        for doc in document_sources:
            src_type = doc.get("source_type", "generic").lower()
            content = cls.clean_and_normalize_content(doc.get("content", ""))
            
            # Simple token truncation check based on character counts (approx 4 chars = 1 token)
            if total_chars + len(content) > (token_limit * 4):
                logger.warning(f"Truncating content from source '{src_type}' to fit token constraints.")
                content = content[:((token_limit * 4) - total_chars)]
            
            total_chars += len(content)
            
            if "deck" in src_type or "pitch" in src_type or "description" in src_type:
                merged_sections["startup_pitch"] += f"\n[Pitch Source]: {content}"
            elif "resume" in src_type or "bio" in src_type or "founder" in src_type:
                merged_sections["founder_profiles"].append(content)
            elif "market" in src_type or "note" in src_type or "competitor" in src_type:
                merged_sections["market_notes"].append(content)
            else:
                merged_sections["raw_text_corpus"] += f"\n[Other Context]: {content}"
                
        # Consolidate raw text corpus
        consolidated_corpus = (
            f"STARTUP OVERVIEW AND PITCH:{merged_sections['startup_pitch']}\n\n"
            f"FOUNDER BIOGRAPHIES AND EXPERIENCES:\n" + "\n".join([f"- {f}" for f in merged_sections["founder_profiles"]]) + "\n\n"
            f"MARKET INTELLIGENCE AND RESEARCH NOTES:\n" + "\n".join([f"- m" for m in merged_sections["market_notes"]]) + "\n\n"
            f"OTHER REFERENCE CORPUS: {merged_sections['raw_text_corpus']}"
        )
        
        elapsed_time = time.time() - start_time
        execution_log = {
            "stage": "LONG_CONTEXT_REASONING",
            "status": "SUCCESS",
            "message": f"Orchestrated {len(document_sources)} sources. Merged character length: {len(consolidated_corpus)}.",
            "timestamp": int(time.time())
        }
        
        logger.info(f"Context orchestration complete in {elapsed_time:.3f}s.")
        return {
            "consolidated_context": consolidated_corpus,
            "orchestrated_sections": merged_sections,
            "total_character_count": len(consolidated_corpus),
            "execution_log": execution_log
        }
