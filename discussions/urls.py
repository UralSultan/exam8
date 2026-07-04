from django.urls import path
from discussions.views import TopicListView

app_name = 'discussions'

urlpatterns = [
    path('', TopicListView.as_view(), name='topic_list'),
]
