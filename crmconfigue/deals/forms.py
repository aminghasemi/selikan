from .models import Deal, Pipeline
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.shortcuts import get_object_or_404
from common.models import Company

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields=("title","pipeline_status", "description", "assigned_to","account","deal_amount", "is_active", "closed_on","teams")
