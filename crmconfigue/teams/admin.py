from django.contrib import admin
from .models import Teams
# Register your models here.

@admin.register(Teams)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on','created_by','company')
    search_fields = ('name','company')