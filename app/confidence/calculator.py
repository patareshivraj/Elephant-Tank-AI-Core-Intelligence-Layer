from typing import Dict, List

class ConfidenceCalculator:
    def calculate_confidence(self, missing_fields: List[str], base_score: float = 100.0) -> float:
        """
        Generates the 0-100 Confidence Metric based on missing/UNVERIFIED payload fields.
        Strictly prevents "False Certainty" by penalizing incomplete financial or market data.
        """
        confidence = base_score
        
        # Determine penalty severity by field mapping
        for field in missing_fields:
            clean_field = field.lower()
            if "mrr" in clean_field or "revenue" in clean_field or "margin" in clean_field:
                confidence -= 20.0  # Massive financial blindspot penalty
            elif "tam" in clean_field or "market" in clean_field:
                confidence -= 15.0  # Missing market sizing
            elif "competitor" in clean_field:
                confidence -= 10.0
            elif "founder" in clean_field:
                confidence -= 15.0
            else:
                confidence -= 5.0   # Baseline missing data penalty
                
        return max(0.0, round(confidence, 2))
