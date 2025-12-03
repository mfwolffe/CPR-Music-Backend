# Railway Deployment Guide

This guide covers deploying the MusicCPR Django backend to Railway.

## Prerequisites

- Railway account (https://railway.app)
- GitHub repo connected to Railway

## Quick Start

1. **Create a new project in Railway**
   - Connect your GitHub repository
   - Railway will auto-detect the Python/Django project

2. **Add PostgreSQL (optional but recommended)**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

3. **Set Environment Variables**

   In Railway dashboard → Variables, add:

   ```
   DJANGO_SECRET_KEY=your-super-secret-key-here
   DJANGO_SETTINGS_MODULE=config.settings.railway
   DJANGO_ALLOWED_HOSTS=.railway.app,.up.railway.app
   ```

4. **Deploy!**
   Railway will automatically:
   - Install dependencies from `requirements/railway.txt`
   - Run migrations
   - Collect static files
   - Start gunicorn

## Environment Variables Reference

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |

### Auto-set by Railway (when you add Postgres)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_DEBUG` | `False` | Enable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `.railway.app` | Comma-separated allowed hosts |
| `DJANGO_ADMIN_URL` | `admin/` | Admin URL path |
| `CORS_ALLOWED_ORIGINS` | (empty) | Comma-separated allowed origins for CORS |
| `CSRF_TRUSTED_ORIGINS` | `https://*.railway.app` | Trusted origins for CSRF |

## Connecting to Vercel Frontend

1. Deploy your Next.js frontend to Vercel
2. Get your Railway backend URL (e.g., `https://your-app.up.railway.app`)
3. In Vercel, set environment variable:
   ```
   NEXT_PUBLIC_BACKEND_HOST=https://your-app.up.railway.app
   ```
4. In Railway, add the Vercel URL to CORS:
   ```
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   CSRF_TRUSTED_ORIGINS=https://your-app.vercel.app,https://*.railway.app
   ```

## Media Files

For short-term testing, media files are stored locally in `/mediafiles`.

**Important**: Railway's filesystem is ephemeral by default. For persistent media storage:
1. Add a Railway Volume (Settings → Volumes)
2. Mount it at `/app/mediafiles`
3. Set `MEDIA_ROOT=/app/mediafiles`

## Troubleshooting

### Static files not loading
- Check that `collectstatic` ran in the deploy logs
- Verify `whitenoise` is in requirements

### Database connection errors
- Make sure you added PostgreSQL to your Railway project
- Check `DATABASE_URL` is set in variables

### CORS errors
- Add your frontend URL to `CORS_ALLOWED_ORIGINS`
- Make sure `CSRF_TRUSTED_ORIGINS` includes your domains

## Local Testing with Railway Settings

```bash
cd CPR-Music-Backend
pip install -r requirements/railway.txt

# Set minimal env vars
export DJANGO_SECRET_KEY="test-secret-key-for-local-dev"
export DJANGO_DEBUG=True
export DJANGO_SETTINGS_MODULE=config.settings.railway

# Run migrations and server
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```
