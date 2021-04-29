from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import DealForm
from common.models import Company, Enrolled
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Deal, Pipeline
from common.mixins import EnrollMixin,SpecialCompanyMixin, SuperUserAccessMixin, CreatorAccessMixin
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from itertools import chain
# Create your views here.


class PipelinesList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/deal/pipelines.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class PipelineCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=Pipeline
    fields=["pipeline_number","pipeline_title","won", "lost"]
    template_name="company/deal/pipeline-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
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
        return reverse_lazy('deals:pipelines', kwargs={'slug': slug}, current_app='deals')

class PipelineUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Pipeline
    fields=["pipeline_number","pipeline_title","won", "lost"]
    template_name = "company/deal/pipeline-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('deals:pipelines', kwargs={'slug': slug}, current_app='deals')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class PipelineDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=Pipeline
    template_name = "company/deal/pipeline_confirm_delete.html"
    success_url= reverse_lazy('deals:pipelines')
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
        return reverse_lazy('deals:pipelines', kwargs={'slug': slug}, current_app='deals')



class DealsList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/deal/deals.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        warning_date=datetime.now() - timedelta(days=1)
        context['company'] = company
        context['warning_date']= warning_date
      #  context['deals']= company.companydeals.all()
        return context
class DealCreate(LoginRequiredMixin, SpecialCompanyMixin,CreateView):
    model=Deal
    form_class = DealForm
    template_name="company/deal/deal-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['pipeline_status'].queryset = company.companypipelines.filter(company=company)
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
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
        return reverse_lazy('deals:deals', kwargs={'slug': slug}, current_app='deals')

class DealUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Deal
    form_class = DealForm
    template_name = "company/deal/deal-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('deals:deals', kwargs={'slug': slug}, current_app='deals')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['form'].fields['pipeline_status'].queryset = Pipeline.objects.filter(company=company)
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['assigned_to'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
        context['company'] = company
        pk=self.kwargs.get('pk')
        context['docs']=company.companydocs.filter(deals_id=pk)
        context['invoices']=company.companyinvoice.filter(deal_id=pk)
        return context
class DealDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=Deal
    template_name = "company/deal/deal_confirm_delete.html"
    success_url= reverse_lazy('deals:deals')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('deals:deals', kwargs={'slug': slug}, current_app='deals')