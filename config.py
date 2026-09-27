import os
from dotenv import load_dotenv

load_dotenv()
MAINTENANCE_START=os.getenv("MAINTENANCE_START","02:00")
MAINTENANCE_END=os.getenv("MAINTENANCE_END","03:00")
UPDATE_SCHEDULE=os.getenv("UPDATE_SCHEDULE","01:30")
MIN_ACCURACY=float(os.getenv("MIN_ACCURACY","0.90"))
MIN_GROUNDING=float(os.getenv("MIN_GROUNDING","0.90"))
MAX_LATENCY_MS=int(os.getenv("MAX_LATENCY_MS","3000"))
ROLLBACK_HEALTH_WINDOW_SECONDS=int(os.getenv("ROLLBACK_HEALTH_WINDOW_SECONDS","300"))
RETRY_DELAYS_MINUTES=(15,30,60)
KNOWLEDGE_DIR=os.getenv("KNOWLEDGE_DIR","knowledge")
QUARANTINE_DIR=os.getenv("QUARANTINE_DIR","quarantine")
STATE_FILE=os.getenv("STATE_FILE","state.json")
AUDIT_LOG=os.getenv("AUDIT_LOG","audit.log")