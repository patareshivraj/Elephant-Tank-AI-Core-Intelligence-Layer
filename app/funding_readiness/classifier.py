from typing import Dict, Any

class ReadinessClassifier:
    def determine_funding_readiness(self, overall_score: float, confidence_score: float, stated_stage: str) -> Dict[str, str]:
        """
        Bypasses LLM hallucinations to deterministically label funding maturity based on calculated scores.
        """
        if confidence_score < 40.0:
            return {
                "classification": "Idea Stage / Insufficient Data",
                "justification": "Confidence score critically low. Missing foundational metrics required for venture due diligence."
            }
            
        if overall_score >= 85.0:
            return {
                "classification": "Growth Ready" if stated_stage == "Series A" else "Series A Ready",
                "justification": "Exceptional scoring matrix across market, operations, and revenue viabilities."
            }
        elif overall_score >= 70.0:
            return {
                "classification": "Seed Ready",
                "justification": "Strong fundamental defensibility and team, prepared for early traction scaling."
            }
        elif overall_score >= 50.0:
            return {
                "classification": "Pre-Seed Ready",
                "justification": "Operational gaps identified. Requires early validation capital to build out MVP/GTM."
            }
        else:
            return {
                "classification": "Idea Stage",
                "justification": "Significant structural weaknesses or severe competitive risks block institutional readiness."
            }
