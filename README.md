# Shahzad Mobile & Electronics

A bilingual (English / Arabic) e-commerce and device-repair platform built as a clean rebuild of the legacy Next.js storefront. Django REST API + Angular SPA, deployed as a self-contained Docker Compose stack.

## Stack

| Layer       | Tech                                                          |
| ----------- | ------------------------------------------------------------- |
| Backend     | Django 5.1 · DRF 3.15 · SimpleJWT · django-unfold admin       |
| Frontend    | Angular 18 · Tailwind CSS · ngx-translate (EN / AR with RTL)  |
| Database    | PostgreSQL 16                                                 |
| Storage     | AWS S3 (product images) via django-storages, local FS in dev  |
| Auth        | JWT + Google OAuth (ID-token verified server-side)            |
| Payments    | Cash on Delivery · Tamara · Tabby (UAE BNPL)                  |
| Deployment  | Docker Compose · gunicorn · nginx · WhiteNoise                |

## Features

- **Storefront:** product catalogue with category / brand / search, product detail with images, color variants, reviews and Q&A, cart with guest→user merge, wishlist, checkout, order tracking.
- **Repair bookings:** browse repair services, book with device + issue details, track booking status.
- **Admin (django-unfold):** dashboard with KPIs (orders today, 30-day revenue, low stock, open repair bookings), product import/export (CSV/XLSX/JSON), bulk actions, banner management.
- **i18n:** full English / Arabic translations with automatic RTL layout switching.
- **Payments:** pluggable adapter pattern for COD / Tamara / Tabby; Stripe-shape `line_items` kept for provider compatibility.

## Project layout

```
backend/                Django project (config + apps/)
  apps/                 accounts · catalog · cart · orders · payments · repairs · wishlist · marketing · core
  config/settings/      base · dev · prod
frontend/               Angular 18 SPA
  src/app/features/     catalog · cart · checkout · account · orders · repairs · wishlist · pages
docker-compose.yml      db + backend + frontend (nginx)
backend/DEPLOY.md       Production deploy guide
ADMIN_GUIDE.md          Admin panel walkthrough
```

## Local development

```bash
# 1. Backend
cd backend
python -m venv venv
source venv/bin/activate            # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env          # then fill in secrets
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

```bash
# 2. Frontend (in a second terminal)
cd frontend
npm install
npm start                           # http://localhost:4200
```

- API: <http://localhost:8000/api/v1/>
- Admin: <http://localhost:8000/admin/>

## Code quality

```bash
# in backend/, with venv activated
pip install -r requirements-dev.txt
pre-commit install                  # one-time — installs the git hook
```

After `pre-commit install`, every `git commit` auto-runs ruff (lint + format) on staged files.
Manual checks: `ruff check backend/` and `ruff format backend/`.

## Production

See [backend/DEPLOY.md](backend/DEPLOY.md) for the full Docker Compose deploy walkthrough (HTTPS via Let's Encrypt, backups, runbook checklist).

## Status

Active rebuild of the previous Next.js + Prisma storefront. See [backend/REBUILD_PLAN.md](backend/REBUILD_PLAN.md) for the porting plan and design rationale.
