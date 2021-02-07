from .models import Lead, LeadStatus, LeadSource
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields=("title","first_name","last_name","email","phone","status","source","description","assigned_to","is_active","tags","contacts","teams","converted_by","closed_on")

class LeadStatusForm(forms.ModelForm):
    class Meta:
        model = LeadStatus
        fields= ("LeadStatus_number","LeadStatus_title")

class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields= ("LeadSource_title",)