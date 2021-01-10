from django.contrib import admin
from .models import Company, User, Address
# Register your models here.


class company_admin(admin.ModelAdmin):
    list_display= ('name','sub_domain','user_limit','address')
    list_filter= ('name',)
    search_fields= ('name','sub_domain')

admin.site.register(Company,company_admin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'company')
    search_fields = ('username', 'email')
