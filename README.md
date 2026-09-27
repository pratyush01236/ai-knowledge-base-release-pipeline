# AI Knowledge Base Release Pipeline

Production-oriented release pipeline for safely updating an AI/RAG knowledge base.

## Features
- Processes new/modified documents and detects exact duplicates with SHA-256.
- Quarantines empty, invalid, and prompt-injection-bearing documents.
- Maintains candidate versions, active version state, and rollback.
- Runs accuracy, grounding, and confidence quality gates before activation.
- Rejects updates that fail quality thresholds.
- Configurable maintenance window and scheduled release workflow.
- Retry plan after failures: 15, 30, and 60 minutes.
- Post-activation health check with automatic rollback to the previous version.
- RBAC roles: viewer, editor, release-manager, admin.
- Prompt-injection protection and sensitive-data masking.
- Monitoring hooks for latency, failures, confidence, and escalations.
- GitHub Actions tests and scheduled release runner.

## Run locally
python -m venv venv
pip install -r requirements.txt
Copy .env.example to .env
uvicorn app:app --reload

## API
GET / = health and active version.
POST /ingest = upload; requires X-Role: editor.
POST /release = quality gate and activation; requires X-Role: release-manager.
POST /retry = 15/30/60 minute retry plan; requires X-Role: release-manager.
GET /metrics = monitoring metrics; requires X-Role: viewer.

## Configuration
MAINTENANCE_START and MAINTENANCE_END define the activation window.
UPDATE_SCHEDULE documents the intended update time; scheduled-release.yml runs at 01:30 UTC and supports manual runs.
MIN_ACCURACY, MIN_GROUNDING, MAX_LATENCY_MS are configurable thresholds.
ROLLBACK_HEALTH_WINDOW_SECONDS defaults to 300 seconds (five minutes).

## Production hardening
For production, replace local JSON/file storage with a transactional database and object storage, add a durable scheduler/queue, malware scanning, MIME validation, SSO/OIDC, immutable audit logs, encryption, distributed health probes, and persistent metrics.