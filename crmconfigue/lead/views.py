from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Lead, LeadStatus, LeadSource
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from .forms import LeadForm, LeadStatusForm, LeadSourceForm
# Create your views here.

class LeadStatusList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leadstatus.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadstatus.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class LeadStatusCreate(LoginRequiredMixin, CreateView):
    model=LeadStatus
    form_class=LeadStatusForm
    template_name="company/lead/leadstatus-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadstatus.all()
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
        return reverse_lazy('lead:leadstatus', kwargs={'slug': slug}, current_app='leads')

class LeadStatusUpdate(LoginRequiredMixin, UpdateView):
    model=LeadStatus
    form_class=LeadStatusForm
    template_name = "company/lead/leadstatus-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('lead:leadstatus', kwargs={'slug': slug}, current_app='leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadstatus.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class LeadStatusDelete(LoginRequiredMixin, DeleteView):
    model=LeadStatus
    template_name = "company/lead/leadstatus_confirm_delete.html"
    success_url= reverse_lazy('leads:leadstatus')
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
        return reverse_lazy('leads:leadstatus', kwargs={'slug': slug}, current_app='leads')


class LeadSourceList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leadsource.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsource.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class LeadSourceCreate(LoginRequiredMixin, CreateView):
    model=LeadSource
    form_class=LeadSourceForm
    template_name="company/lead/leadsource-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsource.all()
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
        return reverse_lazy('lead:leadsource', kwargs={'slug': slug}, current_app='leads')

class LeadSourceUpdate(LoginRequiredMixin, UpdateView):
    model=LeadSource
    form_class=LeadSourceForm
    template_name = "company/lead/leadsource-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('lead:leadsource', kwargs={'slug': slug}, current_app='leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsource.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class LeadSourceDelete(LoginRequiredMixin, DeleteView):
    model=LeadSource
    template_name = "company/lead/leadsource_confirm_delete.html"
    success_url= reverse_lazy('leads:leadsource')
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
        return reverse_lazy('leads:leadsource', kwargs={'slug': slug}, current_app='leads')



class LeadsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leads.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class LeadCreate(LoginRequiredMixin, CreateView):
    model=Lead
    form_class=LeadForm
    template_name="company/lead/lead-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['status'].queryset = LeadStatus.objects.filter(company=company)
        context['form'].fields['source'].queryset = LeadSource.objects.filter(company=company)
        context['form'].fields['contacts'].queryset = company.companycontacts.filter(company=company)
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
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
        return reverse_lazy('leads:leads', kwargs={'slug': slug}, current_app='leads')

class LeadUpdate(LoginRequiredMixin, UpdateView):
    model=Lead
    form_class= LeadForm
    template_name = "company/lead/lead-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('leads:leads', kwargs={'slug': slug}, current_app='leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['form'].fields['status'].queryset = LeadStatus.objects.filter(company=company)
        context['form'].fields['source'].queryset = LeadSource.objects.filter(company=company)
        context['form'].fields['contacts'].queryset = company.companycontacts.filter(company=company)
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['tags'].queryset = company.companytags.filter(company=company)
        context['company'] = company
        return context
class LeadDelete(LoginRequiredMixin, DeleteView):
    model=Lead
    template_name = "company/lead/lead_confirm_delete.html"
    success_url= reverse_lazy('leads:leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('leads:leads', kwargs={'slug': slug}, current_app='leads')