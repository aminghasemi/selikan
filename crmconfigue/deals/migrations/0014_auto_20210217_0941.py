# Generated by Django 3.0.6 on 2021-02-17 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0013_auto_20210217_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='deal_amount',
            field=models.IntegerField(blank=True, null=True, verbose_name='مبلغ معامله'),
        ),
    ]
