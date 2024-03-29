
import arrow
from django.db import models
from extensions.utils import jalali_converter
from common.utils import COUNTRIES, ROLES, INDCHOICES, PROVINCE, UNITS, CURRENCY

from common.models import Address, User, Company, Country, Province
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from accounts.models import Account

class Contact(models.Model):
    first_name = models.CharField(verbose_name="نام",null=True,blank=True, max_length=255)
    last_name = models.CharField(verbose_name="نام خانوادگی",null=True,blank=True, max_length=255)
    position = models.CharField(verbose_name="سمت",null=True,blank=True, max_length=255)
    email = models.EmailField(blank=True,null=True,verbose_name="ایمیل")
    phone = models.CharField(max_length=20,blank=True,null=True, verbose_name="موبایل")
    whatsapp_phone = models.CharField(max_length=20,null=True,blank=True, verbose_name="شماره تماس واتساپ")
    office_phone = models.CharField(max_length=20,blank=True,null=True, verbose_name="تلفن ثابت")
    fax = models.CharField(max_length=20,blank=True,null=True, verbose_name="شماره فکس ")
    address = models.CharField(verbose_name="آدرس",blank=True,null=True, max_length=350)
    description = models.TextField(blank=True,null=True,verbose_name="توضیحات")
    created_by = models.ForeignKey(User, related_name="contact_created_by",  on_delete=models.SET_NULL,null=True, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True,verbose_name="فعال")
    billing_address_line = models.CharField(max_length=255, blank=True,null=True, verbose_name="آدرس")
    billing_city = models.CharField( max_length=255, blank=True,null=True, verbose_name="شهر")
    billing_state = models.CharField(max_length=200, choices=PROVINCE, blank=True, null=True,verbose_name="استان")
    billing_postcode = models.CharField(max_length=10, blank=True,null=True, verbose_name="کد پستی")
    billing_country = models.CharField(max_length=200, choices=COUNTRIES, blank=True, null=True,verbose_name="کشور")
    company = models.ForeignKey(Company, related_name="companycontacts",  on_delete=models.SET_NULL,null=True, blank=True, verbose_name="شرکت")
    birthday=models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    account = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True, blank=True, related_name="account_contacts", verbose_name="مشتری مرتبط")

    def __str__(self):
        return self.first_name
    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jbirthday(self):
        return jalali_converter(self.birthday)
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