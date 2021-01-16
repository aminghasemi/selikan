from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Account
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class AccountsList(LoginRequiredMixin,ListView):
        queryset= Account.objects.all()
        template_name="company/accounts.html"
class AccountCreate(LoginRequiredMixin, CreateView):
    model=Account
    fields=["name", "industry", "email","phone", "billing_address_line", "billing_street", "billing_city", "billing_state",
    "billing_postcode", "billing_country","website", "description", "is_active","status", "lead","contact_name","contacts",
     "assigned_to","teams","company"]
    template_name="company/account-create-update.html"
    success_url= reverse_lazy('accounts:accounts')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AccountUpdate(LoginRequiredMixin, UpdateView):
    model=Account
    fields=["name", "industry", "email","phone", "billing_address_line", "billing_street", "billing_city", "billing_state",
    "billing_postcode", "billing_country","website", "description", "is_active","status", "lead","contact_name","contacts",
     "assigned_to","teams","company"]
    template_name = "company/account-create-update.html"
    success_url= reverse_lazy('accounts:accounts')
class AccountDelete(LoginRequiredMixin, DeleteView):
    model=Account
    template_name = "company/account_confirm_delete.html"
    success_url= reverse_lazy('accounts:accounts')
