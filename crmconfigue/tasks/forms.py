from .models import Task, TaskSubject
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task    
        fields=("title", "status","project", "priority","subject","tasksubject","due_date", "account", "description","tags", "assigned_to","done_on", "done_by", "archive")
        account = forms.CharField(widget=forms.TextInput(attrs={'id': 'select2'} ))  
#    due_date=forms.DateField(label="مهلت انجام",input_formats=MY_DATE_FORMATS,widget=forms.TextInput(attrs={'class': 'shamsi-datepicker'} ))  
  #  done_on=forms.DateField(label="تاریخ تکمیل",input_formats=MY_DATE_FORMATS,widget=AdminJalaliDateWidget )  
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_date'] = JalaliDateField(label="مهلت انجام",widget=AdminJalaliDateWidget)
        self.fields['done_on'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False)  

class TaskSubjectForm(forms.ModelForm):
    class Meta:
        model = TaskSubject
        fields= ("tasksubject_title",)