from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ContactsList, ContactCreate, ContactUpdate, ContactDelete

app_name="contacts"

urlpatterns = [
    path('', ContactsList.as_view(),name="contacts"),
    path('create/', ContactCreate.as_view(),name="contact-create"),
    path('update/<int:pk>', ContactUpdate.as_view(),name="contact-update"),
    path('delete/<int:pk>', ContactDelete.as_view(),name="contact-delete"),



]
