from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.core.paginator import Paginator
from discussions.forms import TopicForm, ReplyForm
from discussions.models import Topic, Reply


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
    replies_per_page = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = (
            self.object.replies
            .select_related('author')
            .order_by('-created_at')
        )
        paginator = Paginator(replies, self.replies_per_page)
        page_number = self.request.GET.get('page')
        replies_page = paginator.get_page(page_number)
        context['reply_form'] = ReplyForm()
        context['replies_page'] = replies_page
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'discussions/topic_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicUpdatePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Topic

    def test_func(self):
        topic = self.get_object()
        user = self.request.user

        return topic.author == user or user.has_perm('discussions.change_topic')


class TopicDeletePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Topic

    def test_func(self):
        topic = self.get_object()
        user = self.request.user

        return topic.author == user or user.has_perm('discussions.delete_topic')


class TopicUpdateView(TopicUpdatePermissionMixin, UpdateView):
    form_class = TopicForm
    template_name = 'discussions/topic_update.html'


class TopicDeleteView(TopicDeletePermissionMixin, DeleteView):
    success_url = reverse_lazy('discussions:topic_list')
    template_name = 'discussions/topic_confirm_delete.html'


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('discussions:topic_detail', kwargs={'pk': self.kwargs['pk']})


class ReplyUpdatePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Reply

    def test_func(self):
        reply = self.get_object()
        user = self.request.user

        return reply.author == user or user.has_perm('discussions.change_reply')


class ReplyDeletePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Reply

    def test_func(self):
        reply = self.get_object()
        user = self.request.user

        return reply.author == user or user.has_perm('discussions.delete_reply')


class ReplyUpdateView(ReplyUpdatePermissionMixin, UpdateView):
    form_class = ReplyForm
    template_name = 'discussions/reply_update.html'

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


class ReplyDeleteView(ReplyDeletePermissionMixin, DeleteView):
    template_name = 'discussions/reply_confirm_delete.html'

    def get_success_url(self):
        return self.object.topic.get_absolute_url()