# J-SEMSAS Render Deployment

The repository contains a Render Blueprint at `render.yaml` that provisions:

- `jsemsas-api` — Django/DRF API
- `jsemsas-postgres` — PostgreSQL 17 with PostGIS support
- `jsemsas-redis` — Render Key Value (Redis-compatible) broker/cache
- `jsemsas-celery-worker` — Celery worker
- `jsemsas-celery-beat` — periodic Celery scheduler

Render supports PostGIS as a PostgreSQL extension. The web service enables it automatically before migrations.

## Deploy

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint**.
3. Connect `absgmb/Jsemsas_apps` and select `main`.
4. Render reads `render.yaml` and creates the services/databases.
5. Enter the four secret/sensitive values requested by the Blueprint:
   - `DJANGO_SECRET_KEY`
   - `QR_SIGNING_KEY`
   - `GOOGLE_SERVICE_ACCOUNT_JSON` (only if NHIA Google Sheets sync is used)
   - `GOOGLE_SHEETS_ID` (only if NHIA Google Sheets sync is used)
6. Wait for the PostgreSQL database to become available and the API deploy to finish.
7. Verify `/healthz/` returns `{"status":"ok","database":"ok"}`.
8. Create the first admin account from a Render shell/one-off command:

```bash
python manage.py createsuperuser
```

## Production environment variables

The Blueprint supplies the database and Redis URLs automatically. Never commit real secrets to GitHub.

Required:

```text
DJANGO_SECRET_KEY=<long-random-secret>
QR_SIGNING_KEY=<separate-long-random-secret>
DATABASE_URL=<provided by Render>
REDIS_URL=<provided by Render>
DEBUG=False
SECURE_SSL_REDIRECT=True
ALLOWED_HOSTS=.onrender.com
```

Optional NHIA sync:

```text
GOOGLE_SHEETS_ID=<sheet-id>
GOOGLE_SHEETS_RANGE=Tariffs!A:E
GOOGLE_SERVICE_ACCOUNT_JSON=<service-account-json>
```

## PostGIS

Render Postgres supports PostGIS. The deployment pre-command runs:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

before Django migrations.

## Health checking

Render uses:

```text
GET /healthz/
```

The endpoint checks database connectivity and returns HTTP 503 if PostgreSQL is unavailable.

## Celery

The worker executes asynchronous jobs:

```bash
celery -A config worker --loglevel=INFO --concurrency=2
```

Celery Beat executes the configured NHIA tariff synchronization every six hours:

```bash
celery -A config beat --loglevel=INFO
```

## Important file-storage note

Render services have an ephemeral filesystem. Uploaded ETC evidence and generated PDFs must eventually be moved to durable object storage (S3-compatible storage or another managed object store) before production use. Do not rely on `MEDIA_ROOT` for permanent records.

## Migration note

The current repository originally contained migration package stubs. The Docker build generates the initial migrations into the image so the first deployment can initialize the database. Once the initial deployment is validated, commit the generated migration files to Git and stop generating migrations during Docker builds. Future schema changes should always be created and reviewed as normal Django migration commits.
