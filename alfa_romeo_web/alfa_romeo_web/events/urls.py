from django.urls import path

from alfa_romeo_web.events.views import ListEventsView, DetailEventView

urlpatterns = (
    path('', ListEventsView.as_view(), name='events_list'),
    path('details/<slug:slug>/', DetailEventView.as_view(), name='event_details'),
)
