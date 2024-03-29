import arrow
from django.db import models
from common.models import User, Company, Enrolled
from accounts.models import Account, Tags
from contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from teams.models import Teams
from django.urls import reverse
from extensions.utils import jalali_converter
from jalali_date import datetime2jalali, date2jalali
from django_jalali.db import models as jmodels
from projects.models import Project

class TaskSubject(models.Model):
    tasksubject_title = models.CharField(max_length=64, verbose_name="عنوان")
    created_by = models.ForeignKey(User, related_name="tasksubject_created_by", on_delete=models.CASCADE,  verbose_name="ساخته شده توسط")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="companytasksubject", verbose_name="کاربر سایت")
    class Meta:
        verbose_name = "موضوع"
        verbose_name_plural = "موضوعات"
    def __str__(self):
        return self.tasksubject_title


class Task(models.Model):

    STATUS_CHOICES = (
        ("جدید", "جدید"),
        ("در حال انجام", "در حال انجام"),
        ("پایان یافته", "پایان یافته"),
    )

    PRIORITY_CHOICES = (("پایین", "پایین"), ("معمولی", "معمولی"), ("بالا", "بالا"))


    SUBJECT_CHOICES = (
        ("جلسه", "جلسه"),
        ("تماس", "تماس"),
        ("ایمیل", "ایمیل"),
        ("پیش‌فاکتور", "پیش‌فاکتور"),
        ("فاکتور", "فاکتور"),
        ("پیگیری", "پیگیری"),
        ("قرارداد", "قرارداد"),
        ("کاتالوگ", "کاتالوگ"),
        ("پروپوزال", "پروپوزال"),
        ("سایر", "سایر"),

    )


    title = models.CharField( max_length=200,null=True,blank=True, verbose_name="عنوان")
    status = models.CharField( max_length=50,null=True,blank=True, choices=STATUS_CHOICES, verbose_name="وضعیت")
    priority = models.CharField( max_length=50,null=True,blank=True, choices=PRIORITY_CHOICES, verbose_name="تقدم")
    subject = models.CharField( max_length=50,null=True,blank=True, choices=SUBJECT_CHOICES, verbose_name="موضوع کار")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL,null=True, related_name='projecttask', blank=True, verbose_name="پروژه")
    tasksubject = models.ForeignKey(TaskSubject, on_delete=models.SET_NULL,null=True, related_name='tasksubject', blank=True, verbose_name="موضوع")
    due_date = models.DateField(null=True,blank=True, verbose_name="مهلت انجام")
    created_on = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ ایجاد")
    account = models.ForeignKey(Account,null=True, related_name="accounts_tasks",blank=True,on_delete=models.SET_NULL, verbose_name="نام مشتری")
    contacts = models.ForeignKey(Contact,blank=True,null=True, related_name="contacts_tasks",on_delete=models.SET_NULL, verbose_name="نام شخص")
    assigned_to = models.ForeignKey(Enrolled,blank=True,null=True, related_name="users_tasks",on_delete=models.SET_NULL, verbose_name="محول شده به")
    created_by = models.ForeignKey(User,related_name="task_created",null=True,blank=True,on_delete=models.SET_NULL, verbose_name="ایجاد شده توسط")
    teams = models.ForeignKey(Teams,null=True,blank=True, related_name="tasks_teams",on_delete=models.SET_NULL, verbose_name="تیم")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL,null=True, related_name='companytask', blank=True, verbose_name="کاربر سایت")
    done_by = models.ForeignKey(Enrolled, null=True,related_name="task_done_by", on_delete=models.SET_NULL, blank=True, verbose_name="تکمیل‌شده توسط")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    done_on=models.DateField(null=True, blank=True, verbose_name="تاریخ تکمیل")
    archive = models.BooleanField(default=False, verbose_name="بایگانی شود؟")
    tags = models.ForeignKey(Tags, blank=True, on_delete=models.SET_NULL, null=True, verbose_name="تگ‌ها")

    def __str__(self):
        return (self.title)

    def jcreated_on(self):
        return jalali_converter(self.created_on)
    def jdone_on(self):
        return jalali_converter(self.done_on)
    def jdue_date(self):
        return jalali_converter(self.due_date)
    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    class Meta:
        ordering = ["-due_date"]
        verbose_name = "کار"
        verbose_name_plural = "کارها"
