from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete

app_name="task"

urlpatterns = [
    path('', TaskList.as_view(),name="task"),
    path('create/', TaskCreate.as_view(),name="task-create"),
    path('update/<int:pk>', TaskUpdate.as_view(),name="task-update"),
    path('delete/<int:pk>', TaskDelete.as_view(),name="task-delete"),



]
