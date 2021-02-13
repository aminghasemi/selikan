from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from common.models import Company
from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Contact
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
from .forms import ContactForm
# Create your views here.

class ContactsList(EnrollMixin, LoginRequiredMixin,ListView):
    template_name = 'company/contacts/contacts.html'
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycontacts.all()
    def get_context_data(self, **kwargs):
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context

class ContactCreate(LoginRequiredMixin, CreateView):
    model=Contact
    form_class=ContactForm
    template_name="company/contacts/contact-create.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycontacts.all()
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
        return reverse_lazy('contacts:contacts', kwargs={'slug': slug}, current_app='contacts')

class ContactUpdate(LoginRequiredMixin, UpdateView):
    model=Contact
    form_class=ContactForm
    template_name = "company/contacts/contact-update.html"
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('contacts:contacts', kwargs={'slug': slug}, current_app='contacts')
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycontacts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        pk=self.kwargs.get('pk')
        context['docs']=company.companydocs.filter(contacts_id=pk)
        return context
class ContactDelete(LoginRequiredMixin, DeleteView):
    model=Contact
    template_name = "company/contacts/contact_confirm_delete.html"
    def get_queryset(self):
        global company
        slug= self.kwargs.get('slug')
        company = get_object_or_404(Company , slug=slug)
        return company.companycontacts.all()
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['company'] = company
        return context
    def get_success_url(self):
        slug= self.kwargs.get('slug')
        return reverse_lazy('contacts:contacts', kwargs={'slug': slug}, current_app='contacts')