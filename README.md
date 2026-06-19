<div align="center">
  <h1>Xeora 🚀</h1>
  <p><b>Autonomous Multi-Agent Task Workspace</b></p>
  <p><i>An enterprise-grade platform executing concurrent, multi-agent automation workflows to systematically process high-volume, highly-unstructured operational communications.</i></p>
</div>

---

## 📖 Overview

In modern enterprise environments, systems and humans generate a massive amount of unstructured data every second—ranging from critical server syslogs and security alerts to customer feedback emails. **Xeora** bridges the gap between chaos and structure. 

Xeora is a highly scalable, autonomous workspace that ingests raw, unstructured payload strings, calculates their priority in real-time, and offloads them to a fleet of specialized AI Agents. These agents analyze the data, extract key entities, determine urgency, and recommend actionable next steps—all tracked via a low-latency, real-time React dashboard.

## ✨ Why Xeora? (Key Benefits)

- **Intelligent Triage:** Stop manually parsing alerts. Xeora uses a blazing-fast heuristics engine to weigh and queue payloads before handing them off to Deep Learning models for deep contextual analysis.
- **Polyglot Performance:** Combines the high-throughput, non-blocking asynchronous event loop of **Node.js** with the heavy-lifting, AI-native ecosystem of **Python**.
- **O(N log N) Priority Queuing:** Utilizing Redis-backed BullMQ, high-priority tasks (e.g., severe server outages) instantly jump ahead of low-priority tasks (e.g., routine database backups).
- **Real-Time Observability:** Leveraging Supabase's Realtime PostgreSQL engine, stakeholders can watch tasks move from `Queued` -> `Processing` -> `Completed` instantly on the glassmorphism dashboard.

---

## 🏗️ Technical Architecture

Xeora is built on a distributed microservice architecture, allowing independent scaling of the queuing system and the AI processing workers.

### 1. Ingestion & Queue Layer (Node.js & Redis)
- **Framework:** Express (TypeScript)
- **Engine:** BullMQ + Redis
- **Role:** Exposes a REST API to receive raw payloads. A fast keyword-weighing algorithm parses the payload to assign an integer priority score before dropping it into the priority queue.

### 2. Autonomous Agent Layer (Python)
- **Framework:** FastAPI + CrewAI + LangChain
- **Role:** Python background workers receive tasks forwarded from the Node.js queue. Specialized **CrewAI Agents** (Data Parsing Specialists & Action Engines) powered by **Google Gemini** orchestrate sequential tasks to extract entities and generate actionable recommendations.

### 3. Persistent Memory & State Layer (Supabase)
- **Database:** PostgreSQL
- **Role:** Acts as the central nervous system. Tracks asynchronous system logs, caches memory, and provides low-latency state validation across parallel background processing workers to prevent task duplication.

### 4. Presentation Layer (React)
- **Framework:** React 18 + Vite
- **Role:** A modern, glassmorphism-styled dashboard that subscribes to Supabase WebSockets to stream live task states and AI-generated outputs directly to the browser.

---

## 🎯 Technical Use Cases

1. **DevOps & SRE Incident Response:**
   - *Input:* A raw syslog indicating high CPU usage and connection timeouts.
   - *Xeora Action:* Identifies the severity as 'Critical', bumps it to the top of the queue, parses the exact server node, and recommends locking down the instance or scaling up resources.
2. **Customer Support Triage:**
   - *Input:* An angry email complaining about a billing error.
   - *Xeora Action:* Analyzes the sentiment, flags the urgency as 'High', extracts the Invoice ID, and routes a summary recommendation directly to the Finance team.
3. **Security Monitoring:**
   - *Input:* A messy JSON blob from a WAF detecting brute-force login attempts.
   - *Xeora Action:* Parses the attacking IP address, determines the target account, and recommends an immediate IP ban to the SecOps team.

---

## 🛠️ Getting Started (Local Deployment)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Required for Redis & local Supabase)
- Node.js (v18+)
- Python (v3.11 or v3.12)

### 1. Database & Broker Setup
Start the local Supabase environment and ensure your Redis container is running:
```bash
npx supabase start
```
*Note the API URL, Anon Key, and Service Role Key printed in your terminal.*

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
REDIS_HOST=localhost
REDIS_PORT=6379
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key
GEMINI_API_KEY=your_google_gemini_api_key
PORT=3000
MICROSERVICE_PORT=8000
```
Create a `.env` in the `/frontend` directory:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
```

### 3. Spin Up the Services

**Terminal 1: Node.js API & Queue**
```bash
cd backend
npm install
npm run dev:api
```

**Terminal 2: Node.js Worker**
```bash
cd backend
npm run dev:worker
```

**Terminal 3: Python AI Microservice**
```bash
cd microservice
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --port 8000
```

**Terminal 4: React Dashboard**
```bash
cd frontend
npm install
npm run dev
```

### 4. Send a Test Payload
Run the following PowerShell command to inject an unstructured string into the system and watch the dashboard update in real-time!
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/payloads" -Method Post -Body '{"id":"test-1", "raw_data":"URGENT: Server US-East-1 db-cluster-x9 down. CPU at 100%. Pls fix asap.", "source":"syslog"}' -ContentType "application/json"
```

---
*Built autonomously with Gemini for advanced workflow orchestration.*
