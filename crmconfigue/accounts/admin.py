from django.contrib import admin
from .models import Account, Tags, Email, EmailLog
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'phone','company')
    search_fields = ('name','email', 'phone','company')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('from_account', 'message_subject', 'from_email')
    search_fields = ('from_account', 'message_subject', 'from_email')

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact', 'is_sent')
    search_fields = ('email', 'contact', 'is_sent')