# 🐘 Elephant Tank AI: Core Intelligence Layer

Welcome to the **Elephant Tank AI Core Intelligence Layer**. 

This repository contains the backend AI engine for the Elephant Tank platform. It is a production-ready, VC-grade intelligence API designed to evaluate startups, score founders, match investors using semantic vector search, and generate professional investment memos.

> **Note for Frontend/Backend Developers:** If you are here to integrate this AI Layer into your existing application, please read the **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** for a simple, step-by-step setup and handoff guide.

---

## 🧠 System Philosophy

This engine was built under a strict "Deterministic-First" philosophy:
*   **No "AI Math"**: Large Language Models (LLMs) are notoriously bad at math and weighting. This system uses LLMs *strictly* for reading unstructured text and generating narrative prose. All venture scoring, stage-weighting, and risk penalties are calculated locally in Python using hardcoded rules.
*   **Zero-Psychology Profiling**: When evaluating founders, the engine is explicitly banned from inferring personality traits. It scores human capital purely on evidence (e.g., years of technical experience, prior exits).
*   **Hallucination Immune System**: Built-in Quality Assurance modules automatically trap and flag the LLM if it attempts to invent revenue numbers that were not present in the original pitch deck.

---

## 🏗️ The 10-Phase Pipeline Architecture

This engine was systematically built across 10 distinct phases, now fully unified into a single API service:

*   **Phase 1: Document Ingestion** - Extracts and cleans raw text from Pitch Deck PDFs.
*   **Phase 2: AI Reasoning** - Groq LLM (Llama 3) maps raw unstructured text into structured dimensions.
*   **Phase 3: Venture Scoring** - Python math engine calculates 0-100 scores based on startup stage (Pre-seed, Seed, Series A).
*   **Phase 4: Founder Intelligence** - Evaluates team execution readiness and flags structural risks (e.g., Solo founder dependency).
*   **Phase 5: Report Generation** - Compiles the hard scores into a 10-section Investor Memo using `mixtral-8x7b`.
*   **Phase 6: Semantic Matching** - Uses `ChromaDB` to embed the startup and match it with mathematically similar VCs/Mentors.
*   **Phase 7: Master Orchestration** - Asynchronously binds all phases into a single execution flow.
*   **Phase 8: Quality Assurance** - Pydantic schema validation and automated hallucination traps.
*   **Phase 9: FastAPI Service Layer** - Exposes the engine as a modular REST API with structured error handling.
*   **Phase 10: Performance Optimization** - Implements MD5 disk caching (skips redundant inferences) and dynamic model routing (saves API costs).

---

## 💻 Tech Stack

*   **API Framework**: `FastAPI` & `Uvicorn`
*   **Data Contracts**: `Pydantic`
*   **LLM Inference**: `Groq API` (llama3-8b, llama-3.3-70b-versatile, mixtral-8x7b-32768)
*   **Vector Database**: `ChromaDB`
*   **Embedding Model**: `BAAI/bge-small-en-v1.5` (via `Sentence-Transformers`)
*   **PDF Extraction**: `PyMuPDF`

---

## 🚀 Quick Start (For API Developers)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/patareshivraj/Elephant-Tank-AI-Core-Intelligence-Layer.git
   cd Elephant-Tank-AI-Core-Intelligence-Layer
   ```
2. **Install requirements:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set your Groq API Key:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
4. **Boot the API:**
   ```bash
   uvicorn app.api.main:app --reload
   ```
5. **View the Docs:**
   Navigate to `http://localhost:8000/docs` to see the automated Swagger API contracts.
