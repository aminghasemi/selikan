# Generated by Django 3.0.6 on 2021-02-18 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_auto_20210218_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
    ]
