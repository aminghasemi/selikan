from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import (
    Dealreportlist, DealreportCreate, DealreportUpdate, DealreportDelete, Dealreport_detail,
    Leadreportlist, LeadreportCreate, LeadreportUpdate, LeadreportDelete, Leadreport_detail,
    Opportunityreportlist, OpportunityreportCreate, OpportunityreportUpdate, OpportunityreportDelete, Opportunityreport_detail,
)
app_name="reports"

urlpatterns = [
    path('dealreports', Dealreportlist.as_view(),name="dealreports"),
    path('dealreports/create/', DealreportCreate.as_view(),name="dealreport-create"),
    path('dealreports/update/<int:pk>', DealreportUpdate.as_view(),name="dealreport-update"),
    path('dealreports/delete/<int:pk>', DealreportDelete.as_view(),name="dealreport-delete"),
    path('dealreports/report/<int:pk>', Dealreport_detail,name="dealreport-detail"),
    path('leadreports', Leadreportlist.as_view(),name="leadreports"),
    path('leadreports/create/', LeadreportCreate.as_view(),name="leadreport-create"),
    path('leadreports/update/<int:pk>', LeadreportUpdate.as_view(),name="leadreport-update"),
    path('leadreports/delete/<int:pk>', LeadreportDelete.as_view(),name="leadreport-delete"),
    path('leadreports/report/<int:pk>', Leadreport_detail,name="leadreport-detail"),
    path('opportunityreports', Opportunityreportlist.as_view(),name="opportunityreports"),
    path('opportunityreports/create/', OpportunityreportCreate.as_view(),name="opportunityreport-create"),
    path('opportunityreports/update/<int:pk>', OpportunityreportUpdate.as_view(),name="opportunityreport-update"),
    path('opportunityreports/delete/<int:pk>', OpportunityreportDelete.as_view(),name="opportunityreport-delete"),
    path('opportunityreports/report/<int:pk>', Opportunityreport_detail,name="opportunityreport-detail"),

]
