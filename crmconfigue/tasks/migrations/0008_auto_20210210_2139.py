# Generated by Django 3.0.6 on 2021-02-10 18:09

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20210210_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='مهلت انجام'),
        ),
    ]
