from django.contrib import admin
from .models import Deal, Pipeline
# Register your models here.

@admin.register(Pipeline)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('pipeline_number','pipeline_title', 'company')
 
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title','pipeline_status', 'company','deal_amount')