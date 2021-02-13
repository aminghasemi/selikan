from .models import Doc
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class DocForm(forms.ModelForm):
    class Meta:
        model = Doc    
        fields=("title", "doc", "account","contacts", "deals", "leads", "opportunities","tasks", "teams","description", "archive")