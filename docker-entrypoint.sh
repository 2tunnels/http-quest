#!/usr/bin/env bash

set -e

if [ "$1" = "gunicorn" ]; then
	exec gunicorn http_quest.asgi:application \
	  --worker-class uvicorn.workers.UvicornWorker \
	  --bind 0.0.0.0:8000 \
	  --access-logfile "-" \
	  --error-logfile "-" \
	  --forwarded-allow-ips "*"
fi

exec "$@"
