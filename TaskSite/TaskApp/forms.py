from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['user_email', 'task', 'due_by', 'priority', 'is_urgent']