🛠️ Self-Healing Cleanup Automation System

📌 Overview

This project demonstrates a monitor-driven, self-healing automation system designed to automatically clean up old files when triggered by an incident (e.g., from ServiceNow).

It simulates how modern SRE / DevOps teams reduce manual intervention by integrating:
	•	Monitoring systems (e.g., Zabbix)
	•	Incident management tools (e.g., ServiceNow)
	•	Automation services (Python API)
	•	CI/CD pipelines (GitHub Actions)

⸻

🧠 Problem Statement

In enterprise environments, disk space issues are common and can lead to:
	•	Application downtime
	•	Performance degradation
	•	Manual operational overhead

Traditionally, cleanup is done via:
	•	Cron jobs ❌ (not dynamic)
	•	Manual intervention ❌ (not scalable)

⸻

✅ Solution

This project implements an event-driven self-healing system:
	•	Detect issue (disk usage high)
	•	Create incident
	•	Trigger automation via API
	•	Perform cleanup
	•	Resolve incident automatically

⸻

🧭 Architecture

Monitoring Tool (Zabbix)
        ↓
ServiceNow Incident (INC12345)
        ↓
REST API Call
        ↓
Flask Application (/cleanup)
        ↓
Service Layer (Orchestration)
        ↓
Cleanup Logic (File Deletion)
        ↓
Logs + Response
        ↓
Incident Updated / Resolved


⸻

🔁 End-to-End Flow

simulate_servicenow.sh
        ↓
POST /cleanup
        ↓
Flask API (routes.py)
        ↓
Service Layer (service.py)
        ↓
Cleanup Engine (file_cleanup.py)
        ↓
File System Cleanup
        ↓
Logs generated
        ↓
JSON response returned


⸻

📁 Project Structure

self-healing-cleanup/
│
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # API endpoints
│   ├── service.py           # Orchestration logic
│   │
│   ├── cleanup/
│   │   ├── file_cleanup.py  # Cleanup engine
│   │   └── utils.py         # Helper functions
│   │
│   ├── config.py            # Configuration
│   └── logger.py            # Logging setup
│
├── scripts/
│   └── simulate_servicenow.sh   # Simulates ServiceNow trigger
│
├── tests/
│   └── test_cleanup.py      # Unit tests
│
├── logs/                   # Runtime logs
├── .github/workflows/      # CI/CD pipeline
├── run.py                  # Entry point
├── requirements.txt
└── README.md


⸻

🚀 How to Run Locally

🔹 1. Setup Environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🔹 2. Start API

python run.py

🔹 3. Trigger Cleanup (Simulate ServiceNow)

bash scripts/simulate_servicenow.sh


⸻

🧪 Testing

Run unit tests:

PYTHONPATH=. pytest tests/

✔️ What is Tested
	•	Old files are deleted
	•	New files are retained
	•	Invalid directory handling

⸻

⚙️ Configuration

Defined in app/config.py:

CLEANUP_DIRECTORY = "/tmp/test_cleanup"
RETENTION_DAYS = 7


⸻

📡 API Details

Endpoint

POST /cleanup

Request

{
  "incident": "INC12345",
  "server": "local"
}

Response

{
  "incident": "INC12345",
  "server": "local",
  "status": "success",
  "deleted_files": 3,
  "errors": 0
}


⸻

🪵 Logging

Logs are stored in:

logs/cleanup.log

Example:

Cleanup triggered for Incident: INC12345
Deleted file: /tmp/test_cleanup/file1.txt
Cleanup completed


⸻

🔁 CI/CD Pipeline (GitHub Actions)

Pipeline stages:

BUILD → TEST → ARTIFACT → DEPLOY

✔️ Features
	•	Dependency installation
	•	Automated testing (pytest)
	•	Artifact packaging
	•	Simulated deployment

⸻

🚀 Deployment Options

🔹 1. Local Deployment (Self-hosted runner)
	•	Extract artifact
	•	Setup virtual environment
	•	Run Flask app

🔹 2. VM Deployment

GitHub Actions → SSH → VM → Deploy

	•	Copy files
	•	Install dependencies
	•	Run service using nohup

🔹 3. Cloud Deployment (PCF)
	•	cf push application
	•	Managed scaling and routing

⸻

🔐 Security Considerations
	•	HTTPS (TLS certificates)
	•	Token-based authentication
	•	API Gateway integration
	•	Input validation

⸻

🧠 Key Concepts Demonstrated
	•	Event-driven automation
	•	Self-healing systems
	•	REST API integration
	•	CI/CD pipelines
	•	Observability (logging)
	•	Test-driven validation

⸻

💬 Interview Talking Points
	•	“Implemented a self-healing system triggered by incidents instead of cron jobs”
	•	“Designed modular architecture with API, service, and execution layers”
	•	“Simulated ServiceNow integration using curl-based scripting”
	•	“Implemented CI/CD pipeline with build, test, and deployment stages”

⸻

🔥 Future Enhancements
	•	Add authentication (JWT/API key)
	•	Integrate with real ServiceNow API [result back to ServiceNow]
	•	Add Prometheus metrics
	•	Dockerize application
	•	Deploy on Kubernetes

⸻

👨‍💻 Author

Suraj Armugham

⸻

⭐ Summary

This project demonstrates how modern organizations move from:

Manual Ops ❌ → Automated Self-Healing Systems ✅

It reflects real-world practices used in:
	•	SRE teams
	•	DevOps environments
	•	Production support engineering