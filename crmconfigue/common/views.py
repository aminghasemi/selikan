from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from cuser.middleware import CuserMiddleware
from itertools import chain
from .models import Company, User
from .mixins import CreatorAccessMixin, SuperUserAccessMixin, SpecialCompanyMixin
from .decorators import allowed_users, company_enrolled, user_limit
from .forms import EnrollForm, ProfileForm
from django.contrib.auth.views import LoginView, PasswordChangeView


# Create your views here.


class CompaniesList(LoginRequiredMixin, ListView):
        queryset= Company.objects.all()
        template_name="registration/home.html"
        def get_queryset(self):
            if self.request.user.is_superuser:
                return Company.objects.all()
            else:
                class1=Company.objects.filter(creator=self.request.user)
                class2=Company.objects.filter(staff=self.request.user)
                class3=chain(class1,class2)
                return class3

class CompanyCreate(LoginRequiredMixin, CreateView):
    model=Company
    fields=["name", "address", "slug",]
    template_name="registration/Company-create-update.html"
    success_url= reverse_lazy('common:home')
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CompanyUpdate(LoginRequiredMixin,CreatorAccessMixin, UpdateView):
    model=Company
    fields=["name", "address",]
    template_name = "registration/Company-create-update.html"
    success_url= reverse_lazy('common:home')
class CompanyDelete(LoginRequiredMixin,CreatorAccessMixin, DeleteView):
    model=Company
    template_name = "registration/Company_confirm_delete.html"
    success_url= reverse_lazy('common:home')


@login_required(login_url='login')
@company_enrolled
@user_limit
def company_staff(request, slug):
    template_name = 'registration/company_add_staff.html'
    #company=Company.objects.get(slug=slug)
    company = get_object_or_404(Company, slug=slug)
    companystaff = company.staff_enroll.all()
    new_staff = None
    if request.method == 'POST':
        def form_valid(self, form):
            form.instance.company = company
            return super(company_staff, self).form_valid(form)
        enroll_form = EnrollForm(data=request.POST)
        if enroll_form.is_valid():

            # Create Comment object but don't save to database yet
            new_staff = enroll_form.save(commit=False)
            # Assign the current post to the comment
            new_staff.company = company
            # Save the comment to the database
            new_staff.save()
    else:
        enroll_form = EnrollForm()
    return render(request, template_name, {'companystaff': companystaff,
                                           'company': company,
                                           'new_staff': new_staff,
                                           'enroll_form': enroll_form,})

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

		if user.is_superuser or user.is_author:
			return reverse_lazy("common:home")
		else:
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