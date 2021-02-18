import arrow
from django.core.cache import cache
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from extensions.utils import jalali_converter

from accounts.models import Tags, Account
from common.models import User, Company, Product
from contacts.models import Contact
from teams.models import Teams


class Pipeline(models.Model):
    pipeline_number=models.IntegerField(verbose_name="ترتیب در فرایند")
    pipeline_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="pipline_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companypipelines", verbose_name="شرکت")
    won = models.BooleanField(default=False, verbose_name="در صورتی که این مرحله بیانگر مرحله پایانی و فروش موفق است این تیک را بزنید.")
    lost = models.BooleanField(default=False, verbose_name="در صورتی که این مرحله بیانگر مرحله پایانی و شکست در معامله است این تیک را بزنید.")

    class Meta:
        verbose_name = "مرحله فروش"
        verbose_name_plural = "مراحل فروش"
    def __str__(self):
        return self.pipeline_title

class Deal(models.Model):
    title = models.CharField(max_length=64, verbose_name="عنوان")
    pipeline_status = models.ForeignKey(Pipeline, related_name="dealpipeline",on_delete=models.CASCADE, verbose_name="مرحله فروش")
    description = models.TextField(blank=True,  verbose_name="توضیحات")
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="deal_assigned_users", blank=True, verbose_name="محول شده به")
    account_name = models.CharField(max_length=255,  blank=True, verbose_name="نام حساب")
    deal_amount = models.DecimalField(decimal_places=0, max_digits=20,blank=True, null=True, verbose_name="مبلغ معامله")
  #  deal_amount = models.IntegerField(blank=True, null=True, verbose_name="مبلغ معامله")
    created_by = models.ForeignKey(User, related_name="deal_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    account = models.ForeignKey(Account,on_delete=models.SET_NULL,blank=True,null=True, related_name="deal_acounts", verbose_name="مشتری")
    teams = models.ForeignKey(Teams,blank=True, on_delete=models.SET_NULL,null=True, related_name="deal_teams", verbose_name="تیم معالمه")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companydeals",  blank=True, verbose_name="شرکت")
    product= models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name="dealproducts",  blank=True, verbose_name="محصول")
    converted_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name="deal_converted_by", blank=True, verbose_name="تکمیل‌شده توسط")
    closed_on = models.DateField(blank=True,null=True, verbose_name="تاریخ تکمیل")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")


    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"
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
