from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INTERNAL_IPS = ["127.0.0.1"]

# Allow any devtunnels.ms host in local development so paired frontend/backend
# tunnels can talk to each other without weakening production CORS.
CORS_ALLOWED_ORIGIN_REGEXES += [
    r"^https://[a-z0-9-]+\.devtunnels\.ms$",
    r"^https://[a-z0-9-]+\-\d+\.inc1\.devtunnels\.ms$",
]
CSRF_TRUSTED_ORIGINS += [
    "https://*.devtunnels.ms",
    "https://*.inc1.devtunnels.ms",
]
