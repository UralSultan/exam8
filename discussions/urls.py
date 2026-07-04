from django.urls import path
from discussions.views import TopicListView, TopicCreateView, TopicDetailView

app_name = 'discussions'

urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
    path('topics/create/', TopicCreateView.as_view(), name='topic_create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic_detail'),
]
