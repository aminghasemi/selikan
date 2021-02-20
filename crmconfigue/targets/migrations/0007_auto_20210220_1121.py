# Generated by Django 3.0.6 on 2021-02-20 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0030_auto_20210218_2019'),
        ('targets', '0006_auto_20210214_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stafftargets',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target_staff', to='common.Enrolled', verbose_name='نام کارمند'),
        ),
    ]
