from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    EMAIL_USE_TLS=(bool, True),
    DB_PORT=(int, 5432),
)
env_file = BASE_DIR / ".env"
if not env_file.exists():
    env_file = BASE_DIR.parent / ".env"
environ.Env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY", default="insecure-dev-key-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", ".devtunnels.ms"],
)
SITE_URL = env("SITE_URL", default="http://localhost:8000")
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:4200")
SITE_ID = 1

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    # third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "storages",
    # local
    "apps.core",
    "apps.accounts",
    "apps.catalog",
    "apps.cart",
    "apps.orders",
    "apps.payments",
    "apps.wishlist",
    "apps.marketing",
    "apps.repairs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="shahzad_ecommerce"),
        "USER": env("DB_USER", default="postgres"),
        "PASSWORD": env("DB_PASSWORD", default="adib"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT"),
    }
}

AUTH_USER_MODEL = "accounts.User"

# bcrypt-first so imported bcryptjs hashes from the old Next.js app still verify
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dubai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

USE_S3 = env("USE_S3")
if USE_S3:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="eu-north-1")
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    STORAGES["default"] = {"BACKEND": "storages.backends.s3.S3Storage"}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@example.com")

from decimal import Decimal as _D  # noqa: E402

# Payments
CURRENCY = env("CURRENCY", default="AED")

# Tamara — same API base for sandbox or prod (you switch via TAMARA_BASE_URL),
# but the API KEY is environment-specific. Per-region UAE/KSA keys are
# checked first; if absent, falls back to the legacy TAMARA_API_KEY.
TAMARA_BASE_URL = env("TAMARA_BASE_URL", default="")
TAMARA_API_KEY = env("TAMARA_API_KEY", default="")
TAMARA_API_KEY_UAE = env("TAMARA_API_KEY_UAE", default="")
TAMARA_API_KEY_KSA = env("TAMARA_API_KEY_KSA", default="")
# Issued separately by Tamara at webhook registration (the "Notification Token").
# Used to verify the HS256-signed JWT they send on webhook auth.
TAMARA_NOTIFICATION_TOKEN = env("TAMARA_NOTIFICATION_TOKEN", default="")

# Tabby — DIFFERENT API base for KSA (api.tabby.sa) vs UAE (api.tabby.ai),
# and different keys per region. Falls back to the legacy TABBY_* if a
# region-specific value is missing.
TABBY_API_URL = env("TABBY_API_URL", default="")
TABBY_SECRET_KEY = env("TABBY_SECRET_KEY", default="")
TABBY_API_URL_UAE = env("TABBY_API_URL_UAE", default="https://api.tabby.ai")
TABBY_SECRET_KEY_UAE = env("TABBY_SECRET_KEY_UAE", default="")
TABBY_API_URL_KSA = env("TABBY_API_URL_KSA", default="https://api.tabby.sa")
TABBY_SECRET_KEY_KSA = env("TABBY_SECRET_KEY_KSA", default="")
# Shared secret you set when registering the Tabby webhook; sent back as the
# value of the X-Webhook-Auth header on every webhook delivery.
TABBY_WEBHOOK_SECRET = env("TABBY_WEBHOOK_SECRET", default="")

# Region-specific shipping. Currency stays AED for both for now.
SHIPPING = {
    "UAE": {
        "fee": _D("30"),
        "days": "1-3",
        "label": "Same-day in Sharjah, next-day UAE-wide",
    },
    "KSA": {
        "fee": _D("150"),
        "days": "15-20",
        "label": "International shipping to Mecca, Madina, or Jeddah",
    },
}

# KSA delivery is currently limited to these three cities only.
KSA_ALLOWED_CITIES = ["Mecca", "Madina", "Jeddah"]

# BNPL service fee added to subtotal when paying via Tamara or Tabby.
# Calculated on subtotal (products) only — shipping is excluded.
BNPL_SURCHARGE_PCT = _D("9")

# Google OAuth (ID-token based; Angular sends ID token, backend verifies & issues JWT)
GOOGLE_OAUTH_CLIENT_ID = env("GOOGLE_OAUTH_CLIENT_ID", default="")
GOOGLE_OAUTH_CLIENT_SECRET = env("GOOGLE_OAUTH_CLIENT_SECRET", default="")

