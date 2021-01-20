# Generated by Django 3.0.6 on 2021-01-19 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20210116_1353'),
        ('accounts', '0003_auto_20210116_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companyaccounts', to='common.Company', verbose_name='کاربر سایت'),
        ),
    ]
