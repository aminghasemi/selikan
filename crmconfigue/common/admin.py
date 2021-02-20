from django.contrib import admin
from .models import Company, User, Address, Enrolled, Product, Country, Enroll_Invitation
# Register your models here.


class company_admin(admin.ModelAdmin):
    list_display= ('name','user_limit','creator','created_time')
    list_filter= ('name',)
    search_fields= ('name',)

admin.site.register(Company,company_admin)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'email')


@admin.register(Enroll_Invitation)
class Enroll_InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'company','created_by')
    search_fields = ('email', 'company','created_by')

@admin.register(Enrolled)
class EnrolledAdmin(admin.ModelAdmin):
    list_display= ('staff','company','date')
    list_filter = ('company', )
    search_fields = ( 'company', )
    autocomplete_lookup_fields = {
        'fk': ['company', ],
    }

@admin.register(Product)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'company')
    search_fields = ('name', 'code', 'price', 'company')

@admin.register(Country)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name','company')
    search_fields = ('name', 'short_name', 'company')