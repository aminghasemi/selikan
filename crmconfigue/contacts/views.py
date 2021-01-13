from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Contact
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class ContactsList(LoginRequiredMixin,EnrollMixin,ListView):
        queryset= Contact.objects.all()
        template_name="company/contacts.html"
