# Generated by Django 3.0.6 on 2021-02-02 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20210202_1143'),
        ('contacts', '0002_contact_birthday'),
        ('accounts', '0002_auto_20210201_1854'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('tasks', '0004_auto_20210202_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts_tasks', to='accounts.Account', verbose_name='نام مشتری'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_tasks', to=settings.AUTH_USER_MODEL, verbose_name='محول شده به'),
        ),
        migrations.AlterField(
            model_name='task',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companytask', to='common.Company', verbose_name='کاربر سایت'),
        ),
        migrations.AlterField(
            model_name='task',
            name='contacts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts_tasks', to='contacts.Contact', verbose_name='نام شخص'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_created', to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط'),
        ),
        migrations.AlterField(
            model_name='task',
            name='done_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_done_by', to=settings.AUTH_USER_MODEL, verbose_name='تکمیل\u200cشده توسط'),
        ),
        migrations.AlterField(
            model_name='task',
            name='teams',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_teams', to='teams.Teams', verbose_name='تیم'),
        ),
    ]
