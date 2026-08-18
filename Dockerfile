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

# Build static assets only. Database migrations run at container startup.
RUN python manage.py collectstatic --noinput

# PandaStack defaults to PORT=8080 and injects PORT at runtime.
EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 1 --threads 2 --timeout 120 --access-logfile - --error-logfile -"]
