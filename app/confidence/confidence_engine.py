import logging

logger = logging.getLogger("ElephantTank.ConfidenceEngine")

class DeterministicConfidenceEngine:
    @staticmethod
    def calculate_confidence(startup_description: str, founder_data: str, base_confidence: int) -> int:
        """
        Adjusts the AI's base confidence score using strict deterministic rules based on data completeness.
        """
        modifier = 0
        
        # Penalize vague startup descriptions
        if not startup_description or len(startup_description.split()) < 10:
            modifier -= 2
            logger.info("Confidence reduced due to highly vague startup description.")
            
        # Penalize missing founder data
        if not founder_data or founder_data.strip() == "" or founder_data.lower() in ["none", "n/a", "unknown"]:
            modifier -= 3
            logger.info("Confidence heavily reduced due to missing founder data.")
            
        # Reward highly detailed descriptions (proxy for clarity)
        if startup_description and len(startup_description.split()) > 50:
            modifier += 1
            logger.info("Confidence increased due to detailed startup description.")
            
        final_confidence = base_confidence + modifier
        
        # Bound between 1 and 10
        return max(1, min(10, final_confidence))
