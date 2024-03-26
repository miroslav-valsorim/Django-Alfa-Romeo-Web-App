from django.urls import path

from alfa_romeo_web.forum.views import forum_view, credentials_needed, create_post, posts, details, \
    StaffTopicsForApproval, ForumTopicEditView

urlpatterns = (
    path('staff/', StaffTopicsForApproval.as_view(), name='staff_forum'),
    path('staff/edit_post/<slug:slug>/', ForumTopicEditView.as_view(), name='edit_post'),
    path('', forum_view, name='forum_main_page'),
    path('credentials/', credentials_needed, name='user_forum_credentials'),
    path('create/', create_post, name='create_post'),
    path('topic/<slug:slug>/', posts, name='topics_from_category'),
    path('topic/details/<slug:slug>/', details, name='post_details'),
)