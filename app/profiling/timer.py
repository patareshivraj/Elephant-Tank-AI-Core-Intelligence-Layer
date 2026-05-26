import time
import logging
from contextlib import contextmanager
from typing import Dict

logger = logging.getLogger("ElephantTank.Performance.Profiler")

class ExecutionProfiler:
    def __init__(self):
        self.timings: Dict[str, float] = {}

    @contextmanager
    def measure(self, module_name: str):
        """
        Context manager used around pipeline stages to record exact execution latency.
        Usage:
            with profiler.measure("LLM_EVALUATION"):
                engine.evaluate()
        """
        start_time = time.perf_counter()
        try:
            yield
        finally:
            elapsed_time_ms = (time.perf_counter() - start_time) * 1000
            self.timings[module_name] = round(elapsed_time_ms, 2)
            logger.debug(f"Module '{module_name}' executed in {self.timings[module_name]}ms")

    def get_timings(self) -> Dict[str, float]:
        return self.timings
