from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from discussions.forms import ReplyForm, TopicForm
from discussions.models import Reply, Topic


class TopicListView(ListView):
    model = Topic
    template_name = 'discussions/topic_list.html'
    context_object_name = 'topics'

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'discussions/topic_detail.html'
    context_object_name = 'topic'


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'discussions/topic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
