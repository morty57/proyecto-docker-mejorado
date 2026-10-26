FROM python:3.11-slim
WORKDIR /worker
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir redis==5.2.1
COPY worker.py .
CMD ["python", "worker.py"]
