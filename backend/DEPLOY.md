# Deployment guide — Shahzad Arshad Electronics

The whole stack runs in three Docker containers: **Postgres**, **Django/gunicorn**, **nginx**. One command brings everything up.

---

## What you need on the server

- A Linux VPS (Ubuntu 22.04+ recommended) — Hetzner, DigitalOcean, Linode, or any cloud
- A domain pointed at the server (e.g. `shahzadmobile.com` → server IP via A record)
- Docker + Docker Compose v2:
  ```bash
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER && newgrp docker
  ```

---

## First-time deploy

```bash
# 1. Clone the project to the server
git clone <your-repo-url> /opt/shahzadmobile && cd /opt/shahzadmobile

# 2. Create the production env file
cp .env.prod.example .env.prod
nano .env.prod        # fill in SECRET_KEY, POSTGRES_PASSWORD, EMAIL_*, S3 keys, payment keys

# 3. Build + start everything
docker compose --env-file .env.prod up -d --build

# 4. Watch logs to confirm migrations + collectstatic ran cleanly
docker compose logs -f web

# 5. Create your admin user
docker compose exec web python manage.py createsuperuser

# 6. (Optional first deploy only) seed catalog + repair services
docker compose exec -e SEED_DEMO=1 web python manage.py seed_demo
docker compose exec web python manage.py seed_repairs
```

The site is now reachable on **port 80**. Visit `http://your-server-ip/` to confirm.

---

## HTTPS with Let's Encrypt (do this next)

The simplest route is `certbot` running on the host:

```bash
sudo apt install certbot
sudo certbot certonly --webroot -w /opt/shahzadmobile/certbot \
    -d shahzadmobile.com -d www.shahzadmobile.com \
    --email sa@shahzadmobile.com --agree-tos -n
```

Then copy the certs into `deploy/certs/` (or symlink), uncomment the HTTPS server block in `deploy/nginx.conf`, and:
```bash
docker compose restart nginx
```
Set up auto-renewal:
```bash
echo "0 3 * * * certbot renew --quiet && docker compose -f /opt/shahzadmobile/docker-compose.yml restart nginx" | sudo crontab -
```

---

## Day-2 operations

| Task | Command |
|---|---|
| Pull a new release | `git pull && docker compose --env-file .env.prod up -d --build` |
| Run a one-off command | `docker compose exec web python manage.py <command>` |
| Open a Django shell | `docker compose exec web python manage.py shell` |
| Tail logs | `docker compose logs -f web` or `nginx` or `db` |
| Backup the DB | `docker compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > backup-$(date +%F).sql.gz` |
| Restore | `gunzip -c backup.sql.gz \| docker compose exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB` |
| Stop everything | `docker compose down` |
| Stop AND wipe DB | `docker compose down -v` (⚠ deletes Postgres volume) |

---

## Runbook checklist before going live

- [ ] `SECRET_KEY` set to a random 50-char string (`python -c "import secrets;print(secrets.token_urlsafe(50))"`)
- [ ] `DEBUG=0` in `.env.prod`
- [ ] `ALLOWED_HOSTS` lists every domain the site responds on
- [ ] Strong `POSTGRES_PASSWORD`
- [ ] SMTP credentials work — order confirmation arrives at a real inbox
- [ ] Tamara + Tabby production keys (not sandbox) entered, **success/cancel URLs** point at `https://shahzadmobile.com/...`
- [ ] AWS S3 keys have `s3:GetObject + s3:PutObject` on the bucket
- [ ] HTTPS server block in `nginx.conf` enabled
- [ ] First admin user created
- [ ] Visited `/admin/` and confirmed login works
- [ ] Placed a real order end-to-end (COD) and received the email
- [ ] WhatsApp button + Tawk.to chat both load on the homepage
- [ ] Atlas / MongoDB import (if needed) ran via `python manage.py import_from_mongo`

---

## Architecture (compose services)

```
                                 ┌─────────────────┐
                          80/443 │     nginx       │  → static + media + proxy
                                 │ (deploy/nginx)  │
                                 └────────┬────────┘
                                          │ proxy_pass http://web:8000
                                 ┌────────▼────────┐
                                 │      web        │  Django + gunicorn (3 workers)
                                 │   (Dockerfile)  │
                                 └────────┬────────┘
                                          │ DATABASE_URL
                                 ┌────────▼────────┐
                                 │       db        │  Postgres 16
                                 │ (postgres-data) │
                                 └─────────────────┘
```

---

## Troubleshooting

- **"Bad Gateway" on /** — `web` container failed to start. `docker compose logs web` will show a Django stack trace (usually a missing env var or a migration error).
- **Static files not loading** — `collectstatic` didn't run, or nginx volume isn't mounted. Re-run `docker compose up -d --build`.
- **`ALLOWED_HOSTS` error** — add your domain (and `www.` variant) to `.env.prod` and restart.
- **DB connection refused** — check `POSTGRES_PASSWORD` is identical in `.env.prod` and the auto-built `DATABASE_URL`. The entrypoint waits up to 60 s for the DB.
- **Mongo import fails** — see the IP allowlist guidance in the project chat. Use a VPN or temporarily allow `0.0.0.0/0` in Atlas Network Access.
