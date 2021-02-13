from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required


from common.models import Company
from .models import Invoice, Inovice_item
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from common.decorators import company_enrolled
# Create your views here.

class InvoiceList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/invoice/invoices.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvoice.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class InvoiceCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Invoice
    fields=["title", "invoice_number", "status","date", "account", "description", "teams", "tax"]
    template_name="company/invoice/invoice-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvoice.all()
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
        return reverse_lazy('invoice:invoice', kwargs={'slug': slug}, current_app='invoice')

class InvoiceUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Invoice
    fields=["title", "invoice_number", "status","date", "account", "description", "teams", "tax"]
    template_name = "company/invoice/invoice-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('invoice:invoice', kwargs={'slug': slug}, current_app='invoice')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


  
class InvoiceDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Invoice
    template_name = "company/invoice/invoice_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('task:task', kwargs={'slug': slug}, current_app='task')










class Invoice_itemCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Invoice
    fields=["product_name", "amount", "total_item_amount","date", "account", "description", "teams", "tax"]
    template_name="company/invoice/invoice-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvoice.all()
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
        return reverse_lazy('invoice:invoice', kwargs={'slug': slug}, current_app='task')