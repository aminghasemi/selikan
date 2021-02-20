import arrow
from django.db import models
from common.models import User, Company, Product
from accounts.models import Account
from contacts.models import Contact
from deals.models import Deal
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
    PAID_CHOICES = (
        ("نقدی", "نقدی"),
        ("اعتباری","اعتباری"),
        ("غیر نقدی", "غیر نقدی"),
        ("چک", "چک"),
    )
    invoice_number=models.CharField(max_length=25, verbose_name="شماره فاکتور")
    status = models.CharField( max_length=50, choices=STATUS_CHOICES,null=True,blank=True, verbose_name="وضعیت")
    paid_status = models.CharField( max_length=50, choices=PAID_CHOICES,null=True,blank=True, verbose_name="نحوه پرداخت")
    date = models.DateField(null=True,blank=True, verbose_name="تاریخ تنظیم")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    account = models.ForeignKey(Account,null=True, related_name="invoice_account",blank=True,on_delete=models.SET_NULL, verbose_name="نام مشتری")
    created_by = models.ForeignKey(User,related_name="invoice_created_by",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    deal = models.ForeignKey(Deal,null=True,blank=True, related_name="invoice_deal",on_delete=models.SET_NULL, verbose_name="معامله")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name='companyinvoice', blank=True, verbose_name="کاربر سایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    tax=models.DecimalField(default=0,decimal_places=0, max_digits=20, null=True, blank=True, verbose_name=" درصد مالیات")
    bargain=models.DecimalField(default=0,decimal_places=0, max_digits=20, null=True, blank=True, verbose_name="درصد تخفیف")
    total_amount=models.DecimalField(default=0,decimal_places=0, max_digits=20, blank=True, verbose_name="جمع مبلغ فاکتور")
    expire_date=models.DateField(null=True,blank=True, verbose_name="تاریخ اعتبار ")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    total_bargain=models.DecimalField(decimal_places=0, max_digits=20 ,null=True, blank=True, verbose_name=" مبلغ تخفیف")
    total_tax=models.DecimalField(decimal_places=0, max_digits=20 ,null=True, blank=True, verbose_name=" مبلغ مالیات")
    final_total_amount=models.DecimalField(decimal_places=0, max_digits=20 ,null=True, blank=True, verbose_name="جمع نهایی مبلغ فاکتور")
    
    def save(self):
        self.total_bargain= ((self.total_amount)*(self.bargain/100))
        self.total_tax= ((self.total_amount)*(self.tax/100))
        self.final_total_amount=(self.total_amount)+(self.total_tax)-(self.total_bargain)
        return super(Invoice, self).save()

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


class Invoice_item(models.Model):
    product_name=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, related_name='invoice_item_product', blank=True, verbose_name="آیتم فاکتور")
    amount=models.IntegerField(null=True, blank=True, verbose_name="تعداد")
    total_item_amount=models.DecimalField(decimal_places=0, max_digits=20 ,null=True, blank=True, verbose_name="مجموع")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    created_by = models.ForeignKey(User,related_name="invoice_item_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL,null=True, related_name='Invoiceitem', blank=True, verbose_name="فاکتور")

    def save(self):
        self.total_item_amount= (self.amount*self.product_name.price)
        return super(Invoice_item, self).save()
    class Meta:
        verbose_name = "آیتم فاکتور"
        verbose_name_plural = "آیتم‌های فاکتور"