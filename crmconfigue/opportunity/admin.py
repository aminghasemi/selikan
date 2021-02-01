from django.contrib import admin
from .models import Opportunity, OpportunityStatus, OpportunitySource
# Register your models here.

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    search_fields = ('name', 'company')

@admin.register(OpportunityStatus)
class OpportunityStatusAdmin(admin.ModelAdmin):
    list_display = ('OpportunityStatus_number','OpportunityStatus_title', 'company')
@admin.register(OpportunitySource)
class OpportunitySourceAdmin(admin.ModelAdmin):
    list_display = ('OpportunitySource_title', 'company')