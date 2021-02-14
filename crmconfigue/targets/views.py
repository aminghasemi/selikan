from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Targetsubject, CompanyTargets, StaffTargets
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from .forms import CompanyTargetsForm, StaffTargetsForm, TargetsubjectForm
# Create your views here.

class TargetsubjectList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/targets/targetsubjectlist.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargetsubjects.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class TargetsubjectCreate(LoginRequiredMixin, CreateView):
    model=Targetsubject
    form_class=TargetsubjectForm
    template_name="company/targets/targetsubject-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargetsubjects.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
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
        return reverse_lazy('targets:targetsubjectlist', kwargs={'slug': slug}, current_app='targets')

class TargetsubjectUpdate(LoginRequiredMixin, UpdateView):
    model=Targetsubject
    form_class=TargetsubjectForm
    template_name = "company/targets/targetsubject-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:targetsubjectlist', kwargs={'slug': slug}, current_app='targets')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargetsubjects.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class TargetsubjectDelete(LoginRequiredMixin, DeleteView):
    model=Targetsubject
    template_name = "company/targets/targetsubject_confirm_delete.html"
    success_url= reverse_lazy('targets:targetsubjectlist')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:targetsubjectlist', kwargs={'slug': slug}, current_app='targets')



class CompanyTargetsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/targets/companytargets.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_company.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class CompanyTargetsCreate(LoginRequiredMixin, CreateView):
    model=CompanyTargets
    form_class=CompanyTargetsForm
    template_name="company/targets/companytargets-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_company.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
    #    context['form'].fields['subject'].queryset = Targetsubject.objects.filter(company=company)
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
        return reverse_lazy('targets:companytargets', kwargs={'slug': slug}, current_app='targets')

class CompanyTargetsUpdate(LoginRequiredMixin, UpdateView):
    model=CompanyTargets
    form_class= CompanyTargetsForm
    template_name = "company/targets/companytargets-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:companytargets', kwargs={'slug': slug}, current_app='targets')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_company.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
     #   context['form'].fields['subject'].queryset = Targetsubject.objects.filter(company=company)
        context['company'] = company
        return context
class CompanyTargetsDelete(LoginRequiredMixin, DeleteView):
    model=CompanyTargets
    template_name = "company/targets/companytargets_confirm_delete.html"
    success_url= reverse_lazy('targets:companytargets')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_company.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:companytargets', kwargs={'slug': slug}, current_app='targets')


class StaffTargetsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/targets/stafftargets.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_staff.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class StaffTargetsCreate(LoginRequiredMixin, CreateView):
    model=StaffTargets
    form_class=StaffTargetsForm
    template_name="company/targets/stafftargets-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_staff.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
    #    context['form'].fields['subject'].queryset = Targetsubject.objects.filter(company=company)
        context['form'].fields['staff'].queryset = company.staff_enroll.filter(company=company)
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
        return reverse_lazy('targets:stafftargets', kwargs={'slug': slug}, current_app='targets')

class StaffTargetsUpdate(LoginRequiredMixin, UpdateView):
    model=StaffTargets
    form_class= StaffTargetsForm
    template_name = "company/targets/stafftargets-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:stafftargets', kwargs={'slug': slug}, current_app='targets')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_staff.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
     #   context['form'].fields['subject'].queryset = Targetsubject.objects.filter(company=company)
        context['form'].fields['staff'].queryset = company.staff_enroll.filter(company=company)
        context['company'] = company
        return context
class StaffTargetsDelete(LoginRequiredMixin, DeleteView):
    model=StaffTargets
    template_name = "company/targets/stafftargets_confirm_delete.html"
    success_url= reverse_lazy('targets:stafftargets')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytargets_staff.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('targets:stafftargets', kwargs={'slug': slug}, current_app='targets')