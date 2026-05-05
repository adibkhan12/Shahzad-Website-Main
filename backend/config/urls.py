from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path, re_path

# Path to the Angular SPA's index.html — populated by the multi-stage
# Dockerfile. Used as a fallback for client-side routes that Angular Router
# handles (e.g., /products/iphone-15-pro). The actual JS/CSS files are served
# at the URL root by the WhiteNoise wrapper in wsgi.py.
SPA_INDEX = Path(settings.BASE_DIR) / "frontend_dist" / "browser" / "index.html"


def spa_fallback(request):
    """Serve the SPA's index.html for any non-API/non-admin path."""
    if not SPA_INDEX.exists():
        raise Http404(
            "Frontend not built. Build the container with the Dockerfile at the repo root, "
            "or run `npm start` separately for local development."
        )
    return FileResponse(open(SPA_INDEX, "rb"), content_type="text/html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("config.api_urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Catchall — MUST be last. Serves the SPA for everything that isn't /admin/
# or /api/v1/. Static files are intercepted earlier by WhiteNoise (wsgi.py).
urlpatterns += [re_path(r"^.*$", spa_fallback)]
