from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from jalali_date import datetime2jalali, date2jalali
from common.decorators import allowed_users, company_enrolled, user_limit
from django.db.models import Sum

from common.models import Company
from .models import Dealreport
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin, SpecialCompanyMixin
from .forms import DealreportForm
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
