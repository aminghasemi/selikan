from django.contrib import admin
from .models import Dealreport
# Register your models here.

@admin.register(Dealreport)
class DealreportAdmin(admin.ModelAdmin):
    list_display = ('title','pipeline_status','company')
    search_fields = ('title','company')
    