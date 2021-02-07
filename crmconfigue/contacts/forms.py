from .models import Contact
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields=("first_name","last_name","email","phone","office_phone","fax","is_active","billing_address_line","billing_street","billing_city","billing_state","billing_postcode","billing_country","birthday","description")


