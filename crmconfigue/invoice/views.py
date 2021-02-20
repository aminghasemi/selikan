from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import InvoiceForm, Invoice_itemForm
from common.models import Company
from .models import Invoice, Invoice_item
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from common.decorators import allowed_users, company_enrolled, user_limit
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

class InvoiceCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Invoice
    form_class= InvoiceForm
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
        context['form'].fields['account'].queryset = company.companyaccounts.filter(company=company)
        context['form'].fields['deal'].queryset = company.companydeals.filter(company=company)
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
        pk= self.kwargs.get('pk')
        return reverse_lazy('invoice:invoice-detail', kwargs={'slug': slug, 'pk': self.object.pk}, current_app='invoice')

class InvoiceUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Invoice
    form_class= InvoiceForm
    template_name = "company/invoice/invoice-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        pk= self.kwargs.get('pk')
        return reverse_lazy('invoice:invoice-detail', kwargs={'slug': slug, 'pk': pk}, current_app='invoice')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvoice.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


  
class InvoiceDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Invoice
    template_name = "company/invoice/invoice_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvoice.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('invoice:invoices', kwargs={'slug': slug}, current_app='invoice')



@login_required(login_url='login')
@company_enrolled
@user_limit
def Invoice_detail(request, slug, pk):
    template_name = 'company/invoice/invoice-detail.html'
    company = get_object_or_404(Company, slug=slug)
    invoice=get_object_or_404(Invoice, pk=pk)
    invoice_item = invoice.Invoiceitem.all()
    new_item = None
    invoice.total_amount=invoice_item.aggregate(sum=Sum('total_item_amount'))['sum'] or 0
    total_amount2=invoice_item.aggregate(sum=Sum('total_item_amount'))['sum'] or 0
    invoice.total_bargain= ((invoice.total_amount)*(invoice.bargain/100))
    invoice.total_tax= ((invoice.total_amount)*(invoice.tax/100))
    invoice.final_total_amount=(invoice.total_amount)+(invoice.total_tax)-(invoice.total_bargain)
    if request.method == 'POST':
        invoice_item_form = Invoice_itemForm(data=request.POST)
        def form_valid(self, form):
            form.instance.invoice = invoice
            form.instance.created_by = self.request.user
            return super(Invoice_detail, self).form_valid(form)
        if invoice_item_form.is_valid():

            # Create Comment object but don't save to database yet
            new_item = invoice_item_form.save(commit=False)
            # Assign the current invoice to the item
            new_item.invoice = invoice
            # Save the comment to the database
            new_item.save()
    else:
        invoice_item_form = Invoice_itemForm()    

    return render(request, template_name, {'invoice': invoice,
                                           'company': company,
                                           'invoice_item': invoice_item,
                                           'new_item': new_item,
                                           'invoice_item_form': invoice_item_form,})




