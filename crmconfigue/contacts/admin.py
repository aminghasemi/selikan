from django.contrib import admin
from .models import Contact
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name','email','phone','company')
    search_fields = ('first_name','last_name', 'email', 'company')