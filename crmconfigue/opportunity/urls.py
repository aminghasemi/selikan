from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import OpportunityList, OpportunityCreate, OpportunityUpdate, OpportunityDelete

app_name="opportunity"

urlpatterns = [
    path('', OpportunityList.as_view(),name="opportunity"),
    path('create/', OpportunityCreate.as_view(),name="opportunity-create"),
    path('update/<int:pk>', OpportunityUpdate.as_view(),name="opportunity-update"),
    path('delete/<int:pk>', OpportunityDelete.as_view(),name="opportunity-delete"),



]
