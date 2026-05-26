# Elephant Tank AI: Core Intelligence Layer

## Overview

This repository contains the backend intelligence API for the Elephant Tank platform. It is designed to process unstructured startup data, calculate quantitative capability scores, generate formatted evaluation reports, and perform semantic vector matching.

The system is deployed as a standalone REST API microservice utilizing FastAPI. External developers integrating this service should reference the `INTEGRATION_GUIDE.md` file for setup and configuration instructions.

---

## System Architecture and Constraints

The evaluation engine adheres to the following structural constraints:
* **Deterministic Execution:** Large Language Models are utilized strictly for text extraction and narrative generation. All mathematical scoring, stage-based weighting, and risk penalties are calculated locally via deterministic Python algorithms.
* **Evidence-Based Evaluation:** The founder evaluation module assesses human capital using explicit historical data (e.g., years of experience, prior exits). Psychological profiling and subjective personality inferences are explicitly restricted.
* **Validation and Quality Assurance:** Automated Pydantic schemas validate all outputs. Discrepancies between input data and generated text are intercepted by local hallucination detection algorithms.

---

## Development Phases

The backend engine was developed across ten sequential modules, integrated into a unified execution pipeline:

1. **Document Ingestion:** Parses and extracts raw text from PDF documents.
2. **AI Reasoning:** Maps unstructured text into categorical dimensions via LLM inference.
3. **Venture Scoring:** Executes deterministic mathematical scoring algorithms based on company stage.
4. **Founder Intelligence:** Evaluates operational readiness and identifies structural team risks.
5. **Report Generation:** Formats quantitative metrics into structured narrative documents.
6. **Semantic Matching:** Utilizes local vector databases to identify similar entities.
7. **Orchestration:** Binds all modules into an asynchronous execution flow.
8. **Quality Assurance:** Enforces data type contracts and structural validation.
9. **API Service Layer:** Exposes the pipeline via FastAPI REST endpoints.
10. **Performance Optimization:** Implements payload hashing for local caching and dynamic model routing.

---

## Technology Stack

* **API Framework:** FastAPI, Uvicorn
* **Data Validation:** Pydantic
* **LLM Integration:** Groq API (llama3-8b, llama-3.3-70b-versatile, mixtral-8x7b-32768)
* **Vector Database:** ChromaDB
* **Embedding Model:** BAAI/bge-small-en-v1.5 (Sentence-Transformers)
* **Document Processing:** PyMuPDF

---

## Local Execution Instructions

1. Clone the repository and navigate to the directory:
   ```bash
   git clone https://github.com/patareshivraj/Elephant-Tank-AI-Core-Intelligence-Layer.git
   cd Elephant-Tank-AI-Core-Intelligence-Layer
   ```

2. Initialize the virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure the environment variables by creating a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. Start the API server:
   ```bash
   uvicorn app.api.main:app --host 0.0.0.0 --port 8000
   ```

5. Access the automated OpenAPI documentation by navigating a web browser to `http://localhost:8000/docs`.
