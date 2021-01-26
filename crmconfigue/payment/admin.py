from django.contrib import admin
from .models import Packages, Billing, Seller
# Register your models here.

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('name','staff_amount', 'monthly_amount')

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('amount','invoice_number','invoice_date', 'status', 'company','user', 'gateway')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name','company_name')
