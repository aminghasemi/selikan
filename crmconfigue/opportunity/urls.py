from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ( OpportunityList, OpportunityCreate, OpportunityUpdate, OpportunityDelete,
                     OpportunityStatusList, OpportunityStatusCreate,OpportunityStatusUpdate,OpportunityStatusDelete,
                     OpportunitySourceList,OpportunitySourceCreate,OpportunitySourceUpdate,OpportunitySourceDelete,
                     OpportunityListAll,OpportunityList_today,OpportunityList_3days, OpportunityList_10days )

app_name="opportunity"

urlpatterns = [
    path('', OpportunityList.as_view(),name="opportunity"),
    path('all', OpportunityListAll.as_view(),name="opportunity-all"),
    path('today', OpportunityList_today.as_view(),name="opportunity-today"),
    path('3days', OpportunityList_3days.as_view(),name="opportunity-3days"),
    path('10days', OpportunityList_10days.as_view(),name="opportunity-10days"),


    path('create/', OpportunityCreate.as_view(),name="opportunity-create"),
    path('update/<int:pk>', OpportunityUpdate.as_view(),name="opportunity-update"),
    path('delete/<int:pk>', OpportunityDelete.as_view(),name="opportunity-delete"),
    path('opportunitystatus', OpportunityStatusList.as_view(),name="opportunitystatus"),
    path('opportunitystatus/create/', OpportunityStatusCreate.as_view(),name="opportunitystatus-create"),
    path('opportunitystatus/update/<int:pk>', OpportunityStatusUpdate.as_view(),name="opportunitystatus-update"),
    path('opportunitystatus/delete/<int:pk>', OpportunityStatusDelete.as_view(),name="opportunitystatus-delete"),
    path('opportunitysource', OpportunitySourceList.as_view(),name="opportunitysource"),
    path('opportunitysource/create/', OpportunitySourceCreate.as_view(),name="opportunitysource-create"),
    path('opportunitysource/update/<int:pk>', OpportunitySourceUpdate.as_view(),name="opportunitysource-update"),
    path('opportunitysource/delete/<int:pk>', OpportunitySourceDelete.as_view(),name="opportunitysource-delete"),



]
