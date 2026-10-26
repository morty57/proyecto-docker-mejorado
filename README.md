# Proyecto multicontenedor: Flask, PostgreSQL, Redis, Worker y Node.js

Aplicación demostrativa con cinco servicios coordinados por Docker Compose:

- **web**: API Flask en Python, publicada en `http://localhost:5001`.
- **db**: PostgreSQL, con datos persistentes en `postgres_data`.
- **redis**: cola de tareas y almacenamiento persistente de Redis en `redis_data`.
- **worker**: proceso Python que consume tareas de Redis, convierte el texto a mayúsculas y guarda los resultados en el volumen `results_data`.
- **visualizer**: aplicación Node.js que lee ese volumen y muestra los resultados en `http://localhost:3000`.

Todos los servicios se conectan a la red privada `app-network`. PostgreSQL y Redis tienen comprobaciones de salud; Flask espera a que ambos estén listos.

## Requisitos

Docker Desktop y Docker Compose v2. No hace falta instalar Python, Node.js ni PostgreSQL localmente.

## Preparación y ejecución

1. Desde la carpeta raíz del proyecto, crea el archivo local de variables:

   ```bash
   cp .env.example .env
   ```

2. Edita `.env`. Pon tu usuario real de Docker Hub en `DOCKERHUB_USERNAME` y cambia `POSTGRES_PASSWORD` por una contraseña segura. No subas `.env` a GitHub.

3. Valida la configuración:

   ```bash
   docker compose config
   ```

   Si termina sin errores, Compose pudo interpretar el archivo.

4. Construye e inicia los cinco servicios:

   ```bash
   docker compose up --build -d
   ```

5. Comprueba el estado y los registros:

   ```bash
   docker compose ps
   docker compose logs --tail=100
   ```

6. Abre `http://localhost:5001` para comprobar Flask, PostgreSQL y Redis. Abre `http://localhost:3000` para el visualizador Node.js.

## Probar el procesamiento de una tarea

Envía una tarea desde una terminal:

```bash
curl -X POST http://localhost:5001/process \
  -H 'Content-Type: application/json' \
  -d '{"text":"Hola desde Docker"}'
```

La API debe responder con `202` y un mensaje de tarea enviada. Espera un par de segundos y actualiza `http://localhost:3000`: debe aparecer el texto original y el resultado en mayúsculas. También puedes revisar el worker:

```bash
docker compose logs --tail=50 worker
```

## Servicios, puertos, redes y volúmenes

| Servicio | Puerto publicado | Volumen | Propósito |
|---|---|---|---|
| web (Flask) | `5001:5000` | — | API web |
| db (PostgreSQL) | No se publica al host | `postgres_data` | Persistencia de base de datos |
| redis | No se publica al host | `redis_data` | Persistencia de Redis/cola |
| worker (Python) | No se publica al host | `results_data` | Escribe resultados procesados |
| visualizer (Node.js) | `3000:3000` | `results_data` en solo lectura | Visualiza resultados |

La red `app-network` permite la comunicación por nombre de servicio (`db`, `redis`). PostgreSQL y Redis no necesitan puertos publicados al host para que los otros contenedores los alcancen.

## Publicar imágenes personalizadas en Docker Hub

Tras iniciar sesión en Docker Hub y configurar `.env`, ejecuta:

```bash
chmod +x scripts/publish-dockerhub.sh
./scripts/publish-dockerhub.sh
```

Publica tres imágenes propias: `proyecto-docker-web`, `proyecto-docker-worker` y `proyecto-docker-visualizer`. PostgreSQL y Redis usan imágenes oficiales. Comprueba en Docker Hub que los repositorios sean públicos y tengan la etiqueta `latest` (o la etiqueta configurada).

## Publicar el código en GitHub

Si esta carpeta ya es el clon del repositorio `https://github.com/morty57/proyecto-docker.git`, revisa el estado antes de publicar:

```bash
git status
git remote -v
git add .
git commit -m "Completa arquitectura multicontenedor con Redis y Node.js"
git push origin main
```

Si `git push` informa `non-fast-forward`, **no uses `git push --force`**. Primero ejecuta `git fetch origin`, `git status` y `git log --oneline --graph --decorate -10`; integra los cambios remotos con cuidado antes de volver a publicar.

Si esta carpeta NO es un clon del repositorio existente, no ejecutes `git init` ni cambies el remoto a ciegas: confirma primero el estado de la carpeta y el remoto para evitar sobrescribir o duplicar historial.

## Comandos de demostración y limpieza

```bash
docker compose ps
docker compose logs --tail=100
docker compose down
```

`docker compose down` detiene y elimina los contenedores, pero conserva los volúmenes nombrados. **No uses `docker compose down -v` si necesitas conservar los datos**, porque elimina los volúmenes.

## Capturas y video de entrega

En el video demuestra, en este orden:

1. `docker compose config` sin errores.
2. `docker compose up --build -d` y `docker compose ps` con los cinco servicios activos.
3. `http://localhost:5001`, mostrando la conexión con PostgreSQL y Redis.
4. Una petición `POST /process` con `curl`.
5. `http://localhost:3000` mostrando el resultado procesado.
6. Los repositorios públicos de Docker Hub con las imágenes personalizadas y el repositorio público de GitHub con el código.

No muestres contraseñas, tokens ni otros secretos en la grabación.
