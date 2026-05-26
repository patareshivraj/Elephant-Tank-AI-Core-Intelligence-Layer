from typing import List, Dict

class RiskAnalyzer:
    def calculate_risk_penalty(self, risk_registry: List[Dict[str, str]]) -> float:
        """
        Analyzes the list of categorical risks and aggregates a deterministic numerical deduction.
        High Severity = -5.0 points
        Medium Severity = -1.5 points
        Low Severity = 0.0 points
        """
        penalty = 0.0
        for risk in risk_registry:
            severity = str(risk.get("severity", "")).upper()
            if severity == "HIGH":
                penalty += 5.0
            elif severity == "MEDIUM":
                penalty += 1.5
            else:
                penalty += 0.0  # Low severity logged for context only
                
        return round(penalty, 2)
