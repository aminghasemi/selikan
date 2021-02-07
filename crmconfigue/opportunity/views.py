from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Opportunity, OpportunityStatus, OpportunitySource
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from .forms import OpportunityForm, OpportunityStatusForm, OpportunitySourceForm
# Create your views here.


class OpportunityStatusList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunitystatus.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityStatusCreate(LoginRequiredMixin, CreateView):
    model=OpportunityStatus
    form_class=OpportunityStatusForm
    template_name="company/opportunity/opportunitystatus-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
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
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')

class OpportunityStatusUpdate(LoginRequiredMixin, UpdateView):
    model=OpportunityStatus
    form_class=OpportunityStatusForm
    template_name = "company/opportunity/opportunitystatus-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitystatus.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class OpportunityStatusDelete(LoginRequiredMixin, DeleteView):
    model=OpportunityStatus
    template_name = "company/opportunity/opportunitystatus_confirm_delete.html"
    success_url= reverse_lazy('opportunity:opportunitystatus')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitystatus', kwargs={'slug': slug}, current_app='opportunity')


class OpportunitySourceList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity/opportunitysource.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunitySourceCreate(LoginRequiredMixin, CreateView):
    model=OpportunitySource
    form_class=OpportunitySourceForm
    template_name="company/opportunity/opportunitysource-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
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
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')

class OpportunitySourceUpdate(LoginRequiredMixin, UpdateView):
    model=OpportunitySource
    form_class=OpportunitySourceForm
    template_name = "company/opportunity/opportunitysource-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunitysource.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class OpportunitySourceDelete(LoginRequiredMixin, DeleteView):
    model=OpportunitySource
    template_name = "company/opportunity/opportunitysource_confirm_delete.html"
    success_url= reverse_lazy('opportunity:opportunitysource')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companypipelines.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunitysource', kwargs={'slug': slug}, current_app='opportunity')



class OpportunityList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/opportunity.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Opportunity
    form_class=OpportunityForm
    template_name="company/opportunity-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
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

class OpportunityUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Opportunity
    form_class=OpportunityForm
    template_name = "company/opportunity-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Opportunity
    template_name = "company/opportunity_confirm_delete.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('opportunity:opportunity', kwargs={'slug': slug}, current_app='opportunity')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunity.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
