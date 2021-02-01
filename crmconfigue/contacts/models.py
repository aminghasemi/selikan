
import arrow
from django.db import models

from common.models import Address, User, Company, Country, Province
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams


class Contact(models.Model):
    first_name = models.CharField(verbose_name="نام", max_length=255)
    last_name = models.CharField(verbose_name="نام خانوادگی", max_length=255)
    email = models.EmailField(blank=True,verbose_name="ایمیل")
    phone = models.CharField(max_length=20,blank=True, verbose_name="موبایل")
    office_phone = models.CharField(max_length=20,blank=True, verbose_name="تلفن ثابت")
    fax = models.CharField(max_length=20,blank=True, verbose_name="شماره فکس ")
    address = models.CharField(verbose_name="آدرس",blank=True, max_length=350)
    description = models.TextField(blank=True,verbose_name="توضیحات")
    created_by = models.ForeignKey(User, related_name="contact_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True,verbose_name="فعال")
    billing_address_line = models.CharField(max_length=255, blank=True, verbose_name="آدرس")
    billing_street = models.CharField(max_length=55, blank=True, verbose_name="خیابان")
    billing_city = models.CharField( max_length=255, blank=True, verbose_name="شهر")
    billing_state = models.ForeignKey(Province, on_delete=models.CASCADE, max_length=255, blank=True, verbose_name="استان")
    billing_postcode = models.CharField(max_length=10, blank=True, verbose_name="کد پستی")
    billing_country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, verbose_name="کشور")
    company = models.ForeignKey(Company, related_name="companycontacts", on_delete=models.CASCADE, blank=True, verbose_name="شرکت")

    def __str__(self):
        return self.first_name
    def jcreated_on(self):
        return jalali_converter(self.created_on)

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ["-created_on"]

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
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"