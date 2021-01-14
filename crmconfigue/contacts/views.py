from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Contact
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class ContactsList(LoginRequiredMixin,ListView):
        queryset= Contact.objects.all()
        template_name="company/contacts.html"
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
