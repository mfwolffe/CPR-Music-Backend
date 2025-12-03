#!/bin/bash
set -e

echo "=== Starting deployment ==="

# Copy media files to volume if source exists and volume is empty
# (Only needed on first deploy or if volume is recreated)
if [ -d "teleband/media" ] && [ ! -f "/app/mediafiles/.seeded" ]; then
    echo "=== Seeding media files to volume ==="
    mkdir -p /app/mediafiles
    cp -rv teleband/media/* /app/mediafiles/ || echo "Copy failed"
    touch /app/mediafiles/.seeded
    echo "=== Media files seeded ==="
fi

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Starting gunicorn ==="
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
