from django.urls import path

from discussions import views

app_name = 'discussions'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
]
