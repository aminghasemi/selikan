import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account, Tags
from contacts.models import Contact
from common.models import User, Company
from common.utils import STAGES, SOURCES, CURRENCY_CODES
from teams.models import Teams


class Opportunity(models.Model):
    name = models.CharField( max_length=64, verbose_name="عنوان")
    account = models.ForeignKey(
        Account,
        related_name="opportunities",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="حساب"
    )
    stage = models.CharField(
         max_length=64, choices=STAGES, verbose_name="مرحله"
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CODES, blank=True, null=True, verbose_name="واحد پولی"
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=12, blank=True, null=True, verbose_name="مقدار"
    )
    lead_source = models.CharField(
        max_length=255, choices=SOURCES, blank=True, null=True, verbose_name="منبع فرصت"
    )
    probability = models.IntegerField(default=0, blank=True, null=True, verbose_name="احتمال")
    contacts = models.ManyToManyField(Contact, verbose_name="مشتری")
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="منعقد شده توسط")
    # closed_on = models.DateTimeField(blank=True, null=True)
    closed_on = models.DateField(blank=True, null=True, verbose_name="تاریخ انعقاد")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    assigned_to = models.ManyToManyField(User, related_name="opportunity_assigned_to", verbose_name="محول شده به")
    created_by = models.ForeignKey(
        User,
        related_name="opportunity_created_by",
        on_delete=models.SET_NULL,
        null=True, verbose_name="ایجاد شده توسط"
    )
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    tags = models.ManyToManyField(Tags, blank=True, verbose_name="تگ‌ها")
    teams = models.ManyToManyField(Teams, related_name="oppurtunity_teams", verbose_name="تیم")
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="شرکت"
    )

    class Meta:
        ordering = ["-created_on"]
        verbose_name= "فرصت"
        verbose_name_plural= "فرصت‌ها"

    def __str__(self):
        return self.name

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
