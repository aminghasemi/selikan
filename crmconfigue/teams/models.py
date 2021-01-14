import arrow
from extensions.utils import jalali_converter

from django.db import models
from common.models import User, Company
from django.utils.translation import ugettext_lazy as _


class Teams(models.Model):
    name = models.CharField(max_length=100,verbose_name="نام تیم")
    description = models.TextField(verbose_name="توضیحات")
    users = models.ManyToManyField(User, related_name="user_teams", verbose_name="کاربران تیم")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    created_by = models.ForeignKey(
        User,
        related_name="teams_created",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="ساخته شده توسط"
    )

    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نام شرکت"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    def get_users(self):
        return ",".join(
            [str(_id) for _id in list(self.users.values_list("id", flat=True))]
        )
        # return ','.join(list(self.users.values_list('id', flat=True)))
    class Meta:
        verbose_name = "تیم"
        verbose_name_plural = "تیم‌ها"
    def jcreated_on(self):
        return jalali_converter(self.created_on) 