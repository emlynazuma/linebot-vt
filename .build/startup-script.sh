#!/usr/bin/env bash

ENV='testing'
APP_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/app-name -H "Metadata-Flavor: Google")
PROJECT_ID=$(curl http://metadata.google.internal/computeMetadata/v1/project/project-id -H "Metadata-Flavor: Google")
GCP_STORAGE='vt-t'
CONFIG_FILE='/etc/stackdriver/logging.config.d/fluentd-lakitu.conf'
CUSTOM_CONFIG_FILE="/etc/stackdriver/logging.config.d/vt.conf"
CUSTOM_CONFIG_FILE_SRC="https://storage.googleapis.com/${GCP_STORAGE}/fluentd-${APP_NAME}.conf?ts=$(date +"%m%d%Y%H%M%S")"

if [ 'lithe-window-713' = "$PROJECT_ID" ]; then
  ENV='production'
  GCP_STORAGE='vt-s'
fi


curl -so $CUSTOM_CONFIG_FILE "$CUSTOM_CONFIG_FILE_SRC"

sed -i $'s/container_id \${tag_parts\[5\]}/container_id \${tag_parts\[5\]}\\n    appName '"${APP_NAME}"'/g' $CONFIG_FILE
sed -i 's/APPNAME_SLOT/'"${APP_NAME}"'/g' $CUSTOM_CONFIG_FILE
sed -i 's/PROJECT_ID_SLOT/'"${PROJECT_ID}"'/g' $CUSTOM_CONFIG_FILE

if docker ps | grep "[s]tackdriver-logging-agent"; then
  systemctl restart stackdriver-logging.service
fi
