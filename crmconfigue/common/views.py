from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from cuser.middleware import CuserMiddleware
from itertools import chain
from .models import Company
from .mixins import CreatorAccessMixin, SuperUserAccessMixin
from .decorators import allowed_users, company_enrolled

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


@login_required(login_url='account:login')
@company_enrolled
def class_student(request, slug):
    template_name = 'registration/Company-create-update.html'
    company = get_object_or_404(Company, slug=slug)
    staff = company.staff_enroll.all()
    new_staff = None
    if request.method == 'POST':
        def form_valid(self, form):
            form.instance.company = company
            return super(staff, self).form_valid(form)
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
    return render(request, template_name, {'staff': staff,
                                           'company': company,
                                           'new_staff': new_staff,
                                           'enroll_form': enroll_form,})