# Generated by Django 3.0.6 on 2021-01-24 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210116_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='access_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ اعتبار حساب'),
        ),
    ]
