from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Deal, Pipeline
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class PipelinesList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/pipelines.html'
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

class PipelineCreate(LoginRequiredMixin, CreateView):
    model=Pipeline
    fields=["pipeline_number","pipeline_title"]
    template_name="company/pipeline-create-update.html"
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

class PipelineUpdate(LoginRequiredMixin, UpdateView):
    model=Pipeline
    fields=["pipeline_number","pipeline_title"]
    template_name = "company/pipeline-create-update.html"
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
class PipelineDelete(LoginRequiredMixin, DeleteView):
    model=Pipeline
    template_name = "company/pipeline_confirm_delete.html"
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



class DealsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/deals.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
      #  context['deals']= company.companydeals.all()
        return context
class DealCreate(LoginRequiredMixin, CreateView):
    model=Deal
    fields=["title","pipeline_status", "description", "assigned_to","account_name","deal_amount", "is_active", "contacts","teams"]
    template_name="company/deal-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydeals.all()
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
        return reverse_lazy('deals:deals', kwargs={'slug': slug}, current_app='deals')

class DealUpdate(LoginRequiredMixin, UpdateView):
    model=Deal
    fields=["title","pipeline_status", "description", "assigned_to","account_name","deal_amount", "is_active", "contacts","teams"]
    template_name = "company/deal-create-update.html"
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
        context['company'] = company
        return context
class DealDelete(LoginRequiredMixin, DeleteView):
    model=Deal
    template_name = "company/deal_confirm_delete.html"
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