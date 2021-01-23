from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import LeadsList, LeadCreate, LeadUpdate, LeadDelete

app_name="leads"

urlpatterns = [
    path('', LeadsList.as_view(),name="leads"),
    path('create/', LeadCreate.as_view(),name="lead-create"),
    path('update/<int:pk>', LeadUpdate.as_view(),name="lead-update"),
    path('delete/<int:pk>', LeadDelete.as_view(),name="lead-delete"),



]
