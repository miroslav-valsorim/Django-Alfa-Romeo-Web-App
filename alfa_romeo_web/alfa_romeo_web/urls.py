"""
MAIN URLS
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('alfa_romeo_web.main_page.urls')),
    path('account/', include('alfa_romeo_web.accounts.urls')),
    path('museum/', include('alfa_romeo_web.museum.urls')),
    path('history/', include('alfa_romeo_web.history.urls')),
    path('events/', include('alfa_romeo_web.events.urls')),
    path('news/', include('alfa_romeo_web.news.urls')),
    path('products/', include('alfa_romeo_web.products.urls')),
    path('cart/', include('alfa_romeo_web.cart.urls')),
    path('checkout/', include('alfa_romeo_web.checkout.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
