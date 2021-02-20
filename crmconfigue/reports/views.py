from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali
from common.decorators import allowed_users, company_enrolled, user_limit
from django.db.models import Sum

from common.models import Company
from .models import Dealreport, Leadreport, Opportunityreport, Taskreport, Staffreport, Companyreport
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from .forms import DealreportForm, LeadreportForm, OpportunityreportForm, TaskreportForm, StaffreportForm, CompanyreportForm
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

class DealreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
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
class DealreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
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


  
class DealreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
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

class LeadreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
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
class LeadreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
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


  
class LeadreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
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
    lead_source=leadreport.lead_source
    lead_teams=leadreport.lead_teams
    lead_tags=leadreport.lead_tags
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

class OpportunityreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
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
class OpportunityreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
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


  
class OpportunityreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
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
    opportunity_source=opportunityreport.opportunity_source
    opportunity_teams=opportunityreport.opportunity_teams
    opportunity_tags=opportunityreport.opportunity_tags
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





class Taskreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/taskreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytaskreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class TaskreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Taskreport
    form_class=TaskreportForm
    template_name="company/reports/taskreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytaskreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['task_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['task_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['done_by'].queryset = company.staff_enroll.filter(company=company)
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
        return reverse_lazy('reports:taskreports', kwargs={'slug': slug}, current_app='reports')
class TaskreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Taskreport
    form_class=TaskreportForm
    template_name = "company/reports/taskreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:taskreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytaskreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['task_tags'].queryset = company.companytags.filter(company=company)
        context['form'].fields['task_teams'].queryset = company.companyteams.filter(company=company)
        context['form'].fields['done_by'].queryset = company.staff_enroll.filter(company=company)
        return context


  
class TaskreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Taskreport
    template_name = "company/reports/taskreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companytaskreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:taskreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Taskreport_detail(request, slug, pk):
    template_name = "company/reports/taskreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    taskreport=get_object_or_404(Taskreport, pk=pk)
    task_status=taskreport.task_status
    task_priority=taskreport.task_priority
    task_teams=taskreport.task_teams
    task_tags=taskreport.task_tags
    startdate=taskreport.startdate
    enddate=taskreport.enddate
    done_by=taskreport.done_by
    if task_status is None:
        tasks1=company.companytask.filter(created_on__range=(startdate, enddate))
    else:
        tasks1=company.companytask.filter(status=task_status).filter(created_on__range=(startdate, enddate))
    if task_priority is None:
        tasks2=tasks1
    else:
        tasks2=tasks1.filter(priority=task_priority).filter(created_on__range=(startdate, enddate))
    if done_by is None:
        tasks3=tasks2
    else:
        tasks2=tasks2.filter(done_by=done_by)
    if task_teams is None:
        tasks3=tasks2
    else:
        tasks3=tasks2.filter(teams=task_teams)
    if task_tags is None:
        tasks=tasks3
    else:
        tasks=tasks3.filter(tags=task_tags)
    total_tasks_count=tasks.count()
    return render(request, template_name, {'tasks': tasks,
                                           'company': company,
                                            'task_status': task_status,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'done_by': done_by,
                                            'total_tasks_count': total_tasks_count,
                                            'taskreport': taskreport,
                                            })



class Staffreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/staffreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companystaffreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class StaffreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Staffreport
    form_class=StaffreportForm
    template_name="company/reports/staffreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companystaffreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['form'].fields['staff'].queryset = company.staff_enroll.filter(company=company)
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
        return reverse_lazy('reports:staffreports', kwargs={'slug': slug}, current_app='reports')
class StaffreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Staffreport
    form_class=StaffreportForm
    template_name = "company/reports/staffreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:staffreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companystaffreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        context['form'].fields['staff'].queryset = company.staff_enroll.filter(company=company)
        return context


  
class StaffreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Staffreport
    template_name = "company/reports/staffreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companystaffreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:staffreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Staffreport_detail(request, slug, pk):
    template_name = "company/reports/staffreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    staffreport=get_object_or_404(Staffreport, pk=pk)
    staff=staffreport.staff
    startdate=staffreport.startdate
    enddate=staffreport.enddate
    staff_deals=company.companydeals.filter(converted_by=staff).filter(created_on__range=(startdate, enddate))
    staff_leads=company.companyleads.filter(converted_by=staff).filter(created_on__range=(startdate, enddate))
    staff_opportunities=company.companyopportunity.filter(converted_by=staff).filter(created_on__range=(startdate, enddate))
    staff_tasks=company.companytask.filter(done_by=staff).filter(created_on__range=(startdate, enddate))
    total_staff_deals=staff_deals.count()
    total_staff_leads=staff_leads.count()
    total_staff_opportunity=staff_opportunities.count()
    total_staff_tasks=staff_tasks.count()
    total_amount_deals=staff_deals.aggregate(sum=Sum('deal_amount'))['sum']
    return render(request, template_name, {'staff': staff,
                                           'company': company,
                                            'staff_deals': staff_deals,
                                            'staff_leads': staff_leads,
                                            'staff_opportunities': staff_opportunities,
                                            'staff_tasks': staff_tasks,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'total_staff_deals': total_staff_deals,
                                            'total_staff_leads': total_staff_leads,
                                            'total_staff_opportunity': total_staff_opportunity,
                                            'total_staff_tasks': total_staff_tasks,
                                            'staffreport': staffreport,
                                            'total_amount_deals': total_amount_deals,
                                            })



class Companyreportlist(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/reports/companyreports.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycompanyreports.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class CompanyreportCreate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, CreateView):
    model=Companyreport
    form_class=CompanyreportForm
    template_name="company/reports/companyreport-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycompanyreports.all()
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
        return reverse_lazy('reports:companyreports', kwargs={'slug': slug}, current_app='reports')

class CompanyreportUpdate(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, UpdateView):
    model=Companyreport
    form_class=CompanyreportForm
    template_name = "company/reports/companyreport-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:companyreports', kwargs={'slug': slug}, current_app='reports')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycompanyreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context


  
class CompanyreportDelete(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin, DeleteView):
    model=Companyreport
    template_name = "company/reports/companyreport_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycompanyreports.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('reports:companyreports', kwargs={'slug': slug}, current_app='reports')

@login_required(login_url='login')
@company_enrolled
@user_limit
def Companyreport_detail(request, slug, pk):
    template_name = "company/reports/companyreport_detail.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    companyreport=get_object_or_404(Companyreport, pk=pk)
    company=companyreport.company
    startdate=companyreport.startdate
    enddate=companyreport.enddate
    company_deals=company.companydeals.filter(created_on__range=(startdate, enddate))
    company_leads=company.companyleads.filter(created_on__range=(startdate, enddate))
    company_opportunities=company.companyopportunity.filter(created_on__range=(startdate, enddate))
    company_tasks=company.companytask.filter(created_on__range=(startdate, enddate))
    total_company_deals=company_deals.count()
    total_company_leads=company_leads.count()
    total_company_opportunity=company_opportunities.count()
    total_company_tasks=company_tasks.count()
    total_amount_deals=company_deals.aggregate(sum=Sum('deal_amount'))['sum']
    return render(request, template_name, {'company': company,
                                           'company': company,
                                            'company_deals': company_deals,
                                            'company_leads': company_leads,
                                            'company_opportunities': company_opportunities,
                                            'company_tasks': company_tasks,
                                            'startdate': startdate,
                                            'enddate': enddate,
                                            'total_company_deals': total_company_deals,
                                            'total_company_leads': total_company_leads,
                                            'total_company_opportunity': total_company_opportunity,
                                            'total_company_tasks': total_company_tasks,
                                            'companyreport': companyreport,
                                            'total_amount_deals': total_amount_deals,
                                            })