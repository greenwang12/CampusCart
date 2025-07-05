from django.contrib import admin
from django.urls import path, include
from backend.views import api_home  # 👈 import the home view

urlpatterns = [
    path('', api_home),  # 👈 this shows your homepage at /
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
]
