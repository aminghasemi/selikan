from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Task
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class TaskList(LoginRequiredMixin,ListView):
        queryset= Task.objects.all()
        template_name="company/task.html"
class TaskCreate(LoginRequiredMixin, CreateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name="company/account-create-update.html"
    success_url= reverse_lazy('task:task')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name = "company/account-create-update.html"
    success_url= reverse_lazy('task:task')
class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    template_name = "company/account_confirm_delete.html"
    success_url= reverse_lazy('task:task')
