from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.views import api_home

urlpatterns = [
    path('', api_home),                  
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),   # ✅ this adds "/api/" prefix to everything
]

# Only serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
