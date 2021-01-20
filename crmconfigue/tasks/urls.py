from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete

app_name="task"

urlpatterns = [
    path('<slug:slug>/tasks', TaskList,name="task"),
    path('<slug:slug>/tasks/create/', TaskCreate,name="task-create"),
    path('tasks/update/<int:pk>', TaskUpdate.as_view(),name="task-update"),
    path('tasks/delete/<int:pk>', TaskDelete.as_view(),name="task-delete"),



]
