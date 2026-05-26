# Elephant Tank AI: Foundational Core Intelligence Engine (Phase 0)

This is the production-ready foundational intelligence layer for **Elephant Tank AI** — a startup intelligence, venture evaluation, and investment due diligence engine. 

The system operates strictly under professional Venture Capital (VC) screening, incubator assessment, and due diligence standards. It completely separates **qualitative LLM synthesis (reasoning)** from **deterministic local aggregation, stage weights, and completeness penalties**.

---

## 1. Core Architecture Blueprint

```
d:\STARTUP\
├── requirements.txt                 # Project third-party dependencies
├── README.md                        # Documentation and setup manual
├── elephant_tank/
│   ├── __init__.py                  # Package exports
│   ├── config.py                    # Model routing, weights, and confidence parameters
│   ├── schemas.py                   # Pydantic data contracts (Ingestion & Final Output)
│   ├── prompts.py                   # System and evaluation prompt templates
│   ├── deterministic_logic.py       # Completeness, stage-weighting, and risk penalty algorithms
│   ├── groq_client.py               # Rate-limit resilient Groq client with simulation fallback
│   └── orchestrator.py              # Operational pipeline coordinator
└── tests/
    └── test_evaluation.py           # Automated test suite (Pre-seed & Series A scenarios)
```

---

## 2. Quantitative Engine Specifications

### 2.1 Confidence Completeness Scoring
The system initializes the completeness score at `10.0`. Missing fields are penalized to prevent false precision in early assessments:
*   **TAM/SAM/SOM Omissions**: `-1.5` points
*   **MRR/Gross Margin Omissions**: `-2.0` points
*   **Growth/Active User Omissions**: `-1.5` points
*   **Empty Co-Founder Registry**: `-2.0` points
*   **Empty Competitor Registry**: `-1.5` points
*   **Missing Founder Domain Detail**: `-1.0` point per founder

### 2.2 Stage-Weighted Scoring Grid
Calculated raw dimension scores (1.0 to 10.0) are combined using weights matching the startup's maturity:

| Dimension | Pre-seed | Seed | Series A |
| :--- | :---: | :---: | :---: |
| **Innovation & Defensibility** | **25%** | 15% | 10% |
| **Founder Capability** | **25%** | 20% | 15% |
| **Market Potential** | 15% | **20%** | 15% |
| **Revenue Viability** | 10% | 15% | **25%** |
| **Scalability** | 10% | 10% | **20%** |
| **Competition & Risk** | 10% | 10% | 10% |
| **Funding Readiness** | 5% | 10% | 5% |

### 2.3 Risk Severity Score Penalties
High and Medium severity threats registered in the AI's risk assessment registry are deducted from the overall score:
*   **High Severity Risk**: `-0.40` deduction per risk.
*   **Medium Severity Risk**: `-0.15` deduction per risk.
*   **Low Severity Risk**: `0.00` deduction.

---

## 3. Getting Started

### 3.1 Setup Virtual Environment and Install Dependencies
Initialize a standard Python virtual environment inside the workspace and install the verified packages:

```bash
# Create environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3.2 Running in Production Mode (with Groq API)
Provide your Groq API Key as an environment variable to execute live AI synthesis:

```powershell
$env:GROQ_API_KEY="your-groq-api-key-here"
```

### 3.3 Running in Simulation/Testing Mode (No Key Required)
If no `GROQ_API_KEY` is set in the environment, the engine will **automatically detect it and fall back to the offline VC screening simulator**. This allows you to immediately run and test the complete pipeline offline without API bills or keys.

---

## 4. Running the Standardized Test Harness
To verify Pydantic types, data completeness penalties, and stage weight routing, execute `pytest`:

```bash
pytest -v tests/test_evaluation.py
```
