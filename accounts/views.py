from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.db.models import Count
from accounts.forms import RegisterForm
from . models import User
from discussions.models import Topic


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('discussions:topic_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return User.objects.annotate(replies_count=Count('replies'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = (
            Topic.objects
            .filter(author=self.object)
            .annotate(replies_count=Count('replies'))
            .order_by('-created_at')
        )
        return context