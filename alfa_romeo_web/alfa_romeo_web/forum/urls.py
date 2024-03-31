from django.urls import path, include

from alfa_romeo_web.forum.views import forum_view, credentials_needed, create_post, posts, details, \
    StaffTopicsForApproval, StaffForumTopicEditView, StaffTopicDeleteView, StaffForumCategoryListView, \
    StaffForumCategoryCreateView, StaffForumCategoryEditView, StaffForumCategoryDeleteView

urlpatterns = (
    path('staff/', include([
        path('', StaffTopicsForApproval.as_view(), name='staff_forum'),
        path('edit_post/<slug:slug>/', StaffForumTopicEditView.as_view(), name='edit_post'),
        path('delete_post/<slug:slug>/', StaffTopicDeleteView.as_view(), name='delete_post'),
        path('categories/', StaffForumCategoryListView.as_view(), name='staff_forum_categories'),
        path('create_forum_category/', StaffForumCategoryCreateView.as_view(), name='staff_create_forum_category'),
        path('edit_forum_category/<int:pk>/', StaffForumCategoryEditView.as_view(), name='staff_edit_forum_category'),
        path('delete_forum_category/<int:pk>/', StaffForumCategoryDeleteView.as_view(), name='staff_delete_forum_category'),
    ])),

    path('', forum_view, name='forum_main_page'),
    path('credentials/', credentials_needed, name='user_forum_credentials'),
    path('create/', create_post, name='create_post'),
    path('topic/<slug:slug>/', posts, name='topics_from_category'),
    path('topic/details/<slug:slug>/', details, name='post_details'),
)