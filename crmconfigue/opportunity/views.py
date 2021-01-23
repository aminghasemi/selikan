from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Opportunity
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.

class OpportunityList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Opportunity
    fields=["name", "account", "stage","currency", "amount", "lead_source", "probability", "contacts",
    "closed_by", "closed_on","description", "assigned_to", "is_active","tags", "teams"]
    template_name="company/opportunity-create-update.html"
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
        context['company'] = company
        return context
    def form_valid(self, form, **kwargs):       
        form.instance.created_by = self.request.user
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        form.instance.company= company
        return super().form_valid(form, **kwargs)

class OpportunityUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Opportunity
    fields=["name", "account", "stage","currency", "amount", "lead_source", "probability", "contacts",
    "closed_by", "closed_on","description", "assigned_to", "is_active","tags", "teams"]
    template_name = "company/opportunity-create-update.html"
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

class OpportunityDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Opportunity
    template_name = "company/opportunity_confirm_delete.html"
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
