# Generated by Django 3.0.6 on 2021-02-07 07:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20210202_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='access_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 22, 7, 1, 3, 834022, tzinfo=utc), verbose_name='تاریخ اعتبار حساب'),
        ),
    ]
