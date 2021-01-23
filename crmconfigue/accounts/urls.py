from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import AccountsList, AccountCreate, AccountUpdate, AccountDelete

app_name="accounts"

urlpatterns = [
    path('', AccountsList.as_view(),name="accounts"),
    path('create/', AccountCreate.as_view(),name="account-create"),
    path('update/<int:pk>', AccountUpdate.as_view(),name="account-update"),
    path('delete/<int:pk>', AccountDelete.as_view(),name="account-delete"),



]
