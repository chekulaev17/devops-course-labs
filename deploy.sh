#!/bin/bash

set -e

IMAGE_NAME=$1
DEPLOY_REF=$2

echo "=== DEPLOY RELEASE ==="
echo "DEPLOY_REF=$DEPLOY_REF"

sudo docker pull $IMAGE_NAME:$DEPLOY_REF

sudo docker stop catty-reminders-app || true
sudo docker rm catty-reminders-app || true

sudo docker run -d \
  -p 8181:8181 \
  --name catty-reminders-app \
  --restart unless-stopped \
  $IMAGE_NAME:$DEPLOY_REF
