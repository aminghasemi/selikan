from .models import Invoice, Invoice_item
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice    
        fields=("paid_status", "invoice_number", "status","date", "account", "description","tax", "total_amount","deal", "expire_date", "bargain","archive")
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label="تاریخ تنظیم",widget=AdminJalaliDateWidget)
        self.fields['expire_date'] = JalaliDateField(label="تاریخ اعتبار",widget=AdminJalaliDateWidget,required=False)  
  
class Invoice_itemForm(forms.ModelForm):
    class Meta:
        model = Invoice_item    
        fields=("product_name", "amount")