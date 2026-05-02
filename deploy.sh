#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/chekulaev17/catty-reminders-app"
ENV_FILE="$APP_DIR/.env.deploy"

cd "$APP_DIR"

git pull

if [ ! -d venv ]; then
  python3 -m venv venv
fi

venv/bin/pip install -r requirements.txt

DEPLOY_REF="$(git rev-parse HEAD)"
echo "DEPLOY_REF=$DEPLOY_REF" > "$ENV_FILE"

sudo systemctl restart catty-app.service
