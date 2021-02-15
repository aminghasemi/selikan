
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from django.urls import reverse
from cuser.middleware import CuserMiddleware
from .managers import  EnrolledManager
from datetime import timedelta
from common.utils import COUNTRIES, ROLES, INDCHOICES, PROVINCE
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "users/profile_pics"
    username = models.CharField(max_length=100, unique=True,verbose_name="نام کاربری")
    first_name = models.CharField(max_length=150, blank=True,verbose_name="نام")
    last_name = models.CharField(max_length=150, blank=True,verbose_name="نام خانوادگی")
    email = models.EmailField(max_length=255, unique=True,verbose_name="ایمیل")
    is_active = models.BooleanField(default=True,verbose_name="فعال")
    is_admin = models.BooleanField(default=False,verbose_name="ادمین")
    is_staff = models.BooleanField(default=False,verbose_name="کارمند")
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ عضویت")
    role = models.CharField(max_length=50, choices=ROLES,verbose_name="نقش")
    thumbnail = models.ImageField(upload_to="media",blank=True, null=True, verbose_name="تصویر کاربر")
    has_sales_access = models.BooleanField(default=False,verbose_name="دسترسی به فروش")
    has_marketing_access = models.BooleanField(default=False,verbose_name="دسترسی به بازاریابی")


    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-is_active"]



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]


    objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def jdate_joined(self):
        return jalali_converter(self.date_joined)        

    @property
    def get_app_name(self):
        if self.company:
            return self.company.sub_domain + "." + settings.APPLICATION_NAME
        else:
            return settings.APPLICATION_NAME

    def documents(self):
        return self.document_uploaded.all()

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_joined).humanize()

    def __str__(self):
        return self.email

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name




class Company(models.Model):
    file_prepend = "users/profile_pics"
    name = models.CharField(max_length=100, blank=True, null=True,verbose_name="نام شرکت")
    slug=models.SlugField(max_length=100,unique=True, verbose_name ="لینک شرکت")
    sub_domain = models.CharField(max_length=30,null=True, blank=True, verbose_name="آدرس زیر دامنه")
    user_limit = models.IntegerField(default=1,verbose_name="محدودیت کاربر")
    country = models.CharField(max_length=3, default="IR", choices=COUNTRIES, blank=True, null=True,verbose_name="کشور")
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='crm_creator', verbose_name="ایجادکننده شرکت")
    created_time=models.DateTimeField(auto_now_add=True, verbose_name ="تاریخ ایجاد")
    staff=models.ManyToManyField(User, through='Enrolled', related_name='companystaff')
    access_date=models.DateTimeField(auto_now_add=False, verbose_name='تاریخ اعتبار حساب')
    national_id = models.CharField(max_length=64,blank=True, verbose_name="کد‌/شناسه ملی")
    economic_id=models.CharField(max_length=64,blank=True, verbose_name="کد اقتصادی")
    email = models.EmailField(blank=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, null=True, verbose_name="شماره تماس موبایل")
    office_phone = models.CharField(max_length=20,blank=True, verbose_name="شماره تماس ثابت")
    fax = models.CharField(max_length=20,blank=True, verbose_name="شماره فکس ")
    industry = models.CharField(max_length=255, choices=INDCHOICES, blank=True, verbose_name="صنعت")
    billing_address_line = models.CharField(max_length=255, blank=True, verbose_name="آدرس")
    billing_street = models.CharField(max_length=55, blank=True, verbose_name="خیابان")
    billing_city = models.CharField( max_length=255, blank=True, verbose_name="شهر")
    billing_state = models.CharField(choices=PROVINCE, max_length=255, blank=True, verbose_name="استان")
    billing_postcode = models.CharField(max_length=10, blank=True, verbose_name="کد پستی")
    website = models.URLField(blank=True, verbose_name="وب‌سایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    logo = models.ImageField(upload_to="companies_logos",blank=True, null=True, verbose_name="لوگو شرکت")



    class Meta:
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت‌ها"

    def jcreated_time(self):
        return jalali_converter(self.created_time)  
    def jaccess_date(self):
        return jalali_converter(self.access_date) 
    def __str__(self):
        return self.name
    def is_special_company(self):
        if self.access_date > timezone.now():
            return True
        else:
            return False
    is_special_company.boolean = True
    is_special_company.short_description = "وضعیت اعتبارحساب"

class Address(models.Model):
    address_line = models.CharField( max_length=255, blank=True, null=True,verbose_name="آدرس")
    street = models.CharField( max_length=55, blank=True, null=True,verbose_name="خیابان")
    city = models.CharField( max_length=255, blank=True, null=True,verbose_name="شهر")
    state = models.CharField( max_length=255, blank=True, null=True,verbose_name="استان")
    postcode = models.CharField(
         max_length=64, blank=True, null=True ,verbose_name="کدپستی"
    )
    country = models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True ,verbose_name="کشور")

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"
    def __str__(self):
        return self.city if self.city else ""

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.get_country_display()
            else:
                address += self.get_country_display()
        return address


class Enrolled(models.Model):
    staff = models.ForeignKey(User, related_name='staff',on_delete=models.CASCADE,  null=True, blank=True,verbose_name="کارمند")
    company = models.ForeignKey(Company, on_delete=models.CASCADE , related_name='staff_enroll', null=True, blank=True, verbose_name="نام شرکت")
    date =models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")
    previous_attempts = models.IntegerField(default=0)
    objects = EnrolledManager()

    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"

    def __str__(self):
        return self.staff.get_full_name()

    def __unicode__(self):
        return u'{0}'.format(self.staff)

    def jdate(self):
        return jalali_converter(self.date)    

    @staticmethod
    def autocomplete_search_fields():
        return (
            "staff__user__last_name__icontains",
            "staff__user__first_name__icontains",)


class Product(models.Model):
    name=models.CharField( max_length=255, blank=True, null=True,verbose_name="نام محصول")
    code=models.CharField( max_length=255, blank=True, null=True,verbose_name="کد محصول")
    unit=models.CharField( max_length=255, blank=True, null=True,verbose_name="واحد اندازه‌گیری")
    price=models.FloatField(blank=True, null=True, verbose_name="قیمت واحد محصول")
    description=models.CharField( max_length=255, blank=True, null=True,verbose_name="توضیحات")
    created_by=models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='product_creator', verbose_name="ایجادکننده محصول")
    created_on=models.DateTimeField(auto_now_add=True, verbose_name ="تاریخ ایجاد")
    company=models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="companyproducts", null=True, blank=True, verbose_name="محصولات شرکت")
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def jdate(self):
        return jalali_converter(self.created_on)

    def __str__(self):
        return self.name

class Country(models.Model):
    name=models.CharField( max_length=255, blank=True, null=True,verbose_name="نام کشور")
    short_name=models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True,verbose_name="نام کوتاه کشور")
    created_by=models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='country_creator', verbose_name="ایجادکننده کشور")
    created_on=models.DateTimeField(auto_now_add=True, verbose_name ="تاریخ ایجاد")
    company=models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="companycountries", null=True, blank=True, verbose_name="کشورهای مرتبط شرکت")

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشورها"
    def jdate(self):
        return jalali_converter(self.created_on)

    def __str__(self):
        return self.name

class Province(models.Model):
    name=models.CharField( max_length=255, blank=True, null=True,verbose_name="نام کشور")
    short_name=models.CharField(max_length=3, choices=COUNTRIES, blank=True, null=True,verbose_name="نام کوتاه کشور")

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان‌ها"

    def __str__(self):
        return self.name