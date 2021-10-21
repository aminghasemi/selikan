from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ( LeadsList, LeadCreate, LeadUpdate,
                     LeadDelete,LeadStatusList, LeadStatusCreate,LeadStatusUpdate,LeadStatusDelete,
                     LeadSourceList,LeadSourceCreate,LeadSourceUpdate,LeadSourceDelete,
                     LeadsListAll,LeadsList_today,LeadsList_3days, LeadsList_10days )
app_name="leads"

urlpatterns = [
    path('', LeadsList.as_view(),name="leads"),
    path('all', LeadsListAll.as_view(),name="leads-all"),
    path('today', LeadsList_today.as_view(),name="leads-today"),
    path('3days', LeadsList_3days.as_view(),name="leads-3days"),
    path('10days', LeadsList_10days.as_view(),name="leads-10days"),

    path('create/', LeadCreate.as_view(),name="lead-create"),
    path('update/<int:pk>', LeadUpdate.as_view(),name="lead-update"),
    path('delete/<int:pk>', LeadDelete.as_view(),name="lead-delete"),
    path('leadstatus', LeadStatusList.as_view(),name="leadstatus"),
    path('leadstatus/create/', LeadStatusCreate.as_view(),name="leadstatus-create"),
    path('leadstatus/update/<int:pk>', LeadStatusUpdate.as_view(),name="leadstatus-update"),
    path('leadstatus/delete/<int:pk>', LeadStatusDelete.as_view(),name="leadstatus-delete"),
    path('leadsource', LeadSourceList.as_view(),name="leadsource"),
    path('leadsource/create/', LeadSourceCreate.as_view(),name="leadsource-create"),
    path('leadsource/update/<int:pk>', LeadSourceUpdate.as_view(),name="leadsource-update"),
    path('leadsource/delete/<int:pk>', LeadSourceDelete.as_view(),name="leadsource-delete"),

]
