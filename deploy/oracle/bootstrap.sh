#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/jsemsas"
REPO="https://github.com/absgmb/Jsemsas_apps.git"

sudo apt-get update
sudo apt-get install -y ca-certificates curl git nginx

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER" || true
fi
sudo systemctl enable --now docker

sudo mkdir -p "$APP_DIR"
sudo chown -R "$USER":"$USER" "$APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
  git clone "$REPO" "$APP_DIR"
else
  git -C "$APP_DIR" fetch origin
  git -C "$APP_DIR" reset --hard origin/main
fi

cd "$APP_DIR"
if [ ! -f .env ]; then
  cp .env.oracle.example .env
  echo "Created $APP_DIR/.env. Edit it with strong secrets before starting the stack."
  exit 0
fi

docker compose -f docker-compose.oracle.yml up -d --build
docker compose -f docker-compose.oracle.yml exec -T web python manage.py migrate --noinput
docker compose -f docker-compose.oracle.yml exec -T web python manage.py collectstatic --noinput

echo "J-SEMSAS stack is running. Configure Nginx/TLS and open TCP 80/443 in the OCI security list." 
