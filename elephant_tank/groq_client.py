import time
import json
import logging
from typing import Dict, Any
from groq import Groq
from elephant_tank.config import (
    GROQ_API_KEY,
    MODEL_PRIMARY,
    MAX_API_RETRIES,
    INITIAL_BACKOFF_SECONDS,
)
from elephant_tank.prompts import MASTER_SYSTEM_PROMPT, EVALUATION_SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ElephantTank.GroqClient")

class GroqEngineClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Groq API client successfully initialized.")
            except Exception as e:
                logger.error(f"Failed to instantiate Groq client: {e}. Falling back to simulation mode.")
                self.client = None
        else:
            logger.warning("GROQ_API_KEY environment variable not detected. Running in Simulation/Mock Mode.")
            self.client = None

    def execute_venture_screening(self, startup_payload_str: str) -> Dict[str, Any]:
        """
        Sends the startup payload string to Groq's llama-3.3-70b-versatile model
        and requests a structured qualitative due diligence report.
        """
        if not self.client:
            return self._generate_simulated_report(startup_payload_str)

        messages = [
            {"role": "system", "content": MASTER_SYSTEM_PROMPT + "\n" + EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the raw startup JSON profile to analyze:\n{startup_payload_str}"}
        ]

        backoff = INITIAL_BACKOFF_SECONDS
        for attempt in range(MAX_API_RETRIES):
            try:
                logger.info(f"Dispatching venture screening request to Groq ({MODEL_PRIMARY}), Attempt {attempt + 1}")
                response = self.client.chat.completions.create(
                    model=MODEL_PRIMARY,
                    messages=messages,
                    temperature=0.1,  # Low temperature for highly deterministic analysis
                    response_format={"type": "json_object"},
                    max_tokens=4096
                )
                
                content = response.choices[0].message.content
                # Parse and validate as JSON
                parsed_json = json.loads(content)
                logger.info("Groq screening output successfully parsed as JSON.")
                return parsed_json
                
            except json.JSONDecodeError as jde:
                logger.error(f"Groq API returned invalid JSON: {jde}. Content: {content}")
                raise ValueError("AI generated malformed JSON output that failed standard decoding.") from jde
                
            except Exception as e:
                logger.warning(f"Groq API connection error on attempt {attempt + 1}: {e}")
                if attempt == MAX_API_RETRIES - 1:
                    logger.error("Max API retries exhausted. Throwing operational exception.")
                    raise e
                
                # Exponential backoff
                time.sleep(backoff)
                backoff *= 2.0

        raise RuntimeError("Venture screening failed due to unexpected API failure.")

    def _generate_simulated_report(self, raw_input_str: str) -> Dict[str, Any]:
        """
        Simulates high-fidelity VC screening qualitative data offline.
        Conforms strictly to the LLMQualitativeOutput validation contract.
        """
        logger.info("Executing offline VC screening simulation model...")
        try:
            startup_data = json.loads(raw_input_str)
            name = startup_data.get("name", "Unknown Startup")
            sector = startup_data.get("sector", "B2B SaaS")
            stage = startup_data.get("current_stage", "Seed")
        except Exception:
            name = "Simulated Startup"
            sector = "B2B SaaS"
            stage = "Seed"

        # Generate realistic scores depending on inputs
        has_tam = "tam_usd" in raw_input_str and "null" not in raw_input_str
        has_rev = "mrr_usd" in raw_input_str and "null" not in raw_input_str
        
        scores = {
            "innovation_defensibility": 7.5 if "patent" in raw_input_str.lower() else 5.5,
            "market_potential": 8.0 if has_tam else 4.0,
            "scalability": 7.0 if "api" in raw_input_str.lower() or "saas" in raw_input_str.lower() else 5.0,
            "revenue_viability": 7.5 if has_rev else 4.0,
            "founder_capability": 8.0 if len(raw_input_str.split("prior_exits")) > 1 else 6.0,
            "competition_risk": 6.5,
            "funding_readiness": 7.0 if has_rev and has_tam else 4.5
        }

        simulated_output = {
            "dimension_scores": scores,
            "dimension_reasonings": {
                "innovation_defensibility": f"The tech stack for {name} shows moderate defensibility. While built on modern frameworks, long-term barriers to entry require proprietary algorithmic moats.",
                "market_potential": f"Targeting {sector} represents a significant TAM. However, specific addressable market segment validation remains highly unverified.",
                "scalability": "Operational model demonstrates standard SaaS operating leverage. Margin profile looks strong at scale, but high customer integration friction is expected.",
                "revenue_viability": "Monetization strategy is straightforward subscription SaaS. Pricing models look initial and lack rigorous unit economics validation.",
                "founder_capability": "Team features domain expertise, but shows key execution gaps in engineering and dedicated scale-up experience.",
                "competition_risk": "Highly saturated competitive landscape with well-funded incumbents operating in similar vertical spaces.",
                "funding_readiness": f"Maturity is aligned with {stage} parameters. Capital efficiency and product-market fit indicators must be resolved before proceeding with full investment due diligence."
            },
            "dimension_evidences": {
                "innovation_defensibility": ["Cites proprietary integration pipeline", "Mentions custom routing layers"],
                "market_potential": ["Cites general market interest", "Targeting B2B software budgets"],
                "scalability": ["SaaS operational structure", "Cloud-native microservice architecture"],
                "revenue_viability": ["Proposed monthly subscription pricing model"],
                "founder_capability": ["Founding team has direct domain operational years"],
                "competition_risk": ["Several active seed-stage competitors listed in this vertical"],
                "funding_readiness": [f"Current stage is stated as {stage}"]
            },
            "dimension_limitations": {
                "innovation_defensibility": [] if "patent" in raw_input_str.lower() else ["No granted utility patents or protected algorithms provided."],
                "market_potential": [] if has_tam else ["Missing empirical TAM/SAM/SOM breakdown. General market sizing is completely unverified."],
                "scalability": ["No verified infrastructure scaling or cost per active user benchmarks."],
                "revenue_viability": [] if has_rev else ["Omitted recurring MRR metrics. Pricing is theoretical and unvalidated."],
                "founder_capability": [],
                "competition_risk": ["Lacks direct head-to-head comparison metrics with prime market incumbents."],
                "funding_readiness": ["Traction parameters are early stage and lack historical month-over-month compound growth trends."]
            },
            "risk_registry": [
                {
                    "risk_type": "Market/Competitive",
                    "severity": "High",
                    "description": f"Intense competitive pressure from established industry leaders who can clone {name}'s features rapidly.",
                    "mitigation": "Establish locked long-term contracts and proprietary data loops to increase customer switching costs."
                },
                {
                    "risk_type": "Business/Financial",
                    "severity": "Medium" if has_rev else "High",
                    "description": "High risk of excessive customer acquisition costs (CAC) draining operational capital before achieving scalable payback loops.",
                    "mitigation": "Develop dynamic organic distribution channels and partner integrations to lower paid media dependency."
                },
                {
                    "risk_type": "Execution",
                    "severity": "Medium",
                    "description": "Lack of full-time dedicated engineering co-founders may slow down product release iterations.",
                    "mitigation": "Immediately source a dedicated technical CTO using equity-based incentives."
                }
            ],
            "strengths": [
                "Strong domain insight into the specified problem statement.",
                "SaaS architecture enables low-cost distribution leverage."
            ],
            "weaknesses": [
                "Unvalidated unit economics and unverified customer acquisition pipelines.",
                "Proprietary defensibility moats are low and easily replicated by competitors."
            ],
            "due_diligence_questions": [
                "What is your current verified CAC and customer payback period?",
                "Can you provide a developer breakdown of your proprietary technology differentiation?",
                "How do you plan to win and protect market share against deep-pocketed direct competitors?"
            ],
            "recommendations": [
                "Execute detailed bottom-up TAM/SAM/SOM sizing before talking to institutional VCs.",
                "Recruit a full-time lead technical engineer or CTO to internalize technology production.",
                "Establish a formal advisory board with active industry executives to accelerate B2B enterprise sales pipelines."
            ]
        }
        return simulated_output
