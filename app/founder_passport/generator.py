import logging
from typing import Dict, Any
from app.founder_scoring.engine import FounderScoringEngine
from app.founder_risk_engine.analyzer import FounderRiskAnalyzer
from app.schemas.founder import FounderPassport

logger = logging.getLogger("ElephantTank.FounderPassport")

class FounderPassportGenerator:
    """
    Orchestrates the Founder Intelligence workflow and strictly validates 
    the final output against the FounderPassport schema.
    """
    def __init__(self):
        self.scoring_engine = FounderScoringEngine()
        self.risk_analyzer = FounderRiskAnalyzer()
        
    def generate_passport(self, raw_founder_data: Dict[str, Any], startup_context: Dict[str, Any]) -> FounderPassport:
        logger.info("Compiling Founder Passport...")
        
        # 1. Calculate Scores
        scores = self.scoring_engine.calculate_scores(raw_founder_data)
        
        # 2. Generate Risk Flags
        risks = self.risk_analyzer.analyze_risks(startup_context, scores)
        
        # 3. Formulate Recommendations based on risks
        recommendations = []
        if any("technical" in r.lower() for r in risks):
            recommendations.append("Immediate: Hire a Technical Co-founder or CTO.")
        if any("Single-founder" in r for r in risks):
            recommendations.append("Build a robust advisory board to offset solo-founder execution bandwidth limitations.")
            
        # 4. Confidence Penalty (Simulated)
        # If 'years_technical_experience' is missing, lower confidence
        confidence = 100.0
        if "years_technical_experience" not in raw_founder_data:
            confidence -= 15.0
            
        # Build Final Validated Contract
        return FounderPassport(
            founder_name=raw_founder_data.get("founder_name", "Unknown Founder"),
            leadership_score=scores["leadership_score"],
            technical_capability_score=scores["technical_capability_score"],
            execution_readiness_score=scores["execution_readiness_score"],
            startup_experience_score=scores["startup_experience_score"],
            domain_expertise_score=scores["domain_expertise_score"],
            confidence_score=confidence,
            strengths=raw_founder_data.get("known_strengths", []),
            weaknesses=raw_founder_data.get("known_weaknesses", []),
            risk_flags=risks,
            recommendations=recommendations
        )
