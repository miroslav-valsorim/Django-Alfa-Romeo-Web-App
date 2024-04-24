"""
MAIN URLS
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import handler403, handler500

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Our URLs
    path('', include('alfa_romeo_web.main_page.urls')),
    path('account/', include('alfa_romeo_web.accounts.urls')),
    path('museum/', include('alfa_romeo_web.museum.urls')),
    path('history/', include('alfa_romeo_web.history.urls')),
    path('events/', include('alfa_romeo_web.events.urls')),
    path('news/api/', include('alfa_romeo_web.news.api.urls')),
    path('news/', include('alfa_romeo_web.news.urls')),
    path('products/', include('alfa_romeo_web.products.urls')),
    path('cart/', include('alfa_romeo_web.cart.urls')),
    path('checkout/', include('alfa_romeo_web.checkout.urls')),
    path('forum/', include('alfa_romeo_web.forum.urls')),

    # PayPal URL
    path('', include('paypal.standard.ipn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Media and Static for Production
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

handler403 = 'alfa_romeo_web.main_page.views.custom_403'
handler500 = 'alfa_romeo_web.main_page.views.custom_500'
