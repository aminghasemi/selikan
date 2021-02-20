# Generated by Django 3.0.6 on 2021-02-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0030_auto_20210218_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True, verbose_name='قیمت واحد محصول'),
        ),
    ]
