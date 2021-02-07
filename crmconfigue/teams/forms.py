from .models import Teams
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class TeamForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields=("name","description","users","is_active")