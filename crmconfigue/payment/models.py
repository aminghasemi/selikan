from django.db import models
from extensions.utils import jalali_converter
from common.models import Company, User
from django.db.models import F
# Create your models here.

BILLING_STATUS = (
    ("PAID", "پرداخت شده"),
    ("NOT_PAID", "پرداخت نشده"),
    ("PENDING", "در حال پرداخت"),
    ("EXPIRED", "منقضی شده"),
)
PAYMENT_GATEWAYS = (
    ("ZARRINPAL", "زرین‌پال"),
    ("PAYIR", "پی"),
    ("BEHPARDAKHT", "به‌پرداخت ملت"),
)


class Packages(models.Model):
    name = models.CharField( max_length=64, verbose_name="عنوان")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    staff_amount=models.IntegerField(  blank=True, null=True, verbose_name="قیمت هر کاربر")
    monthly_amount = models.IntegerField(  blank=True, null=True, verbose_name="حق اشتراک ماهیانه")
    start_date=models.DateField(blank=True, null=True, verbose_name="تاریخ شروع")
    end_date=models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")

    def __str__(self):
        return self.name
    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jstart_date(self):
        return jalali_converter(self.start_date)
    def jend_date(self):
        return jalali_converter(self.end_date)

    class Meta:
        verbose_name= "پکیج‌"
        verbose_name_plural= "پکیج‌ها"


def increment_invoice_number():
    last_invoice = Billing.objects.all().order_by('id').last()
    if not last_invoice:
        return '1'
    invoice_no = last_invoice.invoice_number
    invoice_int = int(invoice_no)
    width = 7
    new_invoice_int = invoice_int + 1
    formatted = str(new_invoice_int)
    new_invoice_no = str(formatted)
    return new_invoice_no 
class Billing(models.Model):
    staff_number=models.IntegerField( verbose_name="تعداد کارمند")
    month_number=models.IntegerField( verbose_name="تعداد ماه")
    staff_unit=models.IntegerField(verbose_name="حق اشتراک به ازای هر کاربر")
    month_unit=models.IntegerField(verbose_name="حق اشتراک به ازای هر ماه")
    invoice_number=models.CharField(max_length=64, default = increment_invoice_number, verbose_name="شماره فاکتور")
    invoice_date=models.DateTimeField(auto_now_add=True, verbose_name="تاریخ فاکتور")
    status=models.CharField(max_length=20, choices=BILLING_STATUS, verbose_name="وضعیت")
    gateway=models.CharField(max_length=20, choices=PAYMENT_GATEWAYS, verbose_name="درگاه پرداخت")
    company=models.ForeignKey(Company,related_name="companybilling", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نام شرکت کاربر")
    amount=models.IntegerField( blank=True, verbose_name="مبلغ فاکتور")
    user=models.ForeignKey(User, related_name="userbilling", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نام کاربر")
    def save(self):
        self.amount= (self.staff_number*self.staff_unit*self.month_number)
        return super(Billing, self).save()
    def jinvoice_date(self):
        return jalali_converter(self.invoice_date)      
    class Meta:
        verbose_name= "پرداخت"
        verbose_name_plural= "پرداخت‌ها"
class Seller(models.Model):
    name = models.CharField( max_length=64, verbose_name="نام")
    company_name = models.CharField( max_length=64, verbose_name="نام شرکت")
    phone_number= models.CharField(max_length = 15, verbose_name= "شماره تماس")
    Address=models.CharField(max_length=250, verbose_name="آدرس")
    zipcode=models.CharField(max_length=10, verbose_name="کدپستی")
    national_number= models.CharField(max_length=15, verbose_name="شناسه ملی")
    economic_number= models.CharField(max_length=15, verbose_name="کد اقتصادی")
    email=models.CharField(max_length=25, verbose_name="ایمیل")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name= "فروشنده"
        verbose_name_plural= "فروشنده‌ها"