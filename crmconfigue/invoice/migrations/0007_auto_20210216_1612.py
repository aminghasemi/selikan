# Generated by Django 3.0.6 on 2021-02-16 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_auto_20210216_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='bargain',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='درصد تخفیف'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' درصد مالیات'),
        ),
    ]
