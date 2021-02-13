from django.contrib import admin
from .models import Doc
# Register your models here.
@admin.register(Doc)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title','description', 'company')