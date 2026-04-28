#!/usr/bin/env bash
set -euo pipefail

echo ">>> Waiting for database…"
python - <<'PY'
import os, time
import psycopg
url = os.environ.get("DATABASE_URL", "")
if not url.startswith("postgres"):
    print("DATABASE_URL is not Postgres — skipping wait.")
else:
    for i in range(30):
        try:
            psycopg.connect(url, connect_timeout=3).close()
            print("DB is up.")
            break
        except Exception as e:
            print(f"  attempt {i+1}/30: {e}")
            time.sleep(2)
    else:
        raise SystemExit("DB did not become reachable within 60s")
PY

echo ">>> Running migrations…"
python manage.py migrate --noinput

echo ">>> Collecting static files…"
python manage.py collectstatic --noinput

if [[ "${SEED_DEMO:-0}" == "1" ]]; then
    echo ">>> Seeding demo data…"
    python manage.py seed_demo || true
    python manage.py seed_repairs || true
fi

echo ">>> Starting: $*"
exec "$@"
