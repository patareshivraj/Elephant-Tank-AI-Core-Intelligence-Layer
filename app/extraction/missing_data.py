from typing import Any
from app.schemas.intelligence import ExtractedField

class MissingDataDetector:
    def validate_and_tag(self, extracted_value: Any, source_reference: str = None) -> ExtractedField:
        """
        Inspects an extracted value deterministically. If it's empty, None, or vague filler, 
        it is explicitly tagged as UNVERIFIED to prevent LLM hallucinations during scoring.
        """
        vague_fillers = {"tbd", "to be determined", "huge", "massive", "unknown", "n/a", ""}
        
        is_missing = False
        
        if extracted_value is None:
            is_missing = True
        elif isinstance(extracted_value, str) and extracted_value.strip().lower() in vague_fillers:
            is_missing = True
        elif isinstance(extracted_value, (int, float)) and extracted_value == 0:
            # Note: 0 TAM is a flag, 0 Prior Exits is valid. Needs contextual overrides later.
            is_missing = False 

        if is_missing:
            return ExtractedField(
                value="UNVERIFIED",
                confidence=0.0,
                verified=False,
                source_chunk=None
            )
        else:
            return ExtractedField(
                value=extracted_value,
                confidence=0.90, # Baseline deterministic confidence assumption
                verified=True,
                source_chunk=source_reference
            )
