# J-SEMSAS

Jigawa State Emergency Medical Services and Ambulance Scheme Claims & Dispatch Management System.

Backend foundation: Django 5.x, Django REST Framework, PostgreSQL/PostGIS, Celery, Redis, JWT authentication, RBAC, HMAC-signed QR verification, GPS validation, and NHIA tariff synchronization.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Run migrations and create an admin user:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

API root: `/api/`
JWT token endpoint: `/api/auth/token/`
QR verification: `/verify/claim/?token=...`

## Production roadmap

Add Flutter Driver and Nurse apps, Django Channels/FCM push delivery, immutable audit events, PDF reporting, object storage, device attestation, comprehensive automated tests, and production observability before government deployment.
