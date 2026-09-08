from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda user: f"{user.first_name} {user.last_name}"
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
