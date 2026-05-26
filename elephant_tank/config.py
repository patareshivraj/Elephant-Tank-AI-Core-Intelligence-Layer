import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# LLM & EMBEDDING ROUTING CONFIGURATION
# --------------------------------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Active Models on Groq API
MODEL_PRIMARY = "llama-3.3-70b-versatile"
MODEL_SECONDARY = "mixtral-8x7b-32768"
MODEL_LIGHTWEIGHT = "llama3-8b-8192"

# Embeddings & Vector DB
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
VECTOR_DB_PATH = "chroma_db_store"

# Retry Mechanism
MAX_API_RETRIES = 3
INITIAL_BACKOFF_SECONDS = 2.0

# --------------------------------------------------
# DETERMINISTIC STAGE WEIGHTS FOR SCORING
# --------------------------------------------------
# Pre-seed: prioritizes Innovation and Founder capability
# Seed: balances Traction, Founder, and Market
# Series A: prioritizes Revenue, Unit Economics, and Scalability
STAGE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Pre-seed": {
        "innovation_defensibility": 0.25,
        "founder_capability": 0.25,
        "market_potential": 0.15,
        "revenue_viability": 0.10,
        "scalability": 0.10,
        "competition_risk": 0.10,
        "funding_readiness": 0.05,
    },
    "Seed": {
        "innovation_defensibility": 0.15,
        "founder_capability": 0.20,
        "market_potential": 0.20,
        "revenue_viability": 0.15,
        "scalability": 0.10,
        "competition_risk": 0.10,
        "funding_readiness": 0.10,
    },
    "Series A": {
        "innovation_defensibility": 0.10,
        "founder_capability": 0.15,
        "market_potential": 0.15,
        "revenue_viability": 0.25,
        "scalability": 0.20,
        "competition_risk": 0.10,
        "funding_readiness": 0.05,
    }
}

# --------------------------------------------------
# DETERMINISTIC CONFIDENCE PENALTY SCHEMA
# --------------------------------------------------
# Start Confidence is 10.0. Penalties subtract from 10.0.
CONFIDENCE_BASE_SCORE = 10.0
CONFIDENCE_MINIMUM = 1.0

CONFIDENCE_PENALTY_TAM = 1.5           # Missing market sizing
CONFIDENCE_PENALTY_REVENUE = 2.0       # Missing MRR or gross margin
CONFIDENCE_PENALTY_TRACTION = 1.5      # Missing active users or YoY growth
CONFIDENCE_PENALTY_FOUNDERS = 2.0      # Missing founder team completely
CONFIDENCE_PENALTY_COMPETITION = 1.5   # Missing competitor lists
CONFIDENCE_PENALTY_FOUNDER_DETAIL = 1.0 # Omitted key background detail per founder

# --------------------------------------------------
# RISK DEDUCTION COEFFICIENTS
# --------------------------------------------------
# Reduces the final overall score based on the severity of registered risks
RISK_PENALTY_HIGH = 0.40
RISK_PENALTY_MEDIUM = 0.15
RISK_PENALTY_LOW = 0.00
