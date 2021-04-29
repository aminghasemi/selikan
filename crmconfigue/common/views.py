from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from cuser.middleware import CuserMiddleware
from itertools import chain
from .models import Company, User, Product, Country, Enrolled, Enroll_Invitation
from .mixins import CreatorAccessMixin, SuperUserAccessMixin, SpecialCompanyMixin, EnrollMixin
from .decorators import allowed_users, company_enrolled, user_limit
from .forms import EnrollForm, ProfileForm, CompanyForm, Enroll_InvitationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from datetime import timedelta, datetime
from django.utils import timezone 
from django.db.models import Sum, Q
from django.http import HttpResponse, HttpResponseRedirect 
# Create your views here.


def home(request):
    return render(request, 'statichome/home.html')

class CompaniesList(LoginRequiredMixin, ListView):
    queryset= Company.objects.all()
    template_name="registration/home.html"
    def get_queryset(self):
        company=Company.objects.filter(staff=self.request.user)
        return company
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        enroll_invitations=Enroll_Invitation.objects.filter(email=self.request.user.email)
        context['enroll_invitations'] = enroll_invitations
        return context

class CompanyCreate(LoginRequiredMixin, CreateView):
    model=Company
    form_class=CompanyForm
    template_name="registration/company-create.html"
    success_url= reverse_lazy('common:home')
    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.access_date=timezone.now()+timedelta(days=15)
        self.object=form.save()
        return super().form_valid(form)
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        pk= self.kwargs.get('pk')
        return reverse_lazy('common:company-preview', kwargs={'slug': self.object.slug}, current_app='common')

@login_required(login_url='login')
def Company_Preview(request, slug):
    template_name = 'company/common/company-preview.html'
    company = get_object_or_404(Company, slug=slug)
    Enrolled.objects.create(company=company, staff=request.user)
    return render(request, template_name, {'company': company,})

class CompanyUpdate(LoginRequiredMixin,CreatorAccessMixin, UpdateView):
    model=Company
    form_class=CompanyForm
    template_name = "registration/company-update.html"
    success_url= reverse_lazy('common:home')
    
class CompanyDelete(LoginRequiredMixin,CreatorAccessMixin, DeleteView):
    model=Company
    template_name = "registration/Company_confirm_delete.html"
    success_url= reverse_lazy('common:home')

class EnrollCreate(LoginRequiredMixin, CreateView):
    model=Enrolled
    form_class=EnrollForm
    template_name= "registration/enroll.html"
    success_url= reverse_lazy('common:home')
    def form_valid(self, form, **kwargs):  
        enroll_invitations=Enroll_Invitation.objects.get(email=self.request.user.email)
        form.instance.staff= self.request.user
        form.instance.company = enroll_invitations.company
        self.object=form.save()
        enroll_invitations.delete()
        return HttpResponseRedirect(self.get_success_url())
    def get_context_data(self, **kwargs):
        enroll_invitations=Enroll_Invitation.objects.filter(email=self.request.user.email)
        context= super().get_context_data(**kwargs)
        context['enroll_invitations'] = enroll_invitations
        return context
    def get_success_url(self):
        return reverse_lazy('common:home')

class Enroll_InvitationDelete(LoginRequiredMixin, DeleteView):
    template_name= "registration/enroll_invitation_confirm_delete.html"
    model= Enroll_Invitation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        enroll_invitations=Enroll_Invitation.objects.filter(email=self.request.user.email)
        context= super().get_context_data(**kwargs)
        context['enroll_invitations'] = enroll_invitations
        return context
    def get_success_url(self):
        return reverse_lazy('common:home')

class Enroll_InvitationDelete_addstaff(LoginRequiredMixin, DeleteView):
    template_name= "registration/invitations_confirm_delete.html"
    model= Enroll_Invitation
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyinvitations.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:company_add_staff', kwargs={'slug': slug}, current_app='common')

@login_required(login_url='login')
@company_enrolled
def company_staff(request, slug):
    template_name = 'registration/company_add_staff.html'
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    companystaff = company.staff_enroll.all()
    companyinvitations=company.companyinvitations.all()
    staff_count=company.staff_enroll.all().count()+1
    new_staff = None
    error= None
    if request.method == 'POST':
        def form_valid(self, form):
            form.instance.company = company
            form.instance.created_by= self.request.user
            return super(company_staff, self).form_valid(form)
        enroll_form = Enroll_InvitationForm(data=request.POST)
        if enroll_form.is_valid():

            new_staff = enroll_form.save(commit=False)
            # Create Comment object but don't save to database yet
            # Assign the current post to the comment
            new_staff.company = company
            new_staff.created_by=request.user
            # Save the comment to the database
            if new_staff.email!= company.creator.email and company.staff_enroll.filter(staff__email=new_staff.email).count()==0:
                new_staff.save()
            else:
                error="کاربر وارد شده با این ایمیل قبلا در شرکت عضو شده است."
    else:
        enroll_form = Enroll_InvitationForm()
    return render(request, template_name, {'companystaff': companystaff,
                                           'companyinvitations': companyinvitations,
                                           'company': company,
                                           'new_staff': new_staff,
                                           'error': error,
                                           'staff_count': staff_count,
                                           'enroll_form': enroll_form,})
class StaffDelete(LoginRequiredMixin,CreatorAccessMixin, DeleteView):
    model=Enrolled
    template_name = "registration/staff_confirm_delete.html"

    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.staff_enroll.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:company_add_staff', kwargs={'slug': slug}, current_app='common')

class Profile(LoginRequiredMixin ,UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("common:home")

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs




class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("common:home")

from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد. <a href="/login">ورود</a>')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک</a> کنید.')
    else:
        return HttpResponse('لینک فعال سازی منقضی شده است. <a href="/registration">دوباره امتحان کنید.</a>')




