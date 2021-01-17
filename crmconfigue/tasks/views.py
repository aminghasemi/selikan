from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


from common.models import Company
from .models import Task
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from common.decorators import company_enrolled
# Create your views here.

@login_required(login_url='login')
@company_enrolled
def TaskList(request, slug):
    template_name = 'company/task.html'
    company = get_object_or_404(Company, slug=slug)
    tasks = company.companytask.all()
    return render(request, template_name, {'company': company,
                                           'tasks': tasks,})





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
