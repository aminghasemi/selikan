from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Contact
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.

@login_required(login_url='login')
@company_enrolled
def ContactsList(request, slug):
    template_name = 'company/contacts.html'
    company = get_object_or_404(Company, slug=slug)
    contacts = company.companycontacts.all()
    return render(request, template_name, {'company': company,
                                           'contacts': contacts,})

#class ContactsList(LoginRequiredMixin,ListView):
  #      queryset= Contact.objects.all()
  #      template_name="company/contacts.html"
class ContactCreate(LoginRequiredMixin, CreateView):
    model=Contact
    fields=["first_name", "last_name", "email","phone","office_phone", "address", "description", "assigned_to", "is_active"]
    template_name="company/contact-create-update.html"
    success_url= reverse_lazy('contacts:contacts')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ContactUpdate(LoginRequiredMixin, UpdateView):
    model=Contact
    fields=["first_name", "last_name", "email","phone", "address", "description", "assigned_to", "is_active"]
    template_name = "company/contact-create-update.html"
    success_url= reverse_lazy('contacts:contacts')
class ContactDelete(LoginRequiredMixin, DeleteView):
    model=Contact
    template_name = "company/contact_confirm_delete.html"
    success_url= reverse_lazy('contacts:contacts')
