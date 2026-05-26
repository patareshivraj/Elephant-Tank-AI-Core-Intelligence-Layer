from typing import Dict, Any
from app.schemas.performance import OptimizationReport
import psutil
import os

class PerformanceRunner:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def analyze_execution(self, timings: Dict[str, float], cache_stats: Dict[str, Any]) -> OptimizationReport:
        """
        Aggregates profiling data, identifies bottlenecks (>2000ms latency), 
        and packages it into the Pydantic OptimizationReport.
        """
        bottlenecks = []
        recommendations = []
        
        # Identify slow modules
        for module, latency in timings.items():
            if latency > 2000: # 2 seconds threshold
                bottlenecks.append(f"{module} exceeded target latency ({latency}ms)")
                if "LLM" in module:
                    recommendations.append(f"Consider routing {module} to a lighter model (e.g., Llama 3 8B).")
                
        # Measure RAM usage
        memory_mb = self.process.memory_info().rss / (1024 * 1024)
        
        return OptimizationReport(
            pipeline_latency=timings,
            groq_performance={"status": "monitored"},
            embedding_performance={"status": "monitored"},
            cache_statistics=cache_stats,
            memory_usage={"peak_mb": round(memory_mb, 2)},
            bottlenecks=bottlenecks,
            optimization_recommendations=recommendations,
            system_health={"status": "optimal"}
        )
