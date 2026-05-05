# Deployment guide — Shahzad Mobile

The whole stack runs as **one Docker image** (Django + Angular SPA bundled by the multi-stage `Dockerfile` at the repo root) plus **one Postgres instance**. Pick whichever host fits — VPS, Fly.io, Railway, or Render. The image is the same.

---

## Architecture

```
   shahzadmobile.com  ───►  ┌─────────────────────┐  ───►  Postgres (managed
                            │   web container     │         or in-stack)
                            │                     │
                            │  /api/v1/  → DRF    │
                            │  /admin/   → admin  │
                            │  /*        → SPA    │
                            │                     │
                            │  gunicorn + 3 workers
                            │  WhiteNoise serves SPA + /static
                            └─────────────────────┘
```

One container, one process tree, no separate frontend service.

---

## Path A — VPS (Hetzner / DigitalOcean / Hostinger)

### What you need

- A Linux VPS (Ubuntu 22.04+) — Hetzner CX22 (~€4/month) is plenty
- A domain pointed at the server
- Docker + Docker Compose v2:
  ```bash
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER && newgrp docker
  ```

### First-time deploy

```bash
# 1. Clone the project to the server
git clone <your-repo-url> /opt/shahzadmobile && cd /opt/shahzadmobile

# 2. Create the production env file
cp .env.prod.example backend/.env.prod
nano backend/.env.prod        # fill in SECRET_KEY, POSTGRES_PASSWORD, EMAIL_*, payment keys, etc.

# 3. Build + start everything
docker compose --env-file backend/.env.prod up -d --build

# 4. Watch logs to confirm migrations + collectstatic ran cleanly
docker compose logs -f web

# 5. Create your admin user
docker compose exec web python manage.py createsuperuser

# 6. (Optional) seed catalog + repair services + demo orders
docker compose exec web python manage.py seed_all
```

The site is reachable on **port 80**. Visit `http://your-server-ip/` and you should see the Angular SPA. `/admin/` shows the Django admin. `/api/v1/catalog/products/` returns JSON.

### HTTPS

The compose stack listens on plain HTTP. For HTTPS, the simplest path is to put **Cloudflare** in front of the VPS (free, automatic TLS, fast in MENA). Alternatively run **Caddy** on the host:

```bash
sudo apt install caddy
sudo nano /etc/caddy/Caddyfile
```

```
shahzadmobile.com, www.shahzadmobile.com {
    reverse_proxy localhost:80
}
```

```bash
sudo systemctl restart caddy
```

Caddy auto-issues Let's Encrypt certs and renews them.

### Day-2 ops

| Task | Command |
|---|---|
| Pull a new release | `git pull && docker compose --env-file backend/.env.prod up -d --build` |
| Run a one-off command | `docker compose exec web python manage.py <command>` |
| Django shell | `docker compose exec web python manage.py shell` |
| Tail logs | `docker compose logs -f web` or `db` |
| Backup the DB | `docker compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB \| gzip > backup-$(date +%F).sql.gz` |
| Restore | `gunzip -c backup.sql.gz \| docker compose exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB` |
| Stop everything | `docker compose down` |
| Stop AND wipe DB | `docker compose down -v` (⚠ deletes Postgres volume) |

---

## Path B — Fly.io

Fly auto-detects the `Dockerfile` at the repo root.

```bash
# install flyctl
curl -L https://fly.io/install.sh | sh

# from repo root
fly launch                    # creates fly.toml, asks region (pick fra/cdg for MENA-friendly)
fly postgres create           # provisions managed Postgres, attaches DATABASE_URL automatically
fly secrets set SECRET_KEY=$(python -c "import secrets;print(secrets.token_urlsafe(50))") \
                ALLOWED_HOSTS=shahzadmobile.com,www.shahzadmobile.com \
                EMAIL_HOST=smtp.resend.com EMAIL_HOST_PASSWORD=re_yourkey \
                # ... rest of env vars per .env.prod.example

fly deploy
```

Fly handles HTTPS automatically. Map your domain with `fly certs add shahzadmobile.com`.

---

## Path C — Railway

Railway auto-detects the `Dockerfile`. Add a Postgres plugin from the dashboard — Railway sets `DATABASE_URL` for you.

