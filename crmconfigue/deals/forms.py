from .models import Deal, Pipeline
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.shortcuts import get_object_or_404
from common.models import Company
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields=("title","pipeline_status", "description","due_date", "assigned_to","account","deal_amount", "is_active", "closed_on","teams", "archive")
    def __init__(self, *args, **kwargs):
        super(DealForm, self).__init__(*args, **kwargs)
        self.fields['closed_on'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False)
        self.fields['due_date'] = JalaliDateField(label="تاریخ پیگیری",widget=AdminJalaliDateWidget,required=False)