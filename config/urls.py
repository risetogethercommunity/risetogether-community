from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("", include("riseapp.urls")),
    path(
        "accounts/", include("accounts.urls", namespace="accounts")
    ),  # <-- namespace here
    path("community/", include("community.urls", namespace="community")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
