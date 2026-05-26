import os
import json
import hashlib
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("ElephantTank.Performance.DiskCache")

class DiskCacheManager:
    def __init__(self, cache_dir: str = "d:/STARTUP/.cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_hash(self, payload: str) -> str:
        """Creates a deterministic MD5 hash of the input string."""
        return hashlib.md5(payload.encode('utf-8')).hexdigest()

    def get(self, payload_str: str) -> Optional[Dict[str, Any]]:
        """Checks if a previously computed intelligence profile exists on disk."""
        payload_hash = self._generate_hash(payload_str)
        cache_path = os.path.join(self.cache_dir, f"{payload_hash}.json")
        
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    logger.info(f"Cache HIT for payload hash: {payload_hash}")
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Corrupted cache file detected. Bypassing.")
                return None
                
        logger.info(f"Cache MISS for payload hash: {payload_hash}")
        return None

    def set(self, payload_str: str, response_data: Dict[str, Any]):
        """Persists a successful pipeline output to disk to accelerate future requests."""
        payload_hash = self._generate_hash(payload_str)
        cache_path = os.path.join(self.cache_dir, f"{payload_hash}.json")
        
        with open(cache_path, 'w') as f:
            json.dump(response_data, f)
        logger.info(f"Response successfully cached for hash: {payload_hash}")
