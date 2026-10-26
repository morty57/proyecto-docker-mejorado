import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
import redis

client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"),
                     port=int(os.getenv("REDIS_PORT", "6379")), decode_responses=True)
results_file = Path(os.getenv("RESULTS_FILE", "/data/results.json"))
results_file.parent.mkdir(parents=True, exist_ok=True)

print("Worker iniciado; esperando tareas en Redis...", flush=True)
while True:
    try:
        item = client.blpop("tasks", timeout=5)
        if not item:
            continue
        task = json.loads(item[1])
        result = {
            "id": task.get("id"),
            "input": task.get("text", ""),
            "result": str(task.get("text", "")).upper(),
            "processed_at": datetime.now(timezone.utc).isoformat()
        }
        try:
            results = json.loads(results_file.read_text()) if results_file.exists() else []
        except (json.JSONDecodeError, OSError):
            results = []
        results.append(result)
        temporary = results_file.with_suffix(".tmp")
        temporary.write_text(json.dumps(results, ensure_ascii=False, indent=2))
        temporary.replace(results_file)
        print(f"Tarea procesada: {result['id']}", flush=True)
    except Exception as exc:
        print(f"Error del worker: {exc}", flush=True)
        time.sleep(2)
