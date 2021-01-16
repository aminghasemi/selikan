from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Opportunity
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class OpportunityList(LoginRequiredMixin,ListView):
        queryset= Opportunity.objects.all()
        template_name="company/opportunity.html"
class OpportunityCreate(LoginRequiredMixin, CreateView):
    model=Opportunity
    fields=["name", "account", "stage","currency", "amount", "lead_source", "probability", "contacts",
    "closed_by", "closed_on","description", "assigned_to", "is_active","tags", "teams"]
    template_name="company/account-create-update.html"
    success_url= reverse_lazy('opportunity:opportunity')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class OpportunityUpdate(LoginRequiredMixin, UpdateView):
    model=Opportunity
    fields=["name", "account", "stage","currency", "amount", "lead_source", "probability", "contacts",
    "closed_by", "closed_on","description", "assigned_to", "is_active","tags", "teams"]
    template_name = "company/account-create-update.html"
    success_url= reverse_lazy('opportunity:opportunity')
class OpportunityDelete(LoginRequiredMixin, DeleteView):
    model=Opportunity
    template_name = "company/account_confirm_delete.html"
    success_url= reverse_lazy('opportunity:opportunity')
