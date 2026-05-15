#!/bin/bash

set -e

IMAGE_NAME=$1
DEPLOY_REF=$2

HOST_PORT=8181
CONTAINER_PORT=8181

CONTAINER_NAME="catty-reminders-app"

IMAGE="$IMAGE_NAME:$DEPLOY_REF"

echo "=== DEPLOY RELEASE ==="
echo "IMAGE_NAME=$IMAGE_NAME"
echo "DEPLOY_REF=$DEPLOY_REF"

echo "=== Pull image ==="
sudo docker pull $IMAGE

echo "=== Stop old container ==="
sudo docker stop $CONTAINER_NAME || true

echo "=== Remove old container ==="
sudo docker rm $CONTAINER_NAME || true

echo "=== Start new container ==="

sudo docker run -d \
  -p $HOST_PORT:$CONTAINER_PORT \
  --name $CONTAINER_NAME \
  --restart unless-stopped \
  $IMAGE

