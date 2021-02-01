from django.contrib import admin
from .models import Lead, LeadStatus, LeadSource
# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title','first_name', 'last_name','email','phone','company')
    search_fields = ('title','first_name','last_name', 'email', 'company')

@admin.register(LeadStatus)
class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ('LeadStatus_number','LeadStatus_title', 'company')
@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ('LeadSource_title', 'company')