# Generated by Django 3.0.6 on 2021-02-07 10:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_auto_20210207_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='access_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 10, 10, 7, 15497, tzinfo=utc), verbose_name='تاریخ اعتبار حساب'),
        ),
        migrations.AlterField(
            model_name='company',
            name='sub_domain',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='آدرس زیر دامنه'),
        ),
    ]
