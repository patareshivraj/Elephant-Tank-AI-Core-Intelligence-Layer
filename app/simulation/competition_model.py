import logging
from typing import Dict, Any, List

logger = logging.getLogger("ElephantTank.Simulation.CompetitionModel")

class StartupCompetitionModel:
    """
    Startup Competition Modeling Engine.
    Maps sector overlaps, crowding index scores, and defensibility erosion zones.
    """
    
    @classmethod
    def evaluate_competition(cls, startup_a: Dict[str, Any], startup_b: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs comparative structural overlap algorithms on two startups.
        """
        name_a = startup_a.get("startup_name", "Venture A")
        name_b = startup_b.get("startup_name", "Venture B")
        
        logger.info(f"Modeling competitive defensibility overlap between '{name_a}' and '{name_b}'...")
        
        sectors_a = set(startup_a.get("sectors", []))
        sectors_b = set(startup_b.get("sectors", []))
        
        common_sectors = list(sectors_a.intersection(sectors_b))
        
        # 1. Overlap Index (0 - 100)
        if common_sectors:
            crowding_index = round((len(common_sectors) / max(len(sectors_a), len(sectors_b))) * 100, 2)
        else:
            crowding_index = 0.0
            
        # 2. Defensibility Erosion Warnings
        vulnerable_startup = None
        erosion_detected = False
        if crowding_index >= 50.0:
            erosion_detected = True
            # The startup with the lower score is flagged as vulnerable
            score_a = startup_a.get("overall_score", 50)
            score_b = startup_b.get("overall_score", 50)
            vulnerable_startup = name_a if score_a < score_b else name_b
            
        return {
            "startup_a": name_a,
            "startup_b": name_b,
            "shared_sectors": common_sectors,
            "ecosystem_crowding_index": crowding_index,
            "defensibility_erosion_detected": erosion_detected,
            "vulnerable_entity": vulnerable_startup,
            "competitive_pressure_zone": "HIGH" if crowding_index >= 70.0 else ("MEDIUM" if crowding_index >= 30.0 else "LOW")
        }
