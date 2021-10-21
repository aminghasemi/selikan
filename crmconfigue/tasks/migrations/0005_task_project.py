# Generated by Django 3.0.6 on 2021-08-18 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('tasks', '0004_auto_20210818_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projecttask', to='projects.Project', verbose_name='پروژه'),
        ),
    ]
