from django.contrib import admin
from .models import Invoice, Invoice_item
# Register your models here.

@admin.register(Invoice)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('title','invoice_number', 'company')

@admin.register(Invoice_item)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('product_name','amount', 'total_item_amount')