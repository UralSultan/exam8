from django import forms

from discussions.models import Reply, Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('title', 'text',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('text',)

