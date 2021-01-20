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


class TaskList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/task.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class TaskCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name="company/task-create-update.html"
    success_url= reverse_lazy('task:task')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def form_valid(self, company, form):
        form.instance.created_by = self.request.user
        form.instance.company= company
        return super().form_valid(form)

class TaskUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Task
    fields=["title", "status", "priority","due_date", "account", "contacts", "assigned_to"]
    template_name = "company/task-create-update.html"
    success_url= reverse_lazy('task:task')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


  
class TaskDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Task
    template_name = "company/task_confirm_delete.html"
    success_url= reverse_lazy('task:task')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context







#@login_required(login_url='login')
#@company_enrolled
#def TaaskList(request, slug):
#    template_name = 'company/task.html'
#    company = get_object_or_404(Company, slug=slug)
#    tasks = company.companytask.all()
#    return render(request, template_name, {'company': company,'tasks': tasks,})


#@login_required(login_url='login')
#@company_enrolled
#def TaaskCreate(request, slug):
#    company = get_object_or_404(Company, slug=slug)
#    template_name="company/task-create-update.html"
#   task_form = TaskForm(request.POST or None)
#   task_form.instance.company= company
#   success_url= reverse_lazy('task:task')
#   if task_form.is_valid():
#       task_form.save()
#        new_task=task_form.save(commit=False)
#        new_task.company= company
 #       new_task.save()
#    return render(request, template_name, {'company':company, 'task_form':task_form})