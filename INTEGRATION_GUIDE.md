# Integration Guide: Elephant Tank AI Core Intelligence Layer

This document outlines the procedure for connecting the AI Intelligence Layer to an external primary backend system. 

The AI Layer operates as a standalone Python microservice. It exposes a REST API via FastAPI. It does not require direct code merging with external Node.js, Java, or Django codebases.

---

## 1. Environment Setup

The service requires Python 3.9 or higher.

### Repository Initialization
Execute the following commands to clone the repository and configure the virtual environment:

```bash
git clone https://github.com/patareshivraj/Elephant-Tank-AI-Core-Intelligence-Layer.git
cd Elephant-Tank-AI-Core-Intelligence-Layer
python -m venv venv
```

Activate the virtual environment:
* Linux/macOS: `source venv/bin/activate`
* Windows: `.\venv\Scripts\activate`

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the root directory and configure the required API key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### Service Execution
Initialize the FastAPI server using Uvicorn:
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```
The API is now accessible locally at `http://localhost:8000`.

---

## 2. Integration Architecture

The interaction between the primary backend and the AI microservice follows a standard HTTP request-response cycle.

### Data Flow Execution
1. **Data Ingestion:** The primary backend receives a startup PDF or text payload from the client frontend.
2. **API Request:** The primary backend executes an HTTP POST request to the AI Layer endpoint (`http://localhost:8000/evaluate-startup`). The payload must be formatted as JSON according to the required schema.
3. **Processing:** The AI Layer executes document extraction, mathematical scoring, large language model inference, and vector embedding generation.
4. **API Response:** The AI Layer returns a structured JSON object containing the finalized evaluation metrics, risk flags, and generated text reports.
5. **Data Persistence:** The primary backend stores the returned JSON values in its primary database and serves the data to the frontend client.

---

## 3. API Contract Documentation

The AI Layer automatically generates OpenAPI (Swagger) documentation based on its Pydantic schemas. 

With the server running, navigate to the following URL to view the exact JSON structures required for requests and responses:
**http://localhost:8000/docs**

### Primary Endpoints
* `GET /system-health`: Validates server uptime and verifies API key configuration.
* `POST /evaluate-startup`: The primary endpoint for submitting startup data and receiving the comprehensive evaluation report.

---

## 4. Technical Implementation Notes

* **Latency:** Evaluation processing requires 5 to 15 seconds. The primary backend must configure HTTP timeout settings accordingly.
* **Error Handling:** The AI API enforces strict schema validation. Invalid payloads will return a standard `422 Unprocessable Entity` HTTP response containing a JSON array of the specific missing or invalid fields.
* **Caching Mechanisms:** The system implements local MD5 hashing. Duplicate payload submissions will bypass the LLM inference pipeline and return cached JSON responses to reduce latency and API usage.
