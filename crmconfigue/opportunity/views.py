from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from itertools import chain
from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Opportunity, OpportunityStatus, OpportunitySource
from common.mixins import EnrollMixin, SuperUserAccessMixin, SpecialCompanyMixin, CreatorAccessMixin
from .forms import OpportunityForm, OpportunityStatusForm, OpportunitySourceForm
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
# Create your views here.


class OpportunityStatusList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunitystatus.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityStatusCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=OpportunityStatus
    form_class=OpportunityStatusForm
    template_name="company/opportunity/opportunitystatus-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
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
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')

class OpportunityStatusUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=OpportunityStatus
    form_class=OpportunityStatusForm
    template_name = "company/opportunity/opportunitystatus-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class OpportunityStatusDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=OpportunityStatus
    template_name = "company/opportunity/opportunitystatus_confirm_delete.html"
    success_url= reverse_lazy('opportunity:opportunitystatus')
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
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')


class OpportunitySourceList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunitysource.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunitySourceCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=OpportunitySource
    form_class=OpportunitySourceForm
    template_name="company/opportunity/opportunitysource-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
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
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')

class OpportunitySourceUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=OpportunitySource
    form_class=OpportunitySourceForm
    template_name = "company/opportunity/opportunitysource-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class OpportunitySourceDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=OpportunitySource
    template_name = "company/opportunity/opportunitysource_confirm_delete.html"
    success_url= reverse_lazy('opportunity:opportunitysource')
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
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')



class OpportunityList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.filter(archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


class OpportunityListAll(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context

class OpportunityList_today(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.filter(due_date=datetime.today(), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context
class OpportunityList_3days(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.filter(due_date__lte=datetime.today()+timedelta(days=3), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context
class OpportunityList_10days(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.filter(due_date__lte=datetime.today()+timedelta(days=10), archive=False)
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context


class OpportunityCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Opportunity
    form_class=OpportunityForm
    template_name="company/opportunity/opportunity-create.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['status'].queryset = OpportunityStatus.objects.filter(company=company)
        context['form'].fields['source'].queryset = OpportunitySource.objects.filter(company=company)
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
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

class OpportunityUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Opportunity
    form_class=OpportunityForm
    template_name = "company/opportunity/opportunity-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['form'].fields['status'].queryset = OpportunityStatus.objects.filter(company=company)
        context['form'].fields['source'].queryset = OpportunitySource.objects.filter(company=company)
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['tags'].queryset = company.companytags.filter(company=company)
        context['company'] = company
        pk=self.kwargs.get('pk')
        context['docs']=company.companydocs.filter(opportunities_id=pk)
        return context

class OpportunityDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Opportunity
    template_name = "company/opportunity/opportunity_confirm_delete.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
