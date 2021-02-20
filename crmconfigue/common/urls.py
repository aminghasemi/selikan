from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import Dashboard, home,EnrollCreate, CompaniesList, CompanyCreate, CompanyUpdate, CompanyDelete, company_staff,StaffDelete, Profile ,ProductsList,ProductCreate,ProductUpdate,ProductDelete, CountriesList, CountryCreate, CountryUpdate, CountryDelete

app_name="common"
urlpatterns = [
    path('', home,name="statichome"),
    path('account', CompaniesList.as_view(),name="home"),
    path('create/', CompanyCreate.as_view(),name="company-create"),
    path('update/<slug:slug>', CompanyUpdate.as_view(),name="company-update"),
    path('delete/<slug:slug>', CompanyDelete.as_view(),name="company-delete"),

    path('<slug:slug>/addstaff',company_staff,name="company_add_staff"),
    path('deletestaff/<slug:slug>/<int:pk>', StaffDelete.as_view(),name="staff-delete"),
    path('addstaff/', EnrollCreate.as_view(),name="enroll"),

    path('profile/', Profile.as_view(), name="profile"),
	path('<slug:slug>/dashboard/', Dashboard, name="dashboard"),
    path('<slug:slug>/products/', ProductsList.as_view(),name="products"),
    path('<slug:slug>/products/create/', ProductCreate.as_view(),name="product-create"),
    path('<slug:slug>/products/update/<int:pk>', ProductUpdate.as_view(),name="product-update"),
    path('<slug:slug>/products/delete/<int:pk>', ProductDelete.as_view(),name="product-delete"),

    path('<slug:slug>/countries/', CountriesList.as_view(),name="countries"),
    path('<slug:slug>/countries/create/', CountryCreate.as_view(),name="country-create"),
    path('<slug:slug>/countries/update/<int:pk>', CountryUpdate.as_view(),name="country-update"),
    path('<slug:slug>/countries/delete/<int:pk>', CountryDelete.as_view(),name="country-delete"),
]
