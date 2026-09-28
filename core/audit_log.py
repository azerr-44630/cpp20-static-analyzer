import json, os
from datetime import datetime, timezone

LOG_PATH = "logs/audit.log"

def log_action(skill_name, target, status, detail=""):
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "skill": skill_name,
        "target": target,
        "status": status,
        "detail": detail,
    }
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
