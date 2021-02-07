# Generated by Django 3.0.6 on 2021-02-07 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('invoice', '0002_auto_20210202_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='teams',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_teams', to='teams.Teams', verbose_name='تیم'),
        ),
    ]
