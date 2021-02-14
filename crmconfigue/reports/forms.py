from .models import Dealreport
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



class DealreportForm(forms.ModelForm):
    class Meta:
        model = Dealreport    
        fields=("title", "pipeline_status", "converted_by","startdate", "enddate", "product", "archive")
#    due_date=forms.DateField(label="مهلت انجام",input_formats=MY_DATE_FORMATS,widget=forms.TextInput(attrs={'class': 'shamsi-datepicker'} ))  
  #  done_on=forms.DateField(label="تاریخ تکمیل",input_formats=MY_DATE_FORMATS,widget=AdminJalaliDateWidget )  
    def __init__(self, *args, **kwargs):
        super(DealreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)  
  
#        self.fields['due_date'] = JalaliDateField(label="مهلت انجام",input_formats=MY_DATE_FORMATS,widget=forms.TextInput(attrs={'class': 'shamsi-datepicker'} ))  