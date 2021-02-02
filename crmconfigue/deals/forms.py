from .models import Deal
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields=("title","pipeline_status", "description", "assigned_to","account_name","deal_amount", "is_active", "closed_on","teams")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-3'),
                Column('pipeline_status', css_class='col-3'),
                Column('assigned_to', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'description',
            Row(
                Column('account_name', css_class='form-group col-md-3 mb-0'),
                Column('deal_amount', css_class='form-group col-md-3 mb-0'),
                Column('closed_on', css_class='form-group col-md-3 mb-0', id='persiandate'),
                css_class='form-row'
            ),
            
            Submit('submit', 'ذخیره')
        )