from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import TeamsList, TeamCreate, TeamUpdate, TeamDelete

app_name="teams"

urlpatterns = [
    path('', TeamsList,name="teams"),
    path('create/', TeamCreate.as_view(),name="team-create"),
    path('update/<int:pk>', TeamUpdate.as_view(),name="team-update"),
    path('delete/<int:pk>', TeamDelete.as_view(),name="team-delete"),


]
