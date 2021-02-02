from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import InvoiceCreate,InvoiceDelete,InvoiceUpdate,InvoiceList

app_name="invoice"

urlpatterns = [
    path('', InvoiceList.as_view(),name="invoices"),
    path('create/', InvoiceCreate.as_view(),name="invoice-create"),
    path('update/<int:pk>', InvoiceUpdate.as_view(),name="invoice-update"),
    path('delete/<int:pk>', InvoiceDelete.as_view(),name="invoice-delete"),
]