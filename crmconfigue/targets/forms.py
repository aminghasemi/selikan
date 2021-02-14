from .models import Targetsubject, CompanyTargets, StaffTargets
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class CompanyTargetsForm(forms.ModelForm):
    class Meta:
        model = CompanyTargets
        fields=("title","target_subject","target","current","start_date","end_date","is_active","archive")
    def __init__(self, *args, **kwargs):
        super(CompanyTargetsForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(label="تاریخ شروع",widget=AdminJalaliDateWidget,required=False)  
        self.fields['end_date'] = JalaliDateField(label="تاریخ پایان",widget=AdminJalaliDateWidget,required=False)  
class StaffTargetsForm(forms.ModelForm):
    class Meta:
        model = StaffTargets
        fields=("title","target_subject","target","current","start_date","end_date","is_active","archive","staff")
    def __init__(self, *args, **kwargs):
        super(StaffTargetsForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(label="تاریخ شروع",widget=AdminJalaliDateWidget,required=False)  
        self.fields['end_date'] = JalaliDateField(label="تاریخ پایان",widget=AdminJalaliDateWidget,required=False)  

class TargetsubjectForm(forms.ModelForm):
    class Meta:
        model = Targetsubject
        fields= ("subject_title",)