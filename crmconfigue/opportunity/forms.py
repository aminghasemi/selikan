from .models import Opportunity, OpportunityStatus, OpportunitySource
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields=("name","account","status","source","amount","probability","contacts","converted_by","closed_on","description","assigned_to","is_active","tags","teams")

class OpportunityStatusForm(forms.ModelForm):
    class Meta:
        model = OpportunityStatus
        fields= ("OpportunityStatus_number","OpportunityStatus_title")

class OpportunitySourceForm(forms.ModelForm):
    class Meta:
        model = OpportunitySource
        fields= ("OpportunitySource_title",)