1. Sign up at <https://railway.app>, connect your GitHub repo
2. New Project → Deploy from GitHub Repo → pick `Shahzad-Website`
3. Add a Postgres plugin (one click)
4. **Variables** → paste the rest of `.env.prod.example` values (skip `DATABASE_URL` — auto-set)
5. Railway builds the Dockerfile, deploys, gives you `*.up.railway.app` URL
6. Add custom domain `shahzadmobile.com` in **Settings → Networking**

Every push to `main` auto-deploys.

---

## Path D — Render

Same idea: dashboard creates a "Web Service" from your GitHub repo, picks up the Dockerfile.

1. Sign up at <https://render.com>, connect GitHub
2. **New → Web Service** → pick the repo, build using "Dockerfile"
3. **New → PostgreSQL** (free tier or paid). Copy the internal `DATABASE_URL`.
4. Back on the Web Service, add env vars (paste from `.env.prod.example` + the `DATABASE_URL` from step 3)
5. Deploy. Render provides `*.onrender.com` URL + auto-HTTPS.
6. Add custom domain in Render dashboard.

Every push to `main` auto-deploys.

---

## Runbook checklist before going live

- [ ] `SECRET_KEY` set to a random 50-char string (`python -c "import secrets;print(secrets.token_urlsafe(50))"`)
- [ ] `DEBUG=0`
- [ ] `ALLOWED_HOSTS` lists every domain (e.g. `shahzadmobile.com,www.shahzadmobile.com`)
- [ ] Strong `POSTGRES_PASSWORD` (or managed Postgres credentials, depending on host)
- [ ] Resend account created, API key set as `EMAIL_HOST_PASSWORD=re_...`
- [ ] SPF + DKIM + DMARC DNS records added on `shahzadmobile.com` per Resend's setup wizard
- [ ] Email pipeline verified: `python manage.py send_test_email you@example.com` lands in your inbox (not spam)
- [ ] Tamara prod API key set (`TAMARA_API_KEY` and `TAMARA_NOTIFICATION_TOKEN`)
- [ ] Tamara dashboard → success/cancel/notification URLs all point at `https://shahzadmobile.com/...`
- [ ] Tabby UAE + KSA secret keys set (`TABBY_SECRET_KEY_UAE`, `TABBY_SECRET_KEY_KSA`)
- [ ] Tabby webhook secret set (`TABBY_WEBHOOK_SECRET`) and matches the value configured in Tabby's dashboard
- [ ] AWS S3 keys (if `USE_S3=1`) have `s3:GetObject + s3:PutObject` on the bucket
- [ ] First admin user created (`createsuperuser`)
- [ ] `/admin/` login works
- [ ] Placed a real test order (COD) and received the confirmation email
- [ ] Placed a real test order (Tamara, 1 AED) and the redirect to Tamara checkout works
- [ ] Google OAuth Client ID set in `frontend/src/environments/environment.prod.ts`; production domain added to "Authorized JavaScript origins" at <https://console.cloud.google.com/apis/credentials>
- [ ] Tawk.to `propertyId` / `widgetId` set in `environment.prod.ts` (or left empty to disable)
- [ ] WhatsApp number set in `environment.prod.ts`
- [ ] Frontend rebuilt with the new env values (the Dockerfile does this automatically on every build)

---

## Troubleshooting

- **"Bad Gateway" / "Application Error" on `/`** — the `web` container failed to start. Check logs (`docker compose logs web`, `fly logs`, Render/Railway logs). Most often a missing required env var or a migration failure.
- **Frontend shows a 404 / blank page** — the SPA bundle didn't get into the container. Rebuild from scratch (`docker compose build --no-cache web`).
- **Static files not loading** — `collectstatic` didn't run; check the entrypoint log line. WhiteNoise serves them; no separate volume is required for cloud hosts (only for VPS).
- **`ALLOWED_HOSTS` error** — add your domain (and `www.` variant) to env, restart.
- **DB connection refused** — check `DATABASE_URL`. On VPS the entrypoint waits up to 60s for the DB. On managed hosts the DATABASE_URL is auto-set.
- **Tamara / Tabby errors at checkout** — check `runserver`/container logs. With `DEBUG=True` the upstream provider error reaches the browser response. With `DEBUG=False` the customer sees a generic "currently unavailable" message and the upstream error is in the container log.
