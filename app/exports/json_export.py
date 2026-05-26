import json
import logging
from typing import Dict, Any

logger = logging.getLogger("ElephantTank.Exports.JSONExport")

class JSONExportManager:
    """
    JSON Export Module.
    Serializes and saves compiled strategic venture reports in structured JSON format.
    """
    
    @classmethod
    def export_to_json(cls, report_data: Dict[str, Any], output_path: str) -> str:
        """
        Saves compiled report as structured JSON.
        """
        logger.info(f"Exporting strategic report to JSON: {output_path}")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            logger.info("JSON export completed successfully.")
            return output_path
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            raise
