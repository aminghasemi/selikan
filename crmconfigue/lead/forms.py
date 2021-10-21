from .models import Lead, LeadStatus, LeadSource
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields=("title","first_name","last_name","email","phone","status","source","description","assigned_to","is_active","tags","due_date","teams","converted_by","closed_on", "archive")
    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        self.fields['closed_on'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False)
        self.fields['due_date'] = JalaliDateField(label="تاریخ پیگیری",widget=AdminJalaliDateWidget,required=False)
class LeadStatusForm(forms.ModelForm):
    class Meta:
        model = LeadStatus
        fields= ("LeadStatus_number","LeadStatus_title")

class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields= ("LeadSource_title",)