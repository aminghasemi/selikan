from .models import Task
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=("title", "status", "priority","due_date", "account", "description", "assigned_to","done_on", "done_by")

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_date'] = JalaliDateField(label=('مهلت انجام')) 
        self.fields['due_date'].widget.attrs.update({'class': 'shamsi-datepicker'}) 