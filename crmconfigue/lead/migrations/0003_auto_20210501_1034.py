# Generated by Django 3.0.6 on 2021-05-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_auto_20210331_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='contacts',
        ),
        migrations.AddField(
            model_name='lead',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='زمان پیگیری'),
        ),
    ]
