# Generated by Django 3.0.6 on 2021-01-26 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import payment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0004_company_access_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال')),
                ('staff_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='قیمت هر کاربر')),
                ('monthly_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='حق اشتراک ماهیانه')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='تاریخ شروع')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='تاریخ پایان')),
            ],
            options={
                'verbose_name': 'پکیج\u200c',
                'verbose_name_plural': 'پکیج\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام')),
                ('company_name', models.CharField(max_length=64, verbose_name='نام شرکت')),
                ('phone_number', models.CharField(max_length=15, verbose_name='شماره تماس')),
                ('Address', models.CharField(max_length=250, verbose_name='آدرس')),
                ('zipcode', models.CharField(max_length=10, verbose_name='کدپستی')),
                ('national_number', models.CharField(max_length=15, verbose_name='شناسه ملی')),
                ('economic_number', models.CharField(max_length=15, verbose_name='کد اقتصادی')),
                ('email', models.CharField(max_length=25, verbose_name='ایمیل')),
            ],
            options={
                'verbose_name': 'فروشنده',
                'verbose_name_plural': 'فروشنده\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_number', models.IntegerField(verbose_name='تعداد کارمند')),
                ('month_number', models.IntegerField(verbose_name='تعداد ماه')),
                ('staff_unit', models.IntegerField(verbose_name='حق اشتراک به ازای هر کاربر')),
                ('month_unit', models.IntegerField(verbose_name='حق اشتراک به ازای هر ماه')),
                ('invoice_number', models.CharField(default=payment.models.increment_invoice_number, max_length=64, verbose_name='شماره فاکتور')),
                ('invoice_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ فاکتور')),
                ('status', models.CharField(choices=[('PAID', 'پرداخت شده'), ('NOT_PAID', 'پرداخت شده'), ('PENDING', 'در حال پرداخت'), ('EXPIRED', 'منقضی شده')], max_length=20, verbose_name='وضعیت')),
                ('gateway', models.CharField(choices=[('ZARRINPAL', 'زرین\u200cپال'), ('PAYIR', 'پی'), ('BEHPARDAKHT', 'به\u200cپرداخت ملت')], max_length=20, verbose_name='درگاه پرداخت')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, verbose_name='مبلغ فاکتور')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companybilling', to='common.Company', verbose_name='نام شرکت کاربر')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userbilling', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربر')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت\u200cها',
            },
        ),
    ]
