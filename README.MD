#  Multi AI Agent System (Confidence Scoring & Orchestration)

A **production-deployed**, scalable Multi-Agent LLMOps system featuring a custom orchestration engine. Built with a **Supervisor/Router pattern** and **Map-Reduce (Scatter-Gather)** execution to dynamically parse user queries, route to the most capable expert agents, execute in parallel, and synthesize a finalized response — all deployed on AWS ECS Fargate via a full CI/CD pipeline.

> 🚀 **Live Deployment:** Containerized and actively running on AWS ECS Fargate with Jenkins CI/CD, SonarQube quality gates, and Amazon ECR image registry.

---

## ✨ Key Features

- **Intelligent Routing:** A specialized Router Agent assigns confidence scores (0–1) to determine which expert agents (Research, Medical, or Coding) are best equipped to handle a query. Agents below a `CONFIDENCE_THRESHOLD` of 0.3 are discarded.
- **Asynchronous Parallel Execution:** Selected agents run entirely in parallel via `asyncio.gather`, drastically reducing latency and overcoming traditional sequential multi-agent bottlenecks.
- **Automated Aggregation:** An Aggregation Agent compiles separate expert outputs into a single, cohesive synthesized response.
- **Interactive UI & Memory:** Streamlit provides a dynamic, streaming chat interface with session-assigned continuous memory.
- **Decoupled API Backend:** FastAPI exposes a scalable `/chat` REST endpoint, fully separating LLM computation from the frontend.

---

## 🏗️ System Architecture

```mermaid
graph TD
    User([User Query]) --> UI[Streamlit Frontend]
    UI -- "REST POST /chat" --> API[FastAPI Backend]
    API --> Memory[(Session Memory Store)]
    API --> Orch{Orchestrator}
    
    Orch -- "1. route_query()" --> Router[Router Agent]
    Router -- "2. [{'Coding': 0.9, 'Medical': 0.1}]" --> Orch
    
    Orch -- "3. Async Parallel Execution" --> Research[Research Agent + Wikipedia/Arxiv]
    Orch -- "3. Async Parallel Execution" --> Medical[Medical Agent + Wikipedia/Tavily]
    Orch -- "3. Async Parallel Execution" --> Coding[Coding Agent]
    
    Research --> Agg[Aggregator Agent]
    Medical --> Agg
    Coding --> Agg
    
    Agg -- "4. Synthesize Final Output" --> Orch
    Orch --> API
    API -- "Stream Tokens" --> UI
```

### Component Breakdown

**1. Frontend (`app/frontend/ui.py`)**
- Built with Streamlit; tracks conversations via uniquely generated `session_id`s.
- Uses `iter_content` to stream response chunks for a typewriter-like feel.

**2. Backend (`app/backend/api.py`)**
- Async FastAPI application exposing a centralized JSON pipeline.
- Handles model context switching (Google Gemini vs Groq LLaMA), session memory updates, and orchestrator delegation.

**3. Core Engine (`app/core/orchestrator.py`)**
The cornerstone of the system:
1. **Routing** — Router LLM performs zero-shot reasoning and outputs agent confidence scores as JSON.
2. **Filtering** — Agents below `CONFIDENCE_THRESHOLD = 0.3` are discarded.
3. **Execution** — Filtered agents fired asynchronously via `asyncio.gather`.
4. **Aggregation** — Aggregator LLM consolidates expert responses into a final articulate answer.

---

## ⚙️ CI/CD & Infrastructure Pipeline

This project is fully production-deployed with an automated DevOps pipeline:

```
GitHub Push → Jenkins Pipeline → SonarQube Analysis → Docker Build → AWS ECR Push → AWS ECS Fargate Deploy
```

### Pipeline Stages

| Stage | Tool | Status |
|---|---|---|
| Source Control | GitHub + Jenkins Webhook | ✅ Automated |
| Code Quality | SonarQube (Quality Gate) | ✅ Passed |
| Containerization | Docker | ✅ 320 MB image |
| Image Registry | AWS ECR (`my-repo`) | ✅ 3 images pushed |
| Orchestration | AWS ECS Fargate | ✅ 1/1 tasks running |
| Networking | AWS VPC + Security Groups | ✅ Ports 8501, 9999 open |

### SonarQube Code Quality Report

| Metric | Result |
|---|---|
| Security Issues | 0 |
| Reliability Issues | 0 |
| Maintainability Issues | 4 (minor) |
| Security Hotspots | 2 (reviewed) |
| Coverage | 0.0% (to be added) |
| Duplications | 0.0% |
| **Quality Gate** | ✅ **Passed** |

### AWS Infrastructure

- **ECR:** Docker image (`latest`) pushed to private registry — `324793866606.dkr.ecr.us-east-1.amazonaws.com/my-repo`
- **ECS Cluster:** `multi-ai-agent-cluster` — 1 active service, 1/1 tasks running
- **Task Definition:** `multi-ai-agent-def:1` — Deployment status: Success
- **VPC Security Group:** Custom inbound rules for ports 8501 (Streamlit) and 9999 (FastAPI)

> 📸 **Screenshots of live deployment, Jenkins console, SonarQube dashboard, and ECS cluster are available in `/assets/screenshots/`**

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- Valid API keys for Google Gemini GenAI, Groq, and Tavily

### 1. Setup Environment

Configure your `.env` file in the root directory:

```bash
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Launches both FastAPI backend (port 9999) and Streamlit frontend (port 8501) concurrently:

```bash
python -m app.main
```

### 4. Access the App

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI Backend | http://localhost:9999 |
| API Docs | http://localhost:9999/docs |

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| LLM Orchestration | LangChain, LangGraph, LangGraph-Groq |
| Inference | Groq LPU (LLaMA 3.3-70B), Google Gemini |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Containerization | Docker |
| CI/CD | Jenkins, SonarQube |
| Cloud | AWS ECR, AWS ECS Fargate, AWS VPC |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
Multi-AI-Agent/
├── app/
│   ├── backend/
│   │   └── api.py              # FastAPI backend
│   ├── frontend/
│   │   └── ui.py               # Streamlit UI
│   ├── core/
│   │   └── orchestrator.py     # Core routing & execution engine
│   └── main.py                 # Entry point
├── custom_jenkins/             # Jenkins pipeline config
├── Dockerfile
├── setup.py
├── requirements.txt
└── README.md
```

---

## 📊 Performance

| Metric | Value |
|---|---|
| Routing Decision Latency | < 800ms |
| End-to-End Orchestration | < 4 seconds |
| Parallel Agents (max) | 3 concurrent |
| Inference Backend | Groq LPU (ultra-low latency) |
| Codebase | 501 Lines of Code |

---

## 🔮 Future Improvements

- Add unit test coverage (target: >80% for SonarQube quality gate)
- Implement horizontal scaling via ECS auto-scaling policies
- Add CloudWatch monitoring and alerting
- Integrate additional expert agents (Finance, Legal)
- Add HTTPS via AWS Certificate Manager + ALB

---

## 👤 Author

**Amit Singh**  
NIT Jamshedpur
[LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/Amitgitup)