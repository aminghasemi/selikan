# Generated by Django 3.0.6 on 2021-05-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210429_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subject',
            field=models.CharField(blank=True, choices=[('جلسه', 'جلسه'), ('تماس', 'تماس'), ('ایمیل', 'ایمیل'), ('پیش\u200cفاکتور', 'پیش\u200cفاکتور'), ('فاکتور', 'فاکتور'), ('پیگیری', 'پیگیری'), ('قرارداد', 'قرارداد'), ('کاتالوگ', 'کاتالوگ'), ('پروپوزال', 'پروپوزال'), ('سایر', 'سایر')], max_length=50, null=True, verbose_name='موضوع'),
        ),
    ]
