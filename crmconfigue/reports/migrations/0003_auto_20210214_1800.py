# Generated by Django 3.0.6 on 2021-02-14 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_auto_20210211_1554'),
        ('deals', '0012_auto_20210213_1529'),
        ('reports', '0002_auto_20210214_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealreport',
            name='pipeline_status',
        ),
        migrations.AddField(
            model_name='dealreport',
            name='pipeline_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportpipeline', to='deals.Pipeline', verbose_name='مرحله فروش'),
        ),
        migrations.RemoveField(
            model_name='dealreport',
            name='product',
        ),
        migrations.AddField(
            model_name='dealreport',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_dealproducts', to='common.Product', verbose_name='محصول'),
        ),
    ]
