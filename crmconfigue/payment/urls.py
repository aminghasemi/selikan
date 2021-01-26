# Github.com/Rasooll
from django.conf.urls import url
from django.urls import path
from . import views
from .views import BillingCreate, BillingPreview, send_request, BillingList, BillingDetail


app_name= "payment"


urlpatterns = [
    path('create/', BillingCreate.as_view(),name="billing-create"),
    path('preview/<int:pk>', BillingPreview.as_view(), name="billing-preview"),
    path('list/', BillingList.as_view(),name="billing-list"),
    path('detail/<int:pk>', BillingDetail.as_view(),name="billing-detail"),
    url(r'^verify/$', views.verify , name='verify'),
]
