from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import CompaniesList, CompanyCreate, CompanyUpdate, CompanyDelete, company_staff, Profile

app_name="common"
urlpatterns = [
    path('', CompaniesList.as_view(),name="home"),
    path('create/', CompanyCreate.as_view(),name="company-create"),
    path('update/<slug:slug>', CompanyUpdate.as_view(),name="company-update"),
    path('delete/<slug:slug>', CompanyDelete.as_view(),name="company-delete"),
    path('addstaff/<slug:slug>',company_staff,name="company_add_staff"),
    path('profile/', Profile.as_view(), name="profile"),

]
