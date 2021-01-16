from django.contrib import admin
from .models import Opportunity
# Register your models here.

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('name','stage', 'company')
    search_fields = ('name','stage', 'company')
    