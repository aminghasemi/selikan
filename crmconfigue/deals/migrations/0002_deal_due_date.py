# Generated by Django 3.0.6 on 2021-04-30 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='زمان پیگیری'),
        ),
    ]
