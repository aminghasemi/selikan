import arrow
from django.db import models
from common.models import User, Company
from accounts.models import Account
from contacts.models import Contact
from deals.models import Deal
from lead.models import Lead
from opportunity.models import Opportunity
from tasks.models import Task
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse
from extensions.utils import jalali_converter
from jalali_date import datetime2jalali, date2jalali
from django_jalali.db import models as jmodels


class Doc(models.Model):
    title = models.CharField( max_length=200, verbose_name="عنوان")
    doc = models.FileField(verbose_name="فایل", upload_to="docs", default="")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    account = models.ForeignKey(Account,null=True, related_name="account_docs",blank=True,on_delete=models.SET_NULL, verbose_name="نام مشتری")
    contacts = models.ForeignKey(Contact,blank=True,null=True, related_name="contact_docs",on_delete=models.SET_NULL, verbose_name="نام شخص")
    deals = models.ForeignKey(Deal,blank=True,null=True, related_name="deal_docs",on_delete=models.SET_NULL, verbose_name="عنوان معامله")
    leads = models.ForeignKey(Lead,blank=True,null=True, related_name="lead_docs",on_delete=models.SET_NULL, verbose_name="عنوان سرنخ")
    opportunities = models.ForeignKey(Opportunity,blank=True,null=True, related_name="opportunity_docs",on_delete=models.SET_NULL, verbose_name="عنوان فرصت")
    tasks = models.ForeignKey(Task,blank=True,null=True, related_name="task_docs",on_delete=models.SET_NULL, verbose_name="عنوان وظیفه")
    created_by = models.ForeignKey(User,related_name="docs_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    teams = models.ForeignKey(Teams,null=True,blank=True, related_name="docs_teams",on_delete=models.SET_NULL, verbose_name="تیم")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name='companydocs', blank=True, verbose_name="کاربر سایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")

    def __str__(self):
        return "%s, %s"%(self.title, self.created_on)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()


    class Meta:
        ordering = ["-created_on"]
        verbose_name = "فایل"
        verbose_name_plural = "فایل‌ها"