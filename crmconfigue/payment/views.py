from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from common.models import Company
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from .models import Billing

class BillingList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'registration/billings.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companybilling.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class BillingCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Billing
    fields=["staff_number", "month_number"]
    template_name="registration/billing_create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytask.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def form_valid(self, form, **kwargs):       
        form.instance.user = self.request.user
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        form.instance.company= company
        return super().form_valid(form, **kwargs)



# -*- coding: utf-8 -*-
# Github.com/Rasooll
from django.http import HttpResponse
from zeep import Client

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.

def send_request(request):
    amount = 1000  # Toman / Required

    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request, slug):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            company = get_object_or_404(Company, slug=slug)
            company.access_date = datetime.now() + timedelta(days=30)
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
