from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import Dealreportlist, DealreportCreate, DealreportUpdate, DealreportDelete, Dealreport_detail

app_name="reports"

urlpatterns = [
    path('dealreports', Dealreportlist.as_view(),name="dealreports"),
    path('dealreports/create/', DealreportCreate.as_view(),name="dealreport-create"),
    path('dealreports/update/<int:pk>', DealreportUpdate.as_view(),name="dealreport-update"),
    path('dealreports/delete/<int:pk>', DealreportDelete.as_view(),name="dealreport-delete"),
    path('dealreports/report/<int:pk>', Dealreport_detail,name="dealreport-detail"),



]
