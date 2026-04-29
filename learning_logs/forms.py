# pythonCopy

from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    """Form for adding a new topic."""
    class Meta:
        model = Topic
        fields = ['text']  # only the 'text' field (topic name)


class EntryForm(forms.ModelForm):
    """Form for adding a new entry to a topic."""
    class Meta:
        model = Entry
        fields = ['text']  # only the 'text' field (entry content)


class TopicForm(forms.ModelForm):
    """Form for creating a new topic."""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class EntryForm(forms.ModelForm):
    """Form for adding a new entry."""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}



from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })