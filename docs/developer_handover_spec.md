# Elephant Tank AI: Frontend & Backend Dev Integration Specification

This document details the exact technical configurations, endpoint schemas, and required codebase changes to enable seamless multi-device collaboration between the Frontend (UI/UX) dev team, the Backend dev team, and the Elephant Tank AI Core service.

---

## 🚀 PART 1: SUGGESTED CODEBASE CHANGE (Requires Confirmation)

Currently, the core FastAPI entry point at `app/api/main.py` has no Cross-Origin Resource Sharing (CORS) policy registered. 
* **The Problem:** Without CORS configuration, frontend browsers on different devices trying to make direct API requests to Elephant Tank AI will be blocked by standard browser security (Same-Origin Policy).
* **The Proposed Fix:** Register FastAPI's `CORSMiddleware` inside `app/api/main.py`.

### Proposed Code Modification:
```diff
 from fastapi import FastAPI
 from fastapi.exceptions import RequestValidationError
+from fastapi.middleware.cors import CORSMiddleware
 from app.endpoints.evaluation import router as eval_router
 from app.endpoints.health import router as health_router
 from app.middleware.error_handler import validation_exception_handler, global_exception_handler
@@ -19,6 +20,15 @@
         version="1.0.0"
     )
     
+    # Enable CORS for external Frontend access across devices
+    app.add_middleware(
+        CORSMiddleware,
+        allow_origins=["*"],  # In production, specify: ["https://your-frontend-app.com"]
+        allow_credentials=True,
+        allow_methods=["*"],
+        allow_headers=["*"],
+    )
+    
     # Bind custom error middleware
     app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

> [!IMPORTANT]
> **Please confirm if we should apply this CORS change to `app/api/main.py`. We will not build or apply it until you explicitly type "CONFIRM".**

---

## 🎨 PART 2: THE FRONTEND (UI/UX) INTEGRATION SPEC

Frontend developers will construct HTTP calls to communicate either directly with your Ngrok/tunnel URL or through your backend's proxy route.

### 1. File Upload Dropzone (Pitch Deck Ingestion)
* **Endpoint:** `POST /upload-startup-documents`
* **Content-Type:** `multipart/form-data`
* **Axios Snippet Example:**
  ```javascript
  const formData = new FormData();
  formData.append("file", fileInput.files[0]); // Pitch deck PDF
  
  axios.post("http://<api-url>/upload-startup-documents", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  })
  .then(res => {
    // res.data is the structured StartupEvaluationResponse
    updateUIRadarChart(res.data.evaluation_results);
  });
  ```
* **UI Mapping Guidelines:**
  - **Radar Chart:** Map `evaluation_results` (`innovation_score`, `market_score`, `scalability_score`, `founder_score`, `funding_readiness_score`) onto a 5-axis Radar Chart.
  - **Overall Score Dial:** Display `evaluation_results.overall_score` (Scale: 0-100) inside a premium Circular Gauge.

---

### 2. Strategic Ecosystem Matchmaking
* **Endpoint:** `POST /match-investors`
* **Content-Type:** `application/json`
* **Axios Snippet Example:**
  ```javascript
  axios.post("http://<api-url>/match-investors", {
    target_stage: "Seed",
    startup_description: "PACS clinical medical imaging SaaS.",
    limit: 3
  })
  .then(res => {
    // List of match cards containing alignment and fit ratings
    renderInvestorCards(res.data.matches);
  });
  ```
* **UI Mapping Guidelines:**
  - Render cards containing `fit_rating` as a badge, `investment_thesis_alignment` as body text, and `match_reasoning` as a highlighted dropdown drawer.

---

### 3. What-If Ecosystem Shock Simulation
* **Endpoint:** `POST /simulation/shock`
* **Content-Type:** `application/json`
* **Axios Snippet Example:**
  ```javascript
  axios.post("http://<api-url>/simulation/shock", {
    startup_name: "MediVision AI",
    shock_type: "REGULATORY_CRACKDOWN"
  })
  .then(res => {
    // Renders before vs after score comparisons
    renderShockSimulationResults(res.data);
  });
  ```
* **UI Mapping Guidelines:**
  - Display a side-by-side metric delta comparison showing the score drop (e.g., **`84 -> 67`** colored in warning Orange/Red) and the AI-generated mitigation strategies in an expandable checklist.

---

## ⚙️ PART 3: THE BACKEND INTEGRATION SPEC

Backend developers will act as secure gatekeepers, proxying frontend requests and updating deal execution logs.

### 1. Ingestion Document Relay (Proxying multipart)
* **Goal:** Accept a file from the frontend and securely stream/relay it to the Elephant Tank AI container.
* **Node.js Express Proxy Code Example:**
  ```javascript
  const express = require('express');
  const multer = require('multer');
  const axios = require('axios');
  const FormData = require('form-data');
  
  const upload = multer();
  const app = express();
  
  app.post('/api/deals/ingest', upload.single('file'), async (req, res) => {
    try {
      const relayForm = new FormData();
      relayForm.append('file', req.file.buffer, { filename: req.file.originalname });
      
      const aiResponse = await axios.post('http://elephant-tank-ai:8090/upload-startup-documents', relayForm, {
        headers: { ...relayForm.getHeaders() }
      });
      
      res.json(aiResponse.data);
    } catch (err) {
      res.status(500).json({ error: "Ingestion proxy failed: " + err.message });
    }
  });
  ```

---

### 2. Consuming Real-Time Dual Timestamps
* **Format:** Every successful intelligence execution output contains the dynamic stage traces:
  ```json
  "execution_logs": [
    {
      "stage": "STARTUP_EVALUATION",
      "status": "SUCCESS",
      "message": "Qualitative reasoning generated by Groq. Deterministic scoring and confidence calculated locally.",
      "timestamp_unix": 1779836712,
      "timestamp_readable": "2026-05-27T09:45:12+05:30"
    }
  ]
  ```
* **Database Mapping:** Store the `timestamp_unix` as an indexable integer column in your history tables, and use `timestamp_readable` directly in system audit dashboards to track deal execution logs.
