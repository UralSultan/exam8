from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from discussions.forms import TopicForm
from discussions.models import Topic


class TopicListView(ListView):
    model = Topic
    template_name = 'discussions/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        return (
            Topic.objects
            .select_related('author')
            .annotate(replies_count=Count('replies'))
            .order_by('-created_at')
        )


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


class TopicAuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Topic

    def test_func(self):
        return self.get_object().author == self.request.user


class TopicUpdateView(TopicAuthorRequiredMixin, UpdateView):
    form_class = TopicForm
    template_name = 'discussions/topic_update.html'


class TopicDeleteView(TopicAuthorRequiredMixin, DeleteView):
    success_url = reverse_lazy('discussions:topic_list')
    template_name = 'discussions/topic_confirm_delete.html'
