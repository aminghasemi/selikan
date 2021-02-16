from .models import Dealreport, Leadreport, Opportunityreport, Taskreport, Staffreport, Companyreport
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Field
from django.contrib.admin.widgets import AdminDateWidget
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime



class DealreportForm(forms.ModelForm):
    class Meta:
        model = Dealreport    
        fields=("title", "pipeline_status", "converted_by","startdate", "enddate", "product", "archive")
    def __init__(self, *args, **kwargs):
        super(DealreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)  
  

class LeadreportForm(forms.ModelForm):
    class Meta:
        model = Leadreport    
        fields=("title", "lead_status","lead_source","lead_tags","lead_teams", "converted_by","startdate", "enddate", "archive")
    def __init__(self, *args, **kwargs):
        super(LeadreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)  
  
class OpportunityreportForm(forms.ModelForm):
    class Meta:
        model = Opportunityreport    
        fields=("title", "opportunity_status","opportunity_source","opportunity_tags","opportunity_teams", "converted_by","startdate", "enddate", "archive")
    def __init__(self, *args, **kwargs):
        super(OpportunityreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)  

class TaskreportForm(forms.ModelForm):
    class Meta:
        model = Taskreport    
        fields=("title", "task_status","task_priority","task_tags","task_teams", "done_by","startdate", "enddate", "archive")
    def __init__(self, *args, **kwargs):
        super(TaskreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)  

class StaffreportForm(forms.ModelForm):
    class Meta:
        model = Staffreport    
        fields=("title", "staff","startdate", "enddate", "archive")
    def __init__(self, *args, **kwargs):
        super(StaffreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)

class CompanyreportForm(forms.ModelForm):
    class Meta:
        model = Companyreport    
        fields=("title", "startdate", "enddate", "archive")
    def __init__(self, *args, **kwargs):
        super(CompanyreportForm, self).__init__(*args, **kwargs)
        self.fields['startdate'] = JalaliDateField(label="تاریخ شروع گزارش",widget=AdminJalaliDateWidget)
        self.fields['enddate'] = JalaliDateField(label="تاریخ پایان گزارش",widget=AdminJalaliDateWidget)