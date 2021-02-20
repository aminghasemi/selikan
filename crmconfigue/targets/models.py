from django.db import models
from common.models import User, Company, Enrolled
from extensions.utils import jalali_converter



class Targetsubject(models.Model):
    
    subject_title = models.CharField(max_length=128, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="targetsubject_created_by", on_delete=models.SET_NULL, null=True,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companytargetsubjects", verbose_name="کاربر سایت")

    class Meta:
        verbose_name = " موضوع هدف"
        verbose_name_plural = "موضوعات  اهداف"
    def __str__(self):
        return self.subject_title

# Create your models here.
class CompanyTargets(models.Model):
    SUBJECT_CHOICES = (
        ("معاملات", "معاملات"),
        ("سرنخ‌ها", "سرنخ‌ها"),
        ("وظایف", "وظایف"),
        ("فرصت‌ها", "فرصت‌ها"),
    )

    title = models.CharField(max_length=64, verbose_name="عنوان")
    target_subject=models.CharField( max_length=100,null=True, choices=SUBJECT_CHOICES, verbose_name="موضوع")
    subject = models.ForeignKey(Targetsubject,null=True,blank=True, related_name="companytargets_subject", on_delete=models.CASCADE, verbose_name="موضوع")
    target=  models.IntegerField(blank=True, null=True, verbose_name="تعداد تارگت")
    current=  models.IntegerField(default=0,null=True,blank=True, verbose_name="تعداد کنونی")
    start_date=models.DateField(null=True,blank=True, verbose_name="تاریخ شروع")
    end_date=models.DateField(null=True,blank=True, verbose_name="تاریخ پایان")
    created_by = models.ForeignKey(User, related_name="company_target_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companytargets_company",  blank=True, verbose_name="شرکت")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")

    class Meta:
        verbose_name = "هدف شرکت"
        verbose_name_plural = "اهداف شرکت"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
    def jstart_date(self):
        return jalali_converter(self.start_date)
    def jend_date(self):
        return jalali_converter(self.end_date)


class StaffTargets(models.Model):
    SUBJECT_CHOICES = (
        ("معاملات", "معاملات"),
        ("سرنخ‌ها", "سرنخ‌ها"),
        ("وظایف", "وظایف"),
        ("فرصت‌ها", "فرصت‌ها"),
    )

    title = models.CharField(max_length=64, verbose_name="عنوان")
    target_subject=models.CharField( max_length=100, null=True, choices=SUBJECT_CHOICES, verbose_name="موضوع")
    subject = models.ForeignKey(Targetsubject,null=True,blank=True, related_name="stafftargets_subject", on_delete=models.CASCADE, verbose_name="موضوع")
    target=  models.IntegerField(blank=True, null=True, verbose_name="تعداد تارگت")
    current=  models.IntegerField(default=0,null=True,blank=True, verbose_name="تعداد کنونی")
    start_date=models.DateField(null=True,blank=True, verbose_name="تاریخ شروع")
    end_date=models.DateField(null=True,blank=True, verbose_name="تاریخ پایان")
    created_by = models.ForeignKey(User, related_name="staff_target_created_by", on_delete=models.CASCADE, verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name="companytargets_staff",  blank=True, verbose_name="شرکت")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    staff = models.ForeignKey(Enrolled,blank=True,null=True, related_name="target_staff",on_delete=models.SET_NULL, verbose_name="نام کارمند")
    class Meta:
        verbose_name = "هدف کارمند"
        verbose_name_plural = "اهداف کارمندان"
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
    def jstart_date(self):
        return jalali_converter(self.start_date)
    def jend_date(self):
        return jalali_converter(self.end_date)