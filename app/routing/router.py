import os

class PromptRouter:
    def __init__(self, prompts_dir: str = "d:/STARTUP/app/prompts"):
        self.prompts_dir = prompts_dir
        self.master_system_prompt = self._load_prompt("master_system_prompt.txt")

    def _load_prompt(self, filename: str) -> str:
        filepath = os.path.join(self.prompts_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Prompt template {filename} not found at {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def route_task(self, task_name: str, **kwargs) -> list:
        """
        Returns a list of dicts formatted for the Groq messages array.
        Prepends the master system prompt to enforce the VC persona.
        """
        task_map = {
            "startup_evaluation": "startup_evaluation.txt",
            "founder_analysis": "founder_evaluation.txt",
            "risk_analysis": "risk_analysis.txt",
            "executive_summary": "executive_summary.txt",
            "recommendation_mode": "recommendation_engine.txt"
        }
        
        if task_name not in task_map:
            raise ValueError(f"Unknown reasoning task: {task_name}")
            
        task_prompt_raw = self._load_prompt(task_map[task_name])
        
        # Inject kwargs into the prompt (e.g., {startup_json})
        task_prompt_hydrated = task_prompt_raw.format(**kwargs)
        
        messages = [
            {"role": "system", "content": self.master_system_prompt},
            {"role": "user", "content": task_prompt_hydrated}
        ]
        
        return messages
