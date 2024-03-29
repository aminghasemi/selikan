from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Account
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from .forms import AccountForm
# Create your views here.

class AccountsList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/accounts/accounts.html'
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

class AccountCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=Account
    form_class = AccountForm
    template_name="company/accounts/account-create.html"
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

class AccountUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Account
    form_class = AccountForm
    template_name = "company/accounts/account-update.html"
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
        pk=self.kwargs.get('pk')
        context['docs']=company.companydocs.filter(account_id=pk)
        context['deals']=company.companydeals.filter(account_id=pk)
        context['contacts']=company.companycontacts.filter(account_id=pk)
        context['tasks']=company.companytask.filter(account_id=pk)

        context['invoices']=company.companyinvoice.filter(account_id=pk)
        return context
class AccountDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=Account
    template_name = "company/accounts/account_confirm_delete.html"
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
