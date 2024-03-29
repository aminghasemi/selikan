from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from itertools import chain
from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Lead, LeadStatus, LeadSource
from common.mixins import EnrollMixin, SuperUserAccessMixin,SpecialCompanyMixin, CreatorAccessMixin
from .forms import LeadForm, LeadStatusForm, LeadSourceForm
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
# Create your views here.

class LeadStatusList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
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

class LeadStatusCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
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
        return reverse_lazy('leads:leadstatus', kwargs={'slug': slug}, current_app='leads')

class LeadStatusUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=LeadStatus
    form_class=LeadStatusForm
    template_name = "company/lead/leadstatus-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('leads:leadstatus', kwargs={'slug': slug}, current_app='leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadstatus.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class LeadStatusDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
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


class LeadSourceList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
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

class LeadSourceCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
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
        return reverse_lazy('leads:leadsource', kwargs={'slug': slug}, current_app='leads')

class LeadSourceUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=LeadSource
    form_class=LeadSourceForm
    template_name = "company/lead/leadsource-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('leads:leadsource', kwargs={'slug': slug}, current_app='leads')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsource.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class LeadSourceDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
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



class LeadsList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leads.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.filter(archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


class LeadsListAll(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
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
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context

class LeadsList_today(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leads.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.filter(due_date=datetime.today(), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context
class LeadsList_3days(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leads.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.filter(due_date__lte=datetime.today()+timedelta(days=3), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context
class LeadsList_10days(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/lead/leads.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleads.filter(due_date__lte=datetime.today()+timedelta(days=10), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context




class LeadCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=Lead
    form_class=LeadForm
    template_name="company/lead/lead-create.html"
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

class LeadUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Lead
    form_class= LeadForm
    template_name = "company/lead/lead-update.html"
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
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['tags'].queryset = company.companytags.filter(company=company)
        context['company'] = company
        pk=self.kwargs.get('pk')
        context['docs']=company.companydocs.filter(leads_id=pk)
        return context
class LeadDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
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