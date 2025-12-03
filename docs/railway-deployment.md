# Railway + Vercel Deployment

## Backend (Railway)

### Setup

1. Create project in Railway, connect GitHub repo
2. Add PostgreSQL: **+ New** → **Database** → **PostgreSQL**
3. Add Volume: **+ New** → **Volume** → mount at `/app/mediafiles`
4. Set environment variables (see below)
5. Enable public networking: **Settings** → **Networking** → **Public Networking**

### Environment Variables

| Variable | Value |
|----------|-------|
| `DJANGO_SECRET_KEY` | `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `MEDIA_ROOT` | `/app/mediafiles` |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-frontend.vercel.app,https://*.railway.app` |

Auto-set by Railway: `DATABASE_URL`

### Key Files

- `config/settings/railway.py` - Railway-specific settings (whitenoise, local cache, no AWS)
- `requirements/railway.txt` - Dependencies without AWS packages
- `start.sh` - Startup script (seeds media to volume, runs migrations, starts gunicorn)
- `nixpacks.toml` - Points to `start.sh`
- `Procfile` - Fallback start command

### Debug Endpoint

`/debug-media/` - Shows MEDIA_ROOT contents and file counts

---

## Frontend (Vercel)

### Setup

1. Import GitHub repo in Vercel
2. Framework: **Next.js** (auto-detected)
3. Set environment variables (see below)
4. Deploy

### Environment Variables

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_BACKEND_HOST` | `https://your-backend.up.railway.app` |
| `NEXTAUTH_URL` | `https://your-frontend.vercel.app` |
| `SECRET` | Any random string |

### Custom Domain

1. Vercel: **Settings** → **Domains** → Add `your.domain.com`
2. DNS: Add CNAME record `your` → `cname.vercel-dns.com`
3. Update `NEXTAUTH_URL` to match

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐
│  Vercel         │────▶│  Railway         │
│  (Next.js)      │     │  (Django)        │
└─────────────────┘     └────────┬─────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
               PostgreSQL    Volume       Whitenoise
               (database)   (media)      (static)
```

| Component | Solution |
|-----------|----------|
| Static files | Whitenoise (served from container) |
| Media files | Railway Volume at `/app/mediafiles` |
| Database | Railway PostgreSQL |
| Cache | Local memory |
| Email | Console backend (logs) |
