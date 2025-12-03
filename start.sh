#!/bin/bash
set -e

echo "=== Starting deployment ==="
echo "Current directory: $(pwd)"
echo "Listing teleband/media:"
ls -la teleband/media/ || echo "teleband/media not found"

echo "=== Copying media files to volume ==="
mkdir -p /app/mediafiles
cp -rv teleband/media/* /app/mediafiles/ || echo "Copy failed or no files"

echo "=== Media files in volume ==="
ls -la /app/mediafiles/ || echo "Volume empty"

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Starting gunicorn ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
