import arrow
from django.db import models
from common.models import User, Company
from accounts.models import Account
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse

class Task(models.Model):

    STATUS_CHOICES = (
        ("New", "جدید"),
        ("In Progress", "در حال انجام"),
        ("Completed", "پایان یافته"),
    )

    PRIORITY_CHOICES = (("Low", "پایین"), ("Medium", "معمولی"), ("High", "بالا"))

    title = models.CharField( max_length=200, verbose_name="عنوان")
    status = models.CharField( max_length=50, choices=STATUS_CHOICES, verbose_name="وضعیت")
    priority = models.CharField( max_length=50, choices=PRIORITY_CHOICES, verbose_name="تقدم")
    due_date = models.DateField(blank=True, null=True, verbose_name="مهلت انجام")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    account = models.ForeignKey(
        Account,
        related_name="accounts_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL, verbose_name="نام شرکت"
    )

    contacts = models.ManyToManyField(Contact, related_name="contacts_tasks", verbose_name="نام مشتری")

    assigned_to = models.ManyToManyField(User, related_name="users_tasks", verbose_name="محول شده به")

    created_by = models.ForeignKey(
        User,
        related_name="task_created",
        blank=True,
        null=True,
        on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط"
    )
    teams = models.ManyToManyField(Teams, related_name="tasks_teams", verbose_name="تیم")
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name='companytask', null=True, blank=True, verbose_name="کاربر سایت"
    )

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

    class Meta:
        ordering = ["-due_date"]
        verbose_name = "کار"
        verbose_name_plural = "کارها"
