# Generated by Django 3.0.6 on 2021-02-09 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20210207_1343'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20210209_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='billing_state',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Province', verbose_name='استان'),
        ),
        migrations.AlterField(
            model_name='account',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companyaccounts', to='common.Company', verbose_name='کاربر سایت'),
        ),
        migrations.AlterField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_created_by', to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط'),
        ),
        migrations.AlterField(
            model_name='account',
            name='tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Tags', verbose_name='تگ\u200cها'),
        ),
    ]
