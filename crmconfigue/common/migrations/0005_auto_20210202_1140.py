# Generated by Django 3.0.6 on 2021-02-02 08:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20210202_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='access_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 17, 8, 10, 47, 219017, tzinfo=utc), verbose_name='تاریخ اعتبار حساب'),
        ),
    ]
