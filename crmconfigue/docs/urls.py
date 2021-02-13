from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import DocList, DocCreate, DocUpdate, DocDelete

app_name="doc"

urlpatterns = [
    path('', DocList.as_view(),name="docs"),
    path('create/', DocCreate.as_view(),name="doc-create"),
    path('update/<int:pk>', DocUpdate.as_view(),name="doc-update"),
    path('delete/<int:pk>', DocDelete.as_view(),name="doc-delete"),



]
