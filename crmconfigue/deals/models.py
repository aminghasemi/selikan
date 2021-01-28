import arrow
from django.core.cache import cache
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Tags
from common.models import User, Company
from contacts.models import Contact
from teams.models import Teams


class Pipeline(models.Model):
    pipeline_number=models.IntegerField(verbose_name="شماره مرحله")
    pipeline_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="pipline_created_by", on_delete=models.SET_NULL, null=True, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="companypipelines", null=True, blank=True, verbose_name="شرکت")

    class Meta:
        verbose_name = "مرحله فروش"
        verbose_name_plural = "مراحل فروش"
    def __str__(self):
        return self.pipeline_title

class Deal(models.Model):
    title = models.CharField(max_length=64, verbose_name="عنوان")
    pipeline_status = models.ForeignKey(Pipeline, related_name="dealpipeline",on_delete=models.SET_NULL,null=True, verbose_name="مرحله فروش")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    assigned_to = models.ManyToManyField(User, related_name="deal_assigned_users", verbose_name="محول شده به")
    account_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="نام حساب")
    deal_amount = models.FloatField(blank=True, null=True, verbose_name="مبلغ معامله")
    created_by = models.ForeignKey(User, related_name="deal_created_by", on_delete=models.SET_NULL, null=True, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    contacts = models.ManyToManyField(Contact, related_name="deal_contacts", verbose_name="مشتریان سرنخ")
    teams = models.ManyToManyField(Teams, related_name="deal_teams", verbose_name="تیم سرنخ")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="companydeals", null=True, blank=True, verbose_name="شرکت")


    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

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
