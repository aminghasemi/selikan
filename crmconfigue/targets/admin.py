from django.contrib import admin
from .models import Targetsubject, CompanyTargets, StaffTargets
# Register your models here.

@admin.register(CompanyTargets)
class CompanyTargetAdmin(admin.ModelAdmin):
    list_display = ('title','target_subject','company')
    search_fields = ('title','target_subject','company')

@admin.register(StaffTargets)
class StaffTargetsAdmin(admin.ModelAdmin):
    list_display = ('title','target_subject','company','staff')
    search_fields = ('title','target_subject','company')

@admin.register(Targetsubject)
class TargetsubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_title','company')
    search_fields = ('company',)