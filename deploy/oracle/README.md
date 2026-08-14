# Oracle Cloud deployment

This deployment targets an Oracle Cloud Infrastructure (OCI) VM, with Docker Compose running Django, PostgreSQL/PostGIS, Redis, Celery worker, and Celery Beat on one VM. This is intended for low-cost development/pilot deployment. For government production, move PostgreSQL to a managed HA service and media to durable object storage.

## 1. Create the VM

Create an OCI Compute VM using an Always Free eligible shape where available (for example an Ampere A1 Flex ARM VM). Use Ubuntu and assign a public IPv4 address. Availability of Always Free capacity depends on your OCI account/region.

Open TCP ports 22, 80, and 443 in the OCI VCN security list/network security group. Do not expose PostgreSQL (5432) or Redis (6379) publicly.

## 2. Bootstrap

SSH into the VM and run:

```bash
curl -fsSL https://raw.githubusercontent.com/absgmb/Jsemsas_apps/main/deploy/oracle/bootstrap.sh -o /tmp/jsemsas-bootstrap.sh
chmod +x /tmp/jsemsas-bootstrap.sh
/tmp/jsemsas-bootstrap.sh
```

Edit `/opt/jsemsas/.env`, replacing every `CHANGE_ME` value and setting `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

Then:

```bash
cd /opt/jsemsas
docker compose -f docker-compose.oracle.yml up -d --build
docker compose -f docker-compose.oracle.yml exec web python manage.py migrate --noinput
docker compose -f docker-compose.oracle.yml exec web python manage.py collectstatic --noinput
```

## 3. Nginx

Copy the included config to `/etc/nginx/sites-available/jsemsas`, change the `alias` paths if needed, enable it, and reload Nginx. For HTTPS, use Certbot/Let's Encrypt after DNS points to the VM.

## 4. Updates

```bash
cd /opt/jsemsas
git pull --ff-only origin main
docker compose -f docker-compose.oracle.yml up -d --build
docker compose -f docker-compose.oracle.yml exec web python manage.py migrate --noinput
docker compose -f docker-compose.oracle.yml exec web python manage.py collectstatic --noinput
```

## 5. Backups

Do not treat a single VM as a government-production backup strategy. Schedule PostgreSQL `pg_dump` backups to durable external storage and test restores. Keep application secrets out of Git.
