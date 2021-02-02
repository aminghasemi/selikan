import arrow
from django.db import models
from common.models import User, Company, Product
from accounts.models import Account
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse
from extensions.utils import jalali_converter

class Invoice(models.Model):

    STATUS_CHOICES = (
        ("پیش‌فاکتور", "پیش‌فاکتور"),
        ("فاکتور","فاکتور"),
        ("کنسل شده", "کنسل شده"),
    )

    title = models.CharField( max_length=200, verbose_name="عنوان")
    invoice_number=models.CharField(max_length=25, verbose_name="شماره فاکتور")
    status = models.CharField( max_length=50, choices=STATUS_CHOICES, verbose_name="وضعیت")
    date = models.DateField(null=True,blank=True, verbose_name="تاریخ فاکتور")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    account = models.ForeignKey(Account,null=True, related_name="accounts_invoices",blank=True,on_delete=models.SET_NULL, verbose_name="نام مشتری")
    created_by = models.ForeignKey(User,related_name="invoice_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    teams = models.ForeignKey(Teams,null=True,blank=True, related_name="invoice_teams",on_delete=models.SET_NULL, verbose_name="تیم")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name='companyinvoice', blank=True, verbose_name="کاربر سایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    done_on=models.DateField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    tax=models.IntegerField(null=True, blank=True, verbose_name="مالیات")
    total_amount=models.FloatField(null=True, blank=True, verbose_name="جمع مبلغ فاکتور")
    def __str__(self):
        return self.title

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdate(self):
        return jalali_converter(self.date)

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
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"


class Inovice_item(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name='invoice_item_product', blank=True, verbose_name="آیتم فاکتور")
    amount=models.IntegerField(null=True, blank=True, verbose_name="تعداد")
    total_item_amount=models.FloatField(null=True, blank=True, verbose_name="مجموع")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    created_by = models.ForeignKey(User,related_name="invoice_item_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL,null=True, related_name='Invoiceitem', blank=True, verbose_name="فاکتور")

    def save(self):
        self.total_item_amount= (self.amount*self.product_name.price)
        return super(Inovice_item, self).save()
    class Meta:
        verbose_name = "آیتم فاکتور"
        verbose_name_plural = "آیتم‌های فاکتور"