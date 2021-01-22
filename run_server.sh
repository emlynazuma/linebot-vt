#! /bin/bash

set -e

if [[ ! -f /var/log/gunicorn ]]; then
    mkdir -p /var/log/gunicorn
fi

gunicorn_config='gunicorn_config.py'
if [ "$1" == "dev" ]; then
    gunicorn_config='gunicorn_config_dev.py'
fi

gunicorn \
    --config "/app/src/${gunicorn_config}" \
    linebot_app:app

exec "$@"
