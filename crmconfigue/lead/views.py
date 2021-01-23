from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Lead
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class LeadsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/leads.html'
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
    fields=["title","first_name", "last_name", "email","phone","status", "source", "address_line",
     "street", "city","state","postcode", "country", "website", "description", "assigned_to",
     "account_name","opportunity_amount", "created_by", "is_active", "enquery_type", "tags",
     "contacts", "created_from_site", "teams"]
    template_name="company/lead-create-update.html"
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
    fields=["title","first_name", "last_name", "email","phone","status", "source", "address_line",
     "street", "city","state","postcode", "country", "website", "description", "assigned_to",
     "account_name","opportunity_amount", "created_by", "is_active", "enquery_type", "tags",
     "contacts", "created_from_site", "teams"]
    template_name = "company/lead-create-update.html"
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
        context['company'] = company
        return context
class LeadDelete(LoginRequiredMixin, DeleteView):
    model=Lead
    template_name = "company/lead_confirm_delete.html"
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