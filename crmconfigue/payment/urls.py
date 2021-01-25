# Github.com/Rasooll
from django.conf.urls import url
from django.urls import path
from . import views
from .views import BillingCreate
app_name= "payment"



urlpatterns = [
    path('create/', BillingCreate.as_view(),name="billing-create"),
    url(r'^request/$', views.send_request, name='request'),
    url(r'^verify/$', views.verify , name='verify'),
]
