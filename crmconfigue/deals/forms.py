from .models import Deal
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields=("title","pipeline_status", "description", "assigned_to","account","deal_amount", "is_active", "closed_on","teams")
