from django.urls import path, include

from alfa_romeo_web.events.views import ListEventsView, DetailEventView, StaffEventListView, StaffEventCreateView, \
    StaffEventEditView, StaffEventDeleteView

urlpatterns = (
    path('staff/', include([
            path('', StaffEventListView.as_view(), name='staff_event'),
            path('create_event/', StaffEventCreateView.as_view(), name='staff_create_event'),
            path('edit_event/<slug:slug>/', StaffEventEditView.as_view(), name='staff_edit_event'),
            path('delete_event/<slug:slug>/', StaffEventDeleteView.as_view(), name='staff_delete_event'),
    ])),

    path('', ListEventsView.as_view(), name='events_list'),
    path('details/<slug:slug>/', DetailEventView.as_view(), name='event_details'),
)
