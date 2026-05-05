"""
WSGI config for the Shahzad Mobile project.

Wraps the Django WSGI app with an extra WhiteNoise layer that serves the
Angular SPA bundle (built into `frontend_dist/browser/` by the project's
multi-stage Dockerfile) at the URL root. Requests for `/main-abc.js`,
`/styles-def.css`, `/i18n/en.json`, `/favicon.ico` etc. are served directly
from the bundle. Django's own `/static/` (admin CSS, etc.) is still served
by the in-app WhiteNoiseMiddleware.

If `frontend_dist/` doesn't exist (e.g., local `runserver` without a build),
the wrapping is skipped — the Angular dev server (`npm start`) serves the
frontend separately on port 4200.
"""
import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_wsgi_application()

BASE_DIR = Path(__file__).resolve().parent.parent
SPA_DIR = BASE_DIR / "frontend_dist" / "browser"

if SPA_DIR.exists():
    from whitenoise import WhiteNoise

    application = WhiteNoise(
        application,
        root=str(SPA_DIR),
        prefix="/",
        index_file=True,
    )
