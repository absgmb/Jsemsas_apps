FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# GeoDjango/PostGIS runtime dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgeos-c1v5 \
    libproj25 \
    libgdal32 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Build static assets only. Do not require the runtime database during image build.
RUN python manage.py collectstatic --noinput

# PandaStack injects PORT at runtime; 8080 is its documented default.
EXPOSE 8080

# Start HTTP immediately so the platform can detect readiness. Run database setup
# and optional superuser bootstrap in the background after Gunicorn is listening.
CMD ["sh", "-c", "echo \"Starting J-SEMSAS on 0.0.0.0:${PORT:-8080}\"; gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 2 --timeout 120 --access-logfile - --error-logfile - & GUNICORN_PID=$!; sleep 2; (python manage.py migrate --noinput && python manage.py bootstrap_superuser || echo 'WARNING: database migration/bootstrap failed; web process remains available for health checks') & wait $GUNICORN_PID"]
