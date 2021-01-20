from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


from common.models import Company
from .models import Task
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from common.decorators import company_enrolled
from .forms import TaskForm
# Create your views here.

@login_required(login_url='login')
@company_enrolled
def TaskList(request, slug):
    template_name = 'company/task.html'
    company = get_object_or_404(Company, slug=slug)
    tasks = company.companytask.all()
    return render(request, template_name, {'company': company,
                                           'tasks': tasks,})

def TaskCreate(request, slug):
    company = get_object_or_404(Company, slug=slug)
    template_name="company/task-create-update.html"
    task_form = TaskForm(data=request.POST)
    if task_form.is_valid():
        new_task=task_form.save(commit=False)
        new_task.company= company
        new_task.save()
    return render(request, template_name, {'company':company, 'task_form':task_form, 'new_task': new_task})

@login_required(login_url='login')
@company_enrolled
class TaaskCreate(LoginRequiredMixin, CreateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name="company/task-create-update.html"
    success_url= reverse_lazy('task:task')
    def form_valid(company, form):
        form.instance.created_by = company
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name = "company/task-create-update.html"
    success_url= reverse_lazy('task:task')
class TaskDelete(LoginRequiredMixin, DeleteView):
    model=Task
    template_name = "company/task_confirm_delete.html"
    success_url= reverse_lazy('task:task')
