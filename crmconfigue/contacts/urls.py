from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ContactsList

app_name="contacts"

urlpatterns = [
    path('', ContactsList.as_view(),name="contacts"),



]
