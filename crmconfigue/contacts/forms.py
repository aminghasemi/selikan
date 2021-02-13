from .models import Contact
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields=("first_name","last_name","email","phone","office_phone","fax","is_active","billing_address_line","billing_street","billing_city","billing_state","billing_postcode","billing_country","birthday","description", "archive")
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['birthday'] = JalaliDateField(label="تاریخ تکمیل",widget=AdminJalaliDateWidget,required=False) 

