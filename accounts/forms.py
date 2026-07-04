from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'avatar', 'password1', 'password2')

