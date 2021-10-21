from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali
from datetime import timedelta, datetime, date
from django.utils import timezone 
from common.models import Company
from .models import Project
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from common.decorators import company_enrolled
from .forms import ProjectForm
# Create your views here.
class ProjectList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/projects/project.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproject.filter(archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context



class ProjectCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Project
    form_class=ProjectForm
    template_name="company/projects/project-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproject.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['project_manager'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['tags'].queryset = company.companytags.filter(company=company)
        context['company'] = company
        return context
    def form_valid(self, form, **kwargs):       
        form.instance.created_by = self.request.user
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        form.instance.company= company
        return super().form_valid(form, **kwargs)
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('project:project', kwargs={'slug': slug}, current_app='project')
class ProjectUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Project
    form_class=ProjectForm
    template_name="company/projects/project-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('project:project', kwargs={'slug': slug}, current_app='project')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproject.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['project_manager'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['tags'].queryset = company.companytags.filter(company=company)
        pk=self.kwargs.get('pk')
        return context


  
class ProjectDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Project
    template_name = "company/projects/project_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproject.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('project:project', kwargs={'slug': slug}, current_app='project')


