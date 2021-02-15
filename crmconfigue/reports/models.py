import arrow
from django.db import models
from common.models import User, Company, Product
from accounts.models import Account
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse
from extensions.utils import jalali_converter
from jalali_date import datetime2jalali, date2jalali
from deals.models import Pipeline
from lead.models import LeadStatus, LeadSource
from accounts.models import Tags
from teams.models import Teams
from opportunity.models import OpportunityStatus, OpportunitySource

class Dealreport(models.Model):

    title=models.CharField( max_length=200, verbose_name="عنوان")
    pipeline_status = models.ForeignKey(Pipeline, related_name="reportpipeline", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="مرحله فروش")
    created_by = models.ForeignKey(User, related_name="report_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    converted_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="report_deal_converted_by", blank=True, verbose_name="تکمیل‌شده توسط")
    startdate = models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    enddate= models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companydealsreports",  blank=True, verbose_name="شرکت")
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,  related_name="reports_dealproducts",  blank=True, verbose_name="محصول")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = " گزارش معاملات"
        verbose_name_plural = "گزارشات معاملات"

    def __str__(self):
        return (self.title)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdone_on(self):
        return jalali_converter(self.startdate)
    def jdue_date(self):
        return jalali_converter(self.enddate)


class Leadreport(models.Model):

    title=models.CharField( max_length=200, verbose_name="عنوان")
    lead_status = models.ForeignKey(LeadStatus, related_name="report_lead_status", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="مرحله سرنخ")
    lead_source = models.ForeignKey(LeadSource, related_name="report_lead_source", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="منبع سرنخ") 
    created_by = models.ForeignKey(User, related_name="lead_report_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    converted_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="report_lead_converted_by", blank=True, verbose_name="تکمیل‌شده توسط")
    startdate = models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    enddate= models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companyleadsreports",  blank=True, verbose_name="شرکت")
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,  related_name="reports_leadproducts",  blank=True, verbose_name="محصول")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    lead_tags = models.ForeignKey(Tags, related_name="report_lead_tags", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="تگ‌های سرنخ‌ها")
    lead_teams = models.ForeignKey(Teams, related_name="report_lead_teams", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="تیم‌ها")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "گزارش سرنخ‌ها"
        verbose_name_plural = "گزارشات سرنخ‌ها"

    def __str__(self):
        return (self.title)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdone_on(self):
        return jalali_converter(self.startdate)
    def jdue_date(self):
        return jalali_converter(self.enddate)

class Opportunityreport(models.Model):

    title=models.CharField( max_length=200, verbose_name="عنوان")
    opportunity_status = models.ForeignKey(OpportunityStatus, related_name="report_opportunity_status", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="مرحله فرصت‌")
    opportunity_source = models.ForeignKey(OpportunitySource, related_name="report_opportunity_source", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="منبع فرصت‌") 
    created_by = models.ForeignKey(User, related_name="opportunity_report_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    converted_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="report_opportunity_converted_by", blank=True, verbose_name="تکمیل‌شده توسط")
    startdate = models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    enddate= models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companyopportunityreports",  blank=True, verbose_name="شرکت")
    product= models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,  related_name="reports_opportunityproducts",  blank=True, verbose_name="محصول")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    opportunity_tags = models.ForeignKey(Tags, related_name="report_opportunity_tags", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="تگ‌های فرصت‌ها")
    opportunity_teams = models.ForeignKey(Teams, related_name="report_opportunity_teams", blank=True,on_delete=models.SET_NULL,null=True,  verbose_name="تیم‌ها")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "گزارش فرصت‌ها"
        verbose_name_plural = "گزارشات فرصت‌ها"

    def __str__(self):
        return (self.title)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdone_on(self):
        return jalali_converter(self.startdate)
    def jdue_date(self):
        return jalali_converter(self.enddate)