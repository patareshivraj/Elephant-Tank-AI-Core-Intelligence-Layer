import logging

logger = logging.getLogger("ElephantTank.Performance.ModelRouter")

class ModelRouter:
    """
    Dynamically routes LLM workloads to optimize latency and token costs.
    Prevents using expensive 70b models for simple formatting tasks.
    """
    
    # Define production-grade routing maps
    ROUTING_TABLE = {
        "EXTRACTION_CLEANUP": "llama3-8b-8192",         # Fast, lightweight
        "STARTUP_EVALUATION": "llama-3.3-70b-versatile", # High reasoning capability required
        "FOUNDER_PASSPORT": "llama-3.3-70b-versatile",   # High reasoning capability required
        "REPORT_GENERATION": "mixtral-8x7b-32768",       # Excellent for long-context narrative prose
        "MATCH_JUSTIFICATION": "llama3-8b-8192"          # Simple 2-sentence generation
    }

    def get_optimal_model(self, task_type: str) -> str:
        """Returns the most efficient model ID for the specific pipeline stage."""
        model_id = self.ROUTING_TABLE.get(task_type, "llama-3.3-70b-versatile")
        logger.debug(f"Task '{task_type}' routed to model: {model_id}")
        return model_id
