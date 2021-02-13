from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali

from common.models import Company
from .models import Doc
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from common.decorators import company_enrolled
from .forms import DocForm
# Create your views here

class DocList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/docs/doc.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydocs.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class DocCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Doc
    form_class=DocForm
    template_name="company/docs/doc-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydocs.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['contacts'].queryset = company.companycontacts.filter(company=company)
        context['form'].fields['deals'].queryset = company.companydeals.filter(company=company)
        context['form'].fields['leads'].queryset = company.companyleads.filter(company=company)
        context['form'].fields['tasks'].queryset = company.companytask.filter(company=company)
        context['form'].fields['opportunities'].queryset = company.companyopportunity.filter(company=company)
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
        return reverse_lazy('doc:docs', kwargs={'slug': slug}, current_app='doc')
class DocUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Doc
    form_class=DocForm
    template_name = "company/docs/doc-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('doc:docs', kwargs={'slug': slug}, current_app='doc')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydocs.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['contacts'].queryset = company.companycontacts.filter(company=company)
        context['form'].fields['deals'].queryset = company.companydeals.filter(company=company)
        context['form'].fields['leads'].queryset = company.companyleads.filter(company=company)
        context['form'].fields['tasks'].queryset = company.companytask.filter(company=company)
        context['form'].fields['opportunities'].queryset = company.companyopportunity.filter(company=company)
        context['form'].fields['teams'].queryset = company.companyteams.filter(company=company)
        return context


  
class DocDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Doc
    template_name = "company/docs/doc_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydocs.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('doc:docs', kwargs={'slug': slug}, current_app='doc')




