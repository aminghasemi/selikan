# Generated by Django 3.0.6 on 2021-02-13 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20210209_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='archive',
            field=models.BooleanField(default=False, verbose_name='بایگانی شود؟'),
        ),
    ]
