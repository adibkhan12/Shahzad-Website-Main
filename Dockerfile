# syntax=docker/dockerfile:1
#
# Single-deployment image: Django backend + bundled Angular SPA.
# Stage 1 builds the Angular production bundle.
# Stage 2 installs Django + copies the SPA bundle into /app/frontend_dist/browser.
# At runtime, gunicorn + WhiteNoise serve the API, the admin, and the SPA from
# one container — no separate frontend service needed.

# ============== Stage 1: build Angular frontend ==============
FROM node:20-alpine AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build -- --configuration=production
# Output: /frontend/dist/frontend/browser/

# ============== Stage 2: Django + bundled Angular SPA ==============
FROM python:3.12-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY backend/ /app/
COPY --from=frontend /frontend/dist/frontend/browser /app/frontend_dist/browser

RUN chmod +x /app/scripts/entrypoint.sh \
    && useradd --system --create-home --uid 1000 app \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app
USER app

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--threads", "2", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--timeout", "60"]
