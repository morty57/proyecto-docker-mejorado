#!/usr/bin/env bash
set -euo pipefail
if [[ ! -f .env ]]; then
  echo "Falta .env. Ejecuta: cp .env.example .env y completa DOCKERHUB_USERNAME."
  exit 1
fi
source .env
: "${DOCKERHUB_USERNAME:?Completa DOCKERHUB_USERNAME en .env}"
TAG="${IMAGE_TAG:-latest}"
docker build -t "${DOCKERHUB_USERNAME}/proyecto-docker-web:${TAG}" ./app
docker build -t "${DOCKERHUB_USERNAME}/proyecto-docker-worker:${TAG}" ./worker
docker build -t "${DOCKERHUB_USERNAME}/proyecto-docker-visualizer:${TAG}" ./visualizer
docker login
docker push "${DOCKERHUB_USERNAME}/proyecto-docker-web:${TAG}"
docker push "${DOCKERHUB_USERNAME}/proyecto-docker-worker:${TAG}"
docker push "${DOCKERHUB_USERNAME}/proyecto-docker-visualizer:${TAG}"
echo "Imágenes publicadas correctamente."
