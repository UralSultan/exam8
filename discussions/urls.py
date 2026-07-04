from django.urls import path

from discussions.views import (TopicCreateView, TopicDeleteView, TopicDetailView, TopicListView, TopicUpdateView,
                               ReplyCreateView, ReplyUpdateView, ReplyDeleteView)

app_name = 'discussions'

urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
    path('topics/<int:pk>/edit/', TopicUpdateView.as_view(), name='topic_update'),
    path('topics/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic_delete'),
    path('topics/<int:pk>/reply/', ReplyCreateView.as_view(), name='reply_create'),
    path('replies/<int:pk>/edit/', ReplyUpdateView.as_view(), name='reply_update'),
    path('replies/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
]
