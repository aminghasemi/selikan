from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import TargetsubjectList,TargetsubjectCreate,TargetsubjectUpdate,TargetsubjectDelete,CompanyTargetsList,CompanyTargetsCreate,CompanyTargetsUpdate,CompanyTargetsDelete,StaffTargetsList,StaffTargetsCreate,StaffTargetsUpdate,StaffTargetsDelete
app_name="targets"

urlpatterns = [
    path('companytargets', CompanyTargetsList.as_view(),name="companytargets"),
    path('companytargets/create/', CompanyTargetsCreate.as_view(),name="companytargets-create"),
    path('companytargets/update/<int:pk>', CompanyTargetsUpdate.as_view(),name="companytargets-update"),
    path('companytargets/delete/<int:pk>', CompanyTargetsDelete.as_view(),name="companytargets-delete"),
    path('stafftargets', StaffTargetsList.as_view(),name="stafftargets"),
    path('stafftargets/create/', StaffTargetsCreate.as_view(),name="stafftargets-create"),
    path('stafftargets/update/<int:pk>', StaffTargetsUpdate.as_view(),name="stafftargets-update"),
    path('stafftargets/delete/<int:pk>', StaffTargetsDelete.as_view(),name="stafftargets-delete"),
    path('targetsubjectlist', TargetsubjectList.as_view(),name="targetsubjectlist"),
    path('targetsubjects/create/', TargetsubjectCreate.as_view(),name="targetsubjects-create"),
    path('targetsubjects/update/<int:pk>', TargetsubjectUpdate.as_view(),name="targetsubjects-update"),
    path('targetsubjects/delete/<int:pk>', TargetsubjectDelete.as_view(),name="targetsubjects-delete"),

]
