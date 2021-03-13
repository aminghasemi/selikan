import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from extensions.utils import jalali_converter

from common.models import User, Company, Country, Province
from common.utils import COUNTRIES, ROLES, INDCHOICES, PROVINCE, UNITS, CURRENCY
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from teams.models import Teams
from common import utils


class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)
    company = models.ForeignKey(Company, related_name= "companytags",  on_delete=models.SET_NULL,null=True,  blank=True, verbose_name="تگ‌ها")
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name= "تگ"
        verbose_name_plural="تگ‌ها"

class Account(models.Model):
    name = models.CharField(max_length=64, verbose_name="نام مشتری")
    national_id = models.CharField(max_length=64,blank=True,null=True, verbose_name="کد‌/شناسه ملی")
    economic_id=models.CharField(max_length=64,blank=True,null=True, verbose_name="کد اقتصادی")
    email = models.EmailField(blank=True,null=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20,null=True,blank=True, verbose_name="شماره تماس موبایل")
    whatsapp_phone = models.CharField(max_length=20,null=True, blank=True, verbose_name="شماره تماس واتساپ")
    office_phone = models.CharField(max_length=20,blank=True,null=True, verbose_name="شماره تماس ثابت")
    fax = models.CharField(max_length=20,blank=True,null=True, verbose_name="شماره فکس ")
    industry = models.CharField(max_length=255, choices=INDCHOICES, blank=True,null=True, verbose_name="صنعت")
    billing_address_line = models.CharField(max_length=255, blank=True,null=True, verbose_name="آدرس")
    billing_street = models.CharField(max_length=55, blank=True,null=True, verbose_name="خیابان")
    billing_city = models.CharField( max_length=255, blank=True,null=True, verbose_name="شهر")
    billing_state = models.CharField(max_length=200, choices=PROVINCE, blank=True, null=True,verbose_name="استان")
    billing_postcode = models.CharField(max_length=10, blank=True,null=True, verbose_name="کد پستی")
    billing_country = models.CharField(max_length=200, choices=COUNTRIES, blank=True, null=True,verbose_name="کشور")
    website = models.CharField(blank=True,null=True, verbose_name="وب‌سایت", max_length=200)
    description = models.TextField(blank=True,null=True, verbose_name="توضیحات")
    created_by = models.ForeignKey(User, related_name="account_created_by", on_delete=models.SET_NULL,null=True, verbose_name="ایجاد شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    tags = models.ForeignKey(Tags, blank=True, on_delete=models.SET_NULL,null=True, verbose_name="تگ‌ها")
    company = models.ForeignKey(Company, related_name= "companyaccounts",  on_delete=models.SET_NULL,null=True,  blank=True, verbose_name="کاربر سایت")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")

    def __str__(self):
        return self.name
    def jcreated_on(self):
        return jalali_converter(self.created_on)

    class Meta:
        verbose_name= "مشتری حقوقی"
        verbose_name_plural="مشتریان حقوقی"
        ordering = ["-created_on"]

    def get_complete_address(self):
        """Concatenates complete address."""
        address = ""
        add_to_address = [
            self.billing_street,
            self.billing_city,
            self.billing_state,
            self.billing_postcode,
            self.get_billing_country_display(),
        ]
        address = utils.append_str_to(address, *add_to_address)

        return address

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def contact_values(self):
        contacts = list(self.contacts.values_list("id", flat=True))
        return ",".join(str(contact) for contact in contacts)

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


class Email(models.Model):
    from_account = models.ForeignKey(
    Account, related_name="sent_email", on_delete=models.SET_NULL, null=True, verbose_name="از حساب")
    recipients = models.ManyToManyField("contacts.Contact", related_name="recieved_email", verbose_name="دریافت کنندگان")
    message_subject = models.TextField(null=True, verbose_name="موضوع ایمیل")
    message_body = models.TextField(null=True, verbose_name="متن ایمیل")
    timezone = models.CharField(max_length=100, default="UTC", verbose_name="منطقه زمانی")
    scheduled_date_time = models.DateTimeField(null=True, verbose_name="زمان برنامه ریزی شده")
    scheduled_later = models.BooleanField(default=False, verbose_name="بعدا ارسال شود")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    from_email = models.EmailField( verbose_name="از طریق ایمیل")
    rendered_message_body = models.TextField(null=True, verbose_name="متن ایمیل رندر شده")

    def __str__(self):
        return self.message_subject
    
    class Meta:
        verbose_name= "ایمیل‌ ارسالی /دریافتی"
        verbose_name_plural="ایمیل‌های ارسالی/دریافتی"

class EmailLog(models.Model):
    """ this model is used to track if the email is sent or not """

    email = models.ForeignKey(
        Email, related_name="email_log", on_delete=models.SET_NULL, null=True, verbose_name="ایمیل"
    )
    contact = models.ForeignKey(
        "contacts.Contact", related_name="contact_email_log", on_delete=models.SET_NULL, null=True, verbose_name="شخص"
    )
    is_sent = models.BooleanField(default=False, verbose_name="وضعیت ارسال")
    
    class Meta:
        verbose_name= "لاگ ایمیل"
        verbose_name_plural="لاگ‌های ایمیل‌ها"