# 🐘 Elephant Tank AI: Integration & Handoff Guide

Hello Developer! 👋 

This repository contains the **Core AI Intelligence Layer** for Elephant Tank. It was designed to run entirely as a standalone **Microservice**. 

You do **not** need to merge this Python code into your main backend (Node.js, Django, Spring, etc.). Instead, you just need to run this AI engine on a server, and have your main backend make standard HTTP REST calls to it.

This document will explain exactly how to boot it up and how to connect it to your existing Frontend and Main Database.

---

## 🛠️ 1. How to Run the AI Layer Locally

The AI Layer is built with **FastAPI**. It requires Python 3.9+.

### Step 1: Clone and Setup
Open your terminal and clone the repository:
```bash
git clone https://github.com/patareshivraj/Elephant-Tank-AI-Core-Intelligence-Layer.git
cd Elephant-Tank-AI-Core-Intelligence-Layer
```

Create a virtual environment and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Set the API Key
Create a `.env` file in the root directory (same folder as this file) and add the Groq API key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### Step 3: Boot the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
```
The AI engine is now running locally at `http://localhost:8000`!

---

## 🔌 2. How to Connect Your Backend (The Data Flow)

Your Main Backend and the AI Layer will work together in a simple "Handshake" workflow.

**The Workflow:**
1. **User Upload:** A startup founder uploads their Pitch Deck PDF on your Frontend.
2. **Main Backend Receives:** Your Main Backend receives the PDF and saves the file/text to your Main Database.
3. **The AI Handshake:** Your Main Backend makes an internal HTTP `POST` request to our AI Layer (`http://localhost:8000/evaluate-startup`). You send the startup's data in the JSON body.
4. **AI Processing:** Our AI Layer does all the heavy lifting. It reads the data, runs the mathematical scoring, uses LLMs to generate VC-grade reports, and checks for hallucination errors.
5. **The Handoff:** Our AI Layer returns a massive, highly structured JSON object (containing scores, risk flags, and the generated VC memo) back to your Main Backend.
6. **Final Display:** Your Main Backend takes our JSON response, saves the scores in your Main Database, and serves it to your Frontend to display to the user.

---

## 📖 3. The API Documentation

You do not need to guess what the JSON requests and responses look like. FastAPI has automatically generated an interactive documentation page for you.

With the server running (Step 3), open your web browser and go to:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Key Endpoints to look at:
*   `GET /system-health`: Use this to verify the AI server is running and the Groq API key is valid.
*   `POST /evaluate-startup`: This is the primary workhorse. Send the startup's data here to receive the final intelligence report.

---

## 💡 4. Important Notes for the Main Developer

*   **Asynchronous:** The AI evaluations can take anywhere from 5 to 15 seconds depending on the complexity of the startup. Ensure your Main Backend does not time out waiting for the HTTP response.
*   **Determinism:** The AI Layer handles its own Error Trapping. If a payload is malformed, it will not crash with a messy Python stack trace. It will return a clean 422 JSON error detailing exactly which fields your Main Backend missed.
*   **Caching:** The AI layer uses MD5 payload hashing. If you send the exact same startup profile twice in a row, the AI will bypass the LLMs and return the cached answer in 10 milliseconds.

Good luck integrating, and let us know if you need any API schema adjustments! 🚀
