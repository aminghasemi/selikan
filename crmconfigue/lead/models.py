import arrow
from django.core.cache import cache
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Tags
from common.models import User, Company
from common.utils import COUNTRIES, LEAD_SOURCE, LEAD_STATUS, return_complete_address
from contacts.models import Contact
from teams.models import Teams


class Lead(models.Model):
    title = models.CharField(
         max_length=64, verbose_name="عنوان"
    )
    first_name = models.CharField( null=True, max_length=255, verbose_name="نام")
    last_name = models.CharField( null=True, max_length=255, verbose_name="نام خانوادگی")
    email = models.EmailField(null=True, blank=True, verbose_name="ایمیل")
    phone = PhoneNumberField(null=True, blank=True, verbose_name="موبایل")
    status = models.CharField(
         max_length=255, blank=True, null=True, choices=LEAD_STATUS, verbose_name="وضعیت سرنخ"
    )
    source = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="منبع"
    )
    address_line = models.CharField( max_length=255, blank=True, null=True, verbose_name="آدرس")
    street = models.CharField( max_length=55, blank=True, null=True, verbose_name="خیابان")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="شهر")
    state = models.CharField( max_length=255, blank=True, null=True, verbose_name="استان")
    postcode = models.CharField(
         max_length=10, blank=True, null=True, verbose_name="کد پستی"
    )
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True, verbose_name="کشور")
    website = models.CharField( max_length=255, blank=True, null=True, verbose_name="وب‌سایت")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    assigned_to = models.ManyToManyField(User, related_name="lead_assigned_users", verbose_name="محول شده به")
    account_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="نام حساب")
    opportunity_amount = models.DecimalField(
        decimal_places=2, max_digits=12, blank=True, null=True, verbose_name="مقدار فرصت"
    )
    created_by = models.ForeignKey(
        User, related_name="lead_created_by", on_delete=models.SET_NULL, null=True, verbose_name="ساخته شده توسط"
    )
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    enquery_type = models.CharField(max_length=255, blank=True, null=True, verbose_name="وضعیت استعلام")
    tags = models.ManyToManyField(Tags, blank=True, verbose_name="تگ‌ها")
    contacts = models.ManyToManyField(Contact, related_name="lead_contacts", verbose_name="مشتریان سرنخ")
    created_from_site = models.BooleanField(default=False, verbose_name="ایجاد شده توسط سایت")
    teams = models.ManyToManyField(Teams, related_name="lead_teams", verbose_name="تیم سرنخ")
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="شرکت"
    )


    class Meta:
        verbose_name = "سرنخ"
        verbose_name_plural = "سرنخ‌ها"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_complete_address(self):
        return return_complete_address(self)

    @property
    def phone_raw_input(self):
        if str(self.phone) == "+NoneNone":
            return ""
        return self.phone

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