LEGACY_DATABASE_URL = env("LEGACY_DATABASE_URL", default="")
LEGACY_MONGODB_URI = env("LEGACY_MONGODB_URI", default="")
LEGACY_MONGODB_DB = env("LEGACY_MONGODB_DB", default="")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 24,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:4200", "http://127.0.0.1:4200"],
)
# Allow any devtunnels.ms host so the frontend dev tunnel can talk to the
# backend dev tunnel regardless of the session-specific subdomain.
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://[a-z0-9-]+\.devtunnels\.ms$",
    r"^https://[a-z0-9-]+\-\d+\.inc1\.devtunnels\.ms$",
]
CSRF_TRUSTED_ORIGINS = [
    "https://*.devtunnels.ms",
    "https://*.inc1.devtunnels.ms",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-guest-session",
]

# Surface ERROR-level logs from our `apps.*` modules to the runserver console.
# Without this, calls like logger.error() inside payment providers would be
# silently swallowed by Django's default logging config.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[%(levelname)s] %(name)s — %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

UNFOLD = {
    "SITE_TITLE": "Shahzad Admin",
    "SITE_HEADER": "Shahzad",
    "SITE_SUBHEADER": "Mobile & electronics",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": "apps.core.admin_dashboard.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "243 232 255",
            "100": "233 213 255",
            "200": "216 180 254",
            "300": "192 132 252",
            "400": "168 85 247",
            "500": "147 51 234",
            "600": "116 13 194",
            "700": "88 9 147",
            "800": "59 7 100",
            "900": "42 6 71",
            "950": "28 4 48",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Catalog",
                "separator": True,
                "items": [
                    {"title": "Products", "icon": "inventory_2", "link": "/admin/catalog/product/"},
                    {
                        "title": "+ Add product",
                        "icon": "add",
                        "link": "/admin/catalog/product/add/",
                    },
                    {
                        "title": "Stock movements",
                        "icon": "swap_horiz",
                        "link": "/admin/catalog/stockmovement/",
                    },
                    {"title": "Categories", "icon": "category", "link": "/admin/catalog/category/"},
                    {"title": "Brands", "icon": "verified", "link": "/admin/catalog/brand/"},
                    {"title": "Reviews", "icon": "star", "link": "/admin/catalog/review/"},
                    {"title": "Questions", "icon": "help", "link": "/admin/catalog/qa/"},
                    {"title": "Banners", "icon": "campaign", "link": "/admin/catalog/adbanner/"},
                ],
            },
            {
                "title": "Sales",
                "separator": True,
                "items": [
                    {"title": "Orders", "icon": "receipt_long", "link": "/admin/orders/order/"},
                    {"title": "Carts", "icon": "shopping_cart", "link": "/admin/cart/cart/"},
                ],
            },
            {
                "title": "Services",
                "separator": True,
                "items": [
                    {
                        "title": "Repair services",
                        "icon": "build",
                        "link": "/admin/repairs/repairservice/",
                    },
                    {
                        "title": "Repair bookings",
                        "icon": "assignment",
                        "link": "/admin/repairs/repairbooking/",
                    },
                    {
                        "title": "+ New booking",
                        "icon": "add",
                        "link": "/admin/repairs/repairbooking/add/",
                    },
                ],
            },
            {
                "title": "Users",
                "separator": True,
                "items": [
                    {"title": "Customers", "icon": "group", "link": "/admin/accounts/user/"},
                    {
                        "title": "Addresses",
                        "icon": "location_on",
                        "link": "/admin/accounts/address/",
                    },
                    {
                        "title": "Wishlists",
                        "icon": "favorite",
                        "link": "/admin/wishlist/wishedproduct/",
                    },
                ],
            },
            {
                "title": "Site config",
                "separator": True,
                "items": [
                    {
                        "title": "Homepage hero",
                        "icon": "home",
                        "link": "/admin/catalog/homepage/",
                    },
                    {
                        "title": "Site settings",
                        "icon": "settings",
                        "link": "/admin/catalog/setting/",
                    },
                ],
            },
        ],
    },
}
