# Generated by Django 3.0.6 on 2021-02-01 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='Address',
            field=models.CharField(default='ارومیه، خیام جنوبی، کوی ۲۲', max_length=250, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='company_name',
            field=models.CharField(default='سلیکان', max_length=64, verbose_name='نام شرکت'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.CharField(default='info@selikan.ir', max_length=25, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(default='سلیکان', max_length=64, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='phone_number',
            field=models.CharField(default='+4432259637', max_length=15, verbose_name='شماره تماس'),
        ),
    ]
