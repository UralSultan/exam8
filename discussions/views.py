from django.shortcuts import render
from django.views.generic import ListView

from discussions.models import Topic


class TopicListView(ListView):
    model = (Topic)
    template_name = 'discussions/topic_list.html'
    context_object_name = 'topics'