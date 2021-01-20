from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from common.decorators import company_enrolled
from .models import Teams
from common.mixins import EnrollMixin, SuperUserAccessMixin, CreatorAccessMixin
# Create your views here.

@login_required(login_url='login')
@company_enrolled
def TeamsList(request, slug):
    template_name = 'company/teams.html'
    company = get_object_or_404(Company, slug=slug)
    teams = company.companyteams.all()
    return render(request, template_name, {'company': company,
                                           'teams': teams,})


#class TeamsList(LoginRequiredMixin,ListView):
#        queryset= Teams.objects.all()
#        template_name="company/teams.html"
class TeamCreate(LoginRequiredMixin, CreateView):
    model=Teams
    fields=["name", "description", "users","company"]
    template_name="company/team-create-update.html"
    success_url= reverse_lazy('teams:teams')
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TeamUpdate(LoginRequiredMixin, UpdateView):
    model=Teams
    fields=["name", "description", "users","company"]
    template_name = "company/team-create-update.html"
    success_url= reverse_lazy('teams:teams')
class TeamDelete(LoginRequiredMixin, DeleteView):
    model=Teams
    template_name = "company/team_confirm_delete.html"
    success_url= reverse_lazy('teams:teams')