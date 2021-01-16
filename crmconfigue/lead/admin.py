from django.contrib import admin
from .models import Lead
# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title','first_name', 'last_name','status','email','phone','company')
    search_fields = ('title','first_name','last_name', 'email', 'company')
    