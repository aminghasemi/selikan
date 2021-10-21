from .models import Project
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project    
        fields=("title", "status", "end_date","start_date","project_manager","teams", "description","tags", "archive")
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(label="تاریخ شروع",widget=AdminJalaliDateWidget)
        self.fields['end_date'] = JalaliDateField(label="تاریخ پایان",widget=AdminJalaliDateWidget,required=False)  

