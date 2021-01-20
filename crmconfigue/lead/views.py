from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Lead
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.

@login_required(login_url='login')
@company_enrolled
def LeadsList(request, slug):
    template_name = 'company/leads.html'
    company = get_object_or_404(Company, slug=slug)
    leads = company.companyleads.all()
    return render(request, template_name, {'company': company,
                                           'leads': leads,})


#class LeadsList(LoginRequiredMixin,ListView):
#        queryset= Lead.objects.all()
#        template_name="company/leads.html"
class LeadCreate(LoginRequiredMixin, CreateView):
    model=Lead
    fields=["title","first_name", "last_name", "email","phone","status", "source", "address_line",
     "street", "city","state","postcode", "country", "website", "description", "assigned_to",
     "account_name","opportunity_amount", "created_by", "is_active", "enquery_type", "tags",
     "contacts", "created_from_site", "teams", "company"]
    template_name="company/lead-create-update.html"
    success_url= reverse_lazy('leads:leads')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class LeadUpdate(LoginRequiredMixin, UpdateView):
    model=Lead
    fields=["title","first_name", "last_name", "email","phone","status", "source", "address_line",
     "street", "city","state","postcode", "country", "website", "description", "assigned_to",
     "account_name","opportunity_amount", "created_by", "is_active", "enquery_type", "tags",
     "contacts", "created_from_site", "teams", "company"]
    template_name = "company/lead-create-update.html"
    success_url= reverse_lazy('leads:leads')
class LeadDelete(LoginRequiredMixin, DeleteView):
    model=Lead
    template_name = "company/lead_confirm_delete.html"
    success_url= reverse_lazy('leads:leads')
