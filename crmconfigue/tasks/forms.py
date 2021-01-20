from .models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=("title", "status", "priority","due_date", "account", "contacts", "assigned_to")