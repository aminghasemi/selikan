from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali
from common.decorators import allowed_users, company_enrolled, user_limit
from django.db.models import Sum

from common.models import Company
from .models import Dealreport, Leadreport, Opportunityreport
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from .forms import DealreportForm, LeadreportForm, OpportunityreportForm
# Create your views here.


class Dealreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/dealreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydealsreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class DealreportCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Dealreport
    form_class=DealreportForm
    template_name="company/reports/dealreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydealsreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['pipeline_status'].queryset = company.companypipelines.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['product'].queryset = company.companyproducts.filter(company=company)
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
        return reverse_lazy('reports:dealreports', kwargs={'slug': slug}, current_app='reports')
class DealreportUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Dealreport
    form_class=DealreportForm
    template_name = "company/reports/dealreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:dealreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydealsreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['pipeline_status'].queryset = company.companypipelines.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        context['form'].fields['product'].queryset = company.companyproducts.filter(company=company)
        return context


  
class DealreportDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Dealreport
    template_name = "company/reports/dealreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companydealsreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:dealreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Dealreport_detail(request, slug, pk):
    template_name = "company/reports/dealreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    dealreport=get_object_or_404(Dealreport, pk=pk)
    title=dealreport.title
    pipeline=dealreport.pipeline_status
    startdate=dealreport.startdate
    enddate=dealreport.enddate
    converted_by=dealreport.converted_by
    product=dealreport.product
    if pipeline is None:
        deals1=company.companydeals.filter(created_on__range=(startdate, enddate))
    else:
        deals1=company.companydeals.filter(pipeline_status=pipeline).filter(created_on__range=(startdate, enddate))
    if converted_by is None:
        deals2=deals1
    else:
        deals2=deals1.filter(converted_by=converted_by)
    if product is None:
        deals=deals2
    else:
        deals=deals2.filter(product=product)
    total_deals_count=deals.count()
    total_amount_deals=deals.aggregate(sum=Sum('deal_amount'))['sum']
    return render(request, template_name, {'deals': deals,
                                           'company': company,
                                            'pipeline': pipeline,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'converted_by': converted_by,
                                            'product' : product,
                                            'total_deals_count': total_deals_count,
                                            'total_amount_deals': total_amount_deals,
                                            'dealreport': dealreport,
                                            })



class Leadreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/leadreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class LeadreportCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Leadreport
    form_class=LeadreportForm
    template_name="company/reports/leadreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['lead_status'].queryset = company.companyleadstatus.filter(company=company)
        context['form'].fields['lead_source'].queryset = company.companyleadsource.filter(company=company)
        context['form'].fields['lead_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['lead_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
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
        return reverse_lazy('reports:leadreports', kwargs={'slug': slug}, current_app='reports')
class LeadreportUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Leadreport
    form_class=LeadreportForm
    template_name = "company/reports/leadreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:leadreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['lead_status'].queryset = company.companyleadstatus.filter(company=company)
        context['form'].fields['lead_source'].queryset = company.companyleadsource.filter(company=company)
        context['form'].fields['lead_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['lead_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        return context


  
class LeadreportDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Leadreport
    template_name = "company/reports/leadreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyleadsreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:leadreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Leadreport_detail(request, slug, pk):
    template_name = "company/reports/leadreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    leadreport=get_object_or_404(Leadreport, pk=pk)
    lead_status=leadreport.lead_status
    lead_source=leadreport.lead_status
    lead_teams=leadreport.lead_status
    lead_tags=leadreport.lead_status
    startdate=leadreport.startdate
    enddate=leadreport.enddate
    converted_by=leadreport.converted_by
    product=leadreport.product
    if lead_status is None:
        leads1=company.companyleads.filter(created_on__range=(startdate, enddate))
    else:
        leads1=company.companyleads.filter(status=lead_status).filter(created_on__range=(startdate, enddate))
    if lead_source is None:
        leads2=leads1
    else:
        leads2=leads1.filter(source=lead_source).filter(created_on__range=(startdate, enddate))
    if converted_by is None:
        leads3=leads2
    else:
        leads2=leads2.filter(converted_by=converted_by)
    if lead_teams is None:
        leads3=leads2
    else:
        leads3=leads2.filter(teams=lead_teams)
    if lead_tags is None:
        leads=leads3
    else:
        leads=leads3.filter(tags=lead_tags)
    total_leads_count=leads.count()
    return render(request, template_name, {'leads': leads,
                                           'company': company,
                                            'lead_status': lead_status,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'converted_by': converted_by,
                                            'product' : product,
                                            'total_leads_count': total_leads_count,
                                            'leadreport': leadreport,
                                            })







class Opportunityreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/opportunityreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunityreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class OpportunityreportCreate(EnrollMixin, LoginRequiredMixin, CreateView):
    model=Opportunityreport
    form_class=OpportunityreportForm
    template_name="company/reports/opportunityreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunityreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['opportunity_status'].queryset = company.companyopportunitystatus.filter(company=company)
        context['form'].fields['opportunity_source'].queryset = company.companyopportunitysource.filter(company=company)
        context['form'].fields['opportunity_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['opportunity_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
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
        return reverse_lazy('reports:opportunityreports', kwargs={'slug': slug}, current_app='reports')
class OpportunityreportUpdate(EnrollMixin, LoginRequiredMixin, UpdateView):
    model=Opportunityreport
    form_class=OpportunityreportForm
    template_name = "company/reports/opportunityreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:opportunityreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunityreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['opportunity_status'].queryset = company.companyopportunitystatus.filter(company=company)
        context['form'].fields['opportunity_source'].queryset = company.companyopportunitysource.filter(company=company)
        context['form'].fields['opportunity_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['opportunity_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['converted_by'].queryset = company.staff_enroll.filter(company=company)
        return context


  
class OpportunityreportDelete(EnrollMixin, LoginRequiredMixin, DeleteView):
    model=Opportunityreport
    template_name = "company/reports/opportunityreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyopportunityreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:opportunityreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Opportunityreport_detail(request, slug, pk):
    template_name = "company/reports/opportunityreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    opportunityreport=get_object_or_404(Opportunityreport, pk=pk)
    opportunity_status=opportunityreport.opportunity_status
    opportunity_source=opportunityreport.opportunity_status
    opportunity_teams=opportunityreport.opportunity_status
    opportunity_tags=opportunityreport.opportunity_status
    startdate=opportunityreport.startdate
    enddate=opportunityreport.enddate
    converted_by=opportunityreport.converted_by
    product=opportunityreport.product
    if opportunity_status is None:
        opportunities1=company.companyopportunity.filter(created_on__range=(startdate, enddate))
    else:
        opportunities1=company.companyopportunity.filter(status=opportunity_status).filter(created_on__range=(startdate, enddate))
    if opportunity_source is None:
        opportunities2=opportunities1
    else:
        opportunities2=opportunities1.filter(source=opportunity_source).filter(created_on__range=(startdate, enddate))
    if converted_by is None:
        opportunities3=opportunities2
    else:
        opportunities2=opportunities2.filter(converted_by=converted_by)
    if opportunity_teams is None:
        opportunities3=opportunities2
    else:
        opportunities3=opportunities2.filter(teams=opportunity_teams)
    if opportunity_tags is None:
        opportunities=opportunities3
    else:
        opportunities=opportunities3.filter(tags=opportunity_tags)
    total_opportunities_count=opportunities.count()
    return render(request, template_name, {'opportunities': opportunities,
                                           'company': company,
                                            'opportunity_status': opportunity_status,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'converted_by': converted_by,
                                            'product' : product,
                                            'total_opportunities_count': total_opportunities_count,
                                            'opportunityreport': opportunityreport,
                                            })
