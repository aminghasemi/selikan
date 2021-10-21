from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ( DealsList, DealCreate, DealUpdate, DealDelete,
                     PipelinesList, PipelineCreate, PipelineUpdate, PipelineDelete,
                     DealsListAll, DealsList_today, DealsList_3days, DealsList_10days )

app_name="deals"

urlpatterns = [
    path('', DealsList.as_view(),name="deals"),
    path('all', DealsListAll.as_view(),name="deals-all"),
    path('today', DealsList_today.as_view(),name="deals-today"),
    path('3days', DealsList_3days.as_view(),name="deals-3days"),
    path('10days', DealsList_10days.as_view(),name="deals-10days"),

    path('create/', DealCreate.as_view(),name="deal-create"),
    path('update/<int:pk>', DealUpdate.as_view(),name="deal-update"),
    path('delete/<int:pk>', DealDelete.as_view(),name="deal-delete"),
    path('pipeline', PipelinesList.as_view(),name="pipelines"),
    path('pipeline/create/', PipelineCreate.as_view(),name="pipeline-create"),
    path('pipeline/update/<int:pk>', PipelineUpdate.as_view(),name="pipeline-update"),
    path('pipeline/delete/<int:pk>', PipelineDelete.as_view(),name="pipeline-delete"),


]
