# Generated by Django 3.0.6 on 2021-03-30 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('accounts', '0002_auto_20210330_1929'),
        ('contacts', '0001_initial'),
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('status', models.CharField(choices=[('جدید', 'جدید'), ('در حال انجام', 'در حال انجام'), ('پایان یافته', 'پایان یافته')], max_length=50, verbose_name='وضعیت')),
                ('priority', models.CharField(choices=[('پایین', 'پایین'), ('معمولی', 'معمولی'), ('بالا', 'بالا')], max_length=50, verbose_name='تقدم')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='مهلت انجام')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('done_on', models.DateField(blank=True, null=True, verbose_name='تاریخ تکمیل')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts_tasks', to='accounts.Account', verbose_name='نام مشتری')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_tasks', to='common.Enrolled', verbose_name='محول شده به')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='companytask', to='common.Company', verbose_name='کاربر سایت')),
                ('contacts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts_tasks', to='contacts.Contact', verbose_name='نام شخص')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_created', to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط')),
                ('done_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_done_by', to='common.Enrolled', verbose_name='تکمیل\u200cشده توسط')),
                ('tags', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Tags', verbose_name='تگ\u200cها')),
                ('teams', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_teams', to='teams.Teams', verbose_name='تیم')),
            ],
            options={
                'verbose_name': 'کار',
                'verbose_name_plural': 'کارها',
                'ordering': ['-due_date'],
            },
        ),
    ]
