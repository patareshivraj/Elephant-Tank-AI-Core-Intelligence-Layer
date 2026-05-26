import logging
from pydantic import ValidationError
from typing import Dict, Any, Tuple
from app.schemas.orchestration import UnifiedIntelligenceOutput

logger = logging.getLogger("ElephantTank.SchemaChecker")

class SchemaChecker:
    def validate_unified_output(self, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Attempts to force the raw dictionary payload into the UnifiedIntelligenceOutput contract.
        If the LLM or orchestration dropped keys or changed types, it fails here.
        """
        errors = []
        try:
            UnifiedIntelligenceOutput(**payload)
            return True, errors
        except ValidationError as e:
            logger.error("Schema validation failed.")
            for error in e.errors():
                errors.append(f"Field {error['loc']} - {error['msg']}")
            return False, errors
