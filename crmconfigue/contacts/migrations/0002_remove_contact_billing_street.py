# Generated by Django 3.0.6 on 2021-04-29 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='billing_street',
        ),
    ]
