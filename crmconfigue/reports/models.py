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
        verbose_name = "گزارش"
        verbose_name_plural = "گزارشات"

    def __str__(self):
        return (self.title)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdone_on(self):
        return jalali_converter(self.startdate)
    def jdue_date(self):
        return jalali_converter(self.enddate)