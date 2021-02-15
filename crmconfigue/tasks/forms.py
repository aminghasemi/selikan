from .models import Task
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
        fields=("title", "status", "priority","due_date", "account", "description","tags", "assigned_to","done_on", "done_by", "archive")
#    due_date=forms.DateField(label="مهلت انجام",input_formats=MY_DATE_FORMATS,widget=forms.TextInput(attrs={'class': 'shamsi-datepicker'} ))  
  #  done_on=forms.DateField(label="تاریخ تکمیل",input_formats=MY_DATE_FORMATS,widget=AdminJalaliDateWidget )  
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['due_date'] = JalaliDateField(label="مهلت انجام",widget=AdminJalaliDateWidget)
        self.fields['done_on'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False)  
  
#        self.fields['due_date'] = JalaliDateField(label="مهلت انجام",input_formats=MY_DATE_FORMATS,widget=forms.TextInput(attrs={'class': 'shamsi-datepicker'} ))  