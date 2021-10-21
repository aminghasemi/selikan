import arrow
from django.db import models
from common.models import User, Company, Enrolled
from accounts.models import Tags
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse
from extensions.utils import jalali_converter
from jalali_date import datetime2jalali, date2jalali
from django_jalali.db import models as jmodels
# Create your models here.

class Project(models.Model):

    STATUS_CHOICES = (
        ("جدید", "جدید"),
        ("در حال انجام", "در حال انجام"),
        ("پایان یافته", "پایان یافته"),
    )




    title = models.CharField( max_length=200,null=True,blank=True, verbose_name="عنوان")
    status = models.CharField( max_length=50,null=True,blank=True, choices=STATUS_CHOICES, verbose_name="وضعیت")
    end_date = models.DateField(null=True,blank=True, verbose_name="تاریخ پایان ")
    start_date = models.DateField(null=True,blank=True, verbose_name="تاریخ شروع ")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    project_manager = models.ForeignKey(Enrolled,blank=True,null=True, related_name="project_manager",on_delete=models.SET_NULL, verbose_name="مدیر پروژه")
    created_by = models.ForeignKey(User,related_name="project_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    teams = models.ForeignKey(Teams,null=True,blank=True, related_name="project_teams",on_delete=models.SET_NULL, verbose_name="تیم")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name='companyproject', blank=True, verbose_name="شرکت")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    tags = models.ForeignKey(Tags, blank=True, on_delete=models.SET_NULL,related_name="project_tags", null=True, verbose_name="تگ‌ها")

    def __str__(self):
        return (self.title)




    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"
