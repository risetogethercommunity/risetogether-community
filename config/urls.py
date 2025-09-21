from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('riseapp.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),  # <-- namespace here
]
