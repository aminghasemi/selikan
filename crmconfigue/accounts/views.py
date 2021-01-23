from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Account
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.

class AccountsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/task.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyaccounts.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class AccountCreate(LoginRequiredMixin, CreateView):
    model=Account
    fields=["name", "industry", "email","phone", "billing_address_line", "billing_street", "billing_city", "billing_state",
    "billing_postcode", "billing_country","website", "description", "is_active","status", "lead","contact_name","contacts",
     "assigned_to","teams"]
    template_name="company/account-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyaccounts.all()
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
        return reverse_lazy('accounts:accounts', kwargs={'slug': slug}, current_app='accounts')

class AccountUpdate(LoginRequiredMixin, UpdateView):
    model=Account
    fields=["name", "industry", "email","phone", "billing_address_line", "billing_street", "billing_city", "billing_state",
    "billing_postcode", "billing_country","website", "description", "is_active","status", "lead","contact_name","contacts",
     "assigned_to","teams"]
    template_name = "company/account-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('accounts:accounts', kwargs={'slug': slug}, current_app='accounts')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyaccounts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class AccountDelete(LoginRequiredMixin, DeleteView):
    model=Account
    template_name = "company/account_confirm_delete.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyaccounts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('accounts:accounts', kwargs={'slug': slug}, current_app='accounts')
