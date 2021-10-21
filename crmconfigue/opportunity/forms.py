from .models import Opportunity, OpportunityStatus, OpportunitySource
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields=("name","account","status","source","amount","probability","due_date","converted_by","closed_on","description","assigned_to","is_active","tags","teams", "archive")
    def __init__(self, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs)
        self.fields['closed_on'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False)
        self.fields['due_date'] = JalaliDateField(label="تاریخ پیگیری",widget=AdminJalaliDateWidget,required=False)
class OpportunityStatusForm(forms.ModelForm):
    class Meta:
        model = OpportunityStatus
        fields= ("OpportunityStatus_number","OpportunityStatus_title")

class OpportunitySourceForm(forms.ModelForm):
    class Meta:
        model = OpportunitySource
        fields= ("OpportunitySource_title",)