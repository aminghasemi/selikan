# Generated by Django 3.0.6 on 2021-02-18 15:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0023_auto_20210218_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='billing_address_line',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='company',
            name='staff',
            field=models.ManyToManyField(blank=True, related_name='companystaff', through='common.Enrolled', to=settings.AUTH_USER_MODEL),
        ),
    ]