class ProductsList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/common/products.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproducts.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class ProductCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=Product
    fields=["name", "code", "unit", "price","price_unit", "description"]
    template_name="company/common/product-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproducts.all()
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
        return reverse_lazy('common:products', kwargs={'slug': slug}, current_app='common')

class ProductUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Product
    fields=["name", "code", "unit", "price","price_unit", "description"]
    template_name = "company/common/product-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:products', kwargs={'slug': slug}, current_app='common')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproducts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class ProductDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=Product
    template_name = "company/common/product_confirm_delete.html"
    success_url= reverse_lazy('common:products')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companyproducts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:products', kwargs={'slug': slug}, current_app='common')

class CountriesList(EnrollMixin,SpecialCompanyMixin, LoginRequiredMixin,ListView):
    template_name = 'company/common/countries.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycountries.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class CountryCreate(LoginRequiredMixin,SpecialCompanyMixin, CreateView):
    model=Country
    fields=["name", "short_name"]
    template_name="company/common/country-create-update.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycountries.all()
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
        return reverse_lazy('common:countries', kwargs={'slug': slug}, current_app='common')

class CountryUpdate(LoginRequiredMixin,SpecialCompanyMixin, UpdateView):
    model=Country
    fields=["name", "short_name"]
    template_name = "company/common/country-create-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:countries', kwargs={'slug': slug}, current_app='common')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycountries.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
class CountryDelete(LoginRequiredMixin,SpecialCompanyMixin, DeleteView):
    model=Country
    template_name = "company/common/country_confirm_delete.html"
    success_url= reverse_lazy('common:countries')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycountries.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('common:countries', kwargs={'slug': slug}, current_app='common')



@login_required(login_url='login')
@company_enrolled
@user_limit
def Dashboard(request, slug):
    template_name = "company/dashboard.html"
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    days7_deals = company.companydeals.filter(pipeline_status__won=True).filter(closed_on__gte=datetime.today()-timedelta(days=7))
  #  dealswon=deals.dealpipeline.filter(is_won=True)
    today=datetime.now()
    deals = company.companydeals.filter(pipeline_status__won=True).filter(closed_on__year=today.year, closed_on__month=today.month)
    total=deals.aggregate(sum=Sum('deal_amount'))['sum']
    totaldeals=company.companydeals.filter(created_on__year=today.year, created_on__month=today.month).count()
    deals2 = company.companydeals.filter(pipeline_status__won=True).filter(closed_on__year=today.year, closed_on__month=today.month).count()
    days7_total=days7_deals.aggregate(sum=Sum('deal_amount'))['sum']
    deals_show=company.companydeals.filter(pipeline_status__won=False).order_by('-id')[:5]
    dealswon = company.companydeals.filter(pipeline_status__won=True).count()
    if totaldeals!= 0:
        deals_conversionrate=(deals2/totaldeals)*100
    else:
        deals_conversionrate=0
    
    #Queries of Leads
    leads_show=company.companyleads.all().order_by('-id')[:5]
    leads_current_month=company.companyleads.filter(created_on__year=today.year, created_on__month=today.month).count()
    leads_won = company.companyleads.filter(status__won=True).filter(closed_on__year=today.year, closed_on__month=today.month).count()
    if leads_current_month!= 0:
        leads_conversionrate=(leads_won/leads_current_month)*100
    else:
        leads_conversionrate=0
    #Queries of Opportunities
    opportunity_show=company.companyopportunity.all().order_by('-id')[:5]
    opportunity_current_month=company.companyopportunity.filter(created_on__year=today.year, created_on__month=today.month).count()
    opportunity_won = company.companyopportunity.filter(status__won=True).filter(closed_on__year=today.year, closed_on__month=today.month).count()
    if opportunity_current_month!= 0:
        opportunity_conversionrate=(opportunity_won/opportunity_current_month)*100
    else:
        opportunity_conversionrate=0
    #Queries of Accounts
    newaccounts=company.companyaccounts.filter(created_on__year=today.year, created_on__month=today.month).count()
    accountsall=company.companyaccounts.all().count()
    #Queries of Tasks
    important_tasks=company.companytask.filter(priority="بالا").order_by('-id')[:3]
    average_tasks=company.companytask.filter(priority="معمولی").order_by('-id')[:3]
    low_tasks=company.companytask.filter(priority="پایین").order_by('-id')[:3]
    new_tasks_month=company.companytask.filter(created_on__year=today.year, created_on__month=today.month).count()
    tasks_done=company.companytask.filter(created_on__year=today.year, created_on__month=today.month).count()
    tasks_done_month=company.companytask.filter(done_on__year=today.year, done_on__month=today.month).count()
    todaytasks=company.companytask.filter(due_date=datetime.today())
    meeting=company.companytask.filter(due_date=datetime.today()).filter(Q(subject="جلسه") | Q(subject="تماس"))

    return render(request, template_name, {'total': total,
                                           'company': company,
                                           'deals_conversionrate': deals_conversionrate,
                                           'todaytasks': todaytasks,
                                           'average_tasks': average_tasks,
                                           'low_tasks': low_tasks,
                                           'tasks_done': tasks_done,
                                           'tasks_done_month': tasks_done_month,
                                           'days7_total': days7_total,
                                           'deals_show': deals_show,
                                           'totaldeals': totaldeals,
                                           'newaccounts': newaccounts,
                                           'accountsall': accountsall,
                                           'leads_current_month': leads_current_month,
                                           'leads_conversionrate': leads_conversionrate,
                                           'opportunity_current_month': opportunity_current_month,
                                           'opportunity_conversionrate': opportunity_conversionrate,
                                           'opportunity_show': opportunity_show,
                                           'leads_show':leads_show,
                                           'meeting': meeting,
                                           })