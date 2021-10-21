from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ( ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete,
                        )

app_name="project"

urlpatterns = [
    path('', ProjectList.as_view(),name="project"),
    path('create/', ProjectCreate.as_view(),name="project-create"),
    path('update/<int:pk>', ProjectUpdate.as_view(),name="project-update"),
    path('delete/<int:pk>', ProjectDelete.as_view(),name="project-delete"),

]