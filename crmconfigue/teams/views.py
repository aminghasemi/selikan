from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy



from .models import Teams
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.


class TeamsList(LoginRequiredMixin,ListView):
        queryset= Teams.objects.all()
        template_name="company/teams.html"
class TeamCreate(LoginRequiredMixin, CreateView):
    model=Teams
    fields=["name", "description", "users","company"]
    template_name="registration/Company-create-update.html"
    success_url= reverse_lazy('common:home')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TeamUpdate(LoginRequiredMixin,CreatorAccessMixin, UpdateView):
    model=Teams
    fields=["name", "description", "users","created_by","company"]
    template_name = "registration/team-create-update.html"
    success_url= reverse_lazy('teams:teams')
class TeamDelete(LoginRequiredMixin,CreatorAccessMixin, DeleteView):
    model=Teams
    template_name = "registration/team_confirm_delete.html"
    success_url= reverse_lazy('teams:teams')