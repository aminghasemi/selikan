import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from extensions.utils import jalali_converter
from accounts.models import Account, Tags
from contacts.models import Contact
from common.models import User, Company, Enrolled
from common.utils import STAGES, SOURCES, CURRENCY_CODES
from teams.models import Teams

class OpportunityStatus(models.Model):
    OpportunityStatus_number=models.IntegerField(verbose_name="شماره مرحله")
    OpportunityStatus_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="opportunity_status_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyopportunitystatus", verbose_name="کاربر سایت")
    won = models.BooleanField(default=False, verbose_name="در صورتی که این مرحله بیانگر مرحله پایانی و فرصت موفق است این تیک را بزنید.")
    lost = models.BooleanField(default=False, verbose_name="در صورتی که این مرحله بیانگر مرحله پایانی و شکست در فرصت است این تیک را بزنید.")
    class Meta:
        verbose_name = "مرحله فرصت"
        verbose_name_plural = "مراحل فرصت"
    def __str__(self):
        return self.OpportunityStatus_title

class OpportunitySource(models.Model):
    OpportunitySource_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="opportunity_source_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyopportunitysource", verbose_name="کاربر سایت")

    class Meta:
        verbose_name = "منبع فرصت"
        verbose_name_plural = "منابع فرصت"
    def __str__(self):
        return self.OpportunitySource_title

class Opportunity(models.Model):
    name = models.CharField( max_length=64, verbose_name="عنوان")
    account = models.ForeignKey(Account,related_name="opportunities",on_delete=models.SET_NULL,null=True, blank=True,verbose_name="مشتری")
    status = models.ForeignKey(OpportunityStatus,blank=True, related_name="Opportunity_status",on_delete=models.SET_NULL, null=True,verbose_name="مرحله")
    source = models.ForeignKey(OpportunitySource,related_name="Opportunity_source",on_delete=models.SET_NULL, null=True, blank=True, verbose_name="منبع")
    amount = models.FloatField(blank=True,null=True, verbose_name="مبلغ")
    probability = models.IntegerField(default=0, blank=True,null=True, verbose_name="احتمال")
    contacts = models.ForeignKey(Contact,blank=True, on_delete=models.SET_NULL, null=True, verbose_name="شخص")
    converted_by = models.ForeignKey(Enrolled,related_name="Opportunity_converted_by", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تکمیل‌شده توسط")
    closed_on = models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    description = models.TextField(blank=True,null=True, verbose_name="توضیحات")
    assigned_to = models.ForeignKey(Enrolled,blank=True, on_delete=models.SET_NULL, null=True, related_name="opportunity_assigned_to", verbose_name="محول شده به")
    created_by = models.ForeignKey(User,related_name="opportunity_created_by", on_delete=models.SET_NULL, null=True, verbose_name="ایجاد شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    tags = models.ForeignKey(Tags,on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تگ‌ها")
    teams = models.ForeignKey(Teams,on_delete=models.SET_NULL, null=True,blank=True, related_name="oppurtunity_teams", verbose_name="تیم")
    company = models.ForeignKey(Company, related_name= "companyopportunity", on_delete=models.SET_NULL, null=True,  blank=True, verbose_name="کاربر سایت")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")

    class Meta:
        ordering = ["-created_on"]
        verbose_name= "فرصت"
        verbose_name_plural= "فرصت‌ها"

    def __str__(self):
        return self.name
    def jclosed_on(self):
        return jalali_converter(self.closed_on)
    def jcreated_on(self):
        return jalali_converter(self.created_on)

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))
