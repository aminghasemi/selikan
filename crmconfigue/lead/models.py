import arrow
from django.core.cache import cache
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from extensions.utils import jalali_converter
from accounts.models import Tags
from common.models import User, Company
from contacts.models import Contact
from teams.models import Teams

class LeadStatus(models.Model):
    LeadStatus_number=models.IntegerField(verbose_name="شماره مرحله")
    LeadStatus_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="lead_status_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyleadstatus", verbose_name="کاربر سایت")

    class Meta:
        verbose_name = "مرحله سرنخ"
        verbose_name_plural = "مراحل سرنخ"
    def __str__(self):
        return self.LeadStatus_title

class LeadSource(models.Model):
    LeadSource_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="lead_source_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyleadsource", verbose_name="کاربر سایت")

    class Meta:
        verbose_name = "منبع سرنخ"
        verbose_name_plural = "منابع سرنخ"
    def __str__(self):
        return self.LeadSource_title

class Lead(models.Model):
    title = models.CharField(max_length=64, verbose_name="عنوان")
    first_name = models.CharField(max_length=64, verbose_name="نام")
    last_name = models.CharField( max_length=64, verbose_name="نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, verbose_name="موبایل")
    status = models.ForeignKey(LeadStatus, related_name="Lead_status",on_delete=models.CASCADE,verbose_name="مرحله سرنخ")
    source = models.ForeignKey(LeadSource,related_name="Lead_source",on_delete=models.CASCADE, blank=True, verbose_name="منبع")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    assigned_to = models.ForeignKey(User, related_name="lead_assigned_users",on_delete=models.CASCADE, verbose_name="محول شده به")
    created_by = models.ForeignKey(User, related_name="lead_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    tags = models.ForeignKey(Tags, blank=True, on_delete=models.CASCADE, verbose_name="تگ‌ها")
    contacts = models.ForeignKey(Contact,on_delete=models.CASCADE, related_name="lead_contacts", verbose_name="اشخاص مرتبط")
    teams = models.ForeignKey(Teams,on_delete=models.CASCADE, related_name="lead_teams", verbose_name="تیم سرنخ")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companyleads", blank=True, verbose_name="کاربر سایت")
    converted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="lead_converted_by", blank=True, verbose_name="تکمیل‌شده توسط")
    closed_on = models.DateField(blank=True, verbose_name="تاریخ تکمیل")


    class Meta:
        verbose_name = "سرنخ"
        verbose_name_plural = "سرنخ‌ها"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jclosed_on(self):
        return jalali_converter(self.closed_on)
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

    # def save(self, *args, **kwargs):
    #     super(Lead, self).save(*args, **kwargs)
    #     queryset = Lead.objects.all().exclude(status='converted').select_related('created_by'
    #         ).prefetch_related('tags', 'assigned_to',)
    #     open_leads = queryset.exclude(status='closed')
    #     close_leads = queryset.filter(status='closed')
    #     cache.set('admin_leads_open_queryset', open_leads, 60*60)
    #     cache.set('admin_leads_close_queryset', close_leads, 60*60)
