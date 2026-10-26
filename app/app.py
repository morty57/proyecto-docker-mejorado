from flask import Flask, request
import os
import psycopg2
import redis
import json

app = Flask(__name__)
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, port=DB_PORT, connect_timeout=3)


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True,
                       socket_connect_timeout=3)


@app.route("/")
def home():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
        get_redis().ping()
        return {
            "mensaje": "Aplicacion desplegada y funcionando correctamente",
            "database": "PostgreSQL conectado",
            "redis": "Redis conectado",
            "version": version,
            "endpoints": {"crear_tarea": "POST /process", "salud": "/health"}
        }
    except Exception as exc:
        return {"mensaje": "Error en la aplicación", "error": str(exc)}, 503


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/process", methods=["POST"])
def process():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    if not text:
        return {"error": "Envía un JSON con el campo text, por ejemplo {\"text\": \"hola\"}"}, 400
    task = {"text": text}
    task_id = get_redis().incr("task_counter")
    task["id"] = task_id
    get_redis().rpush("tasks", json.dumps(task))
    return {"mensaje": "Tarea enviada al worker", "task": task}, 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
