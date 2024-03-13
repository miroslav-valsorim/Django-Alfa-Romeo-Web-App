"""
MAIN URLS
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("alfa_romeo_web.main_page.urls")),
    path('account/', include("alfa_romeo_web.accounts.urls")),
]
