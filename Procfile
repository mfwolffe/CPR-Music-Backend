web: export DJANGO_SETTINGS_MODULE=config.settings.railway && python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
