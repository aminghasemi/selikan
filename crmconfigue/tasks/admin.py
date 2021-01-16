from django.contrib import admin
from .models import Task
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','status', 'priority','due_date','company')
    search_fields = ('title','status', 'priority','company')
    