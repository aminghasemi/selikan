from .models import Account
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields=("name","national_id", "economic_id", "email","phone","office_phone", "fax", "industry","billing_address_line","billing_street","billing_city", "billing_state", "billing_postcode", "billing_country", "website", "description", "is_active", "tags", "contacts")
