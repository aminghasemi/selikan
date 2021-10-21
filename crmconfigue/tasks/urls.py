from django.urls import path, re_path, reverse
from django.contrib.auth import views
from django.conf.urls import url

from .views import ( TaskList, TaskCreate, TaskUpdate, TaskDelete,
                     TaskListAll, TaskList_daily, TaskList_weekly, TaskList_monthly, TaskList_call,
                     TaskSubjectList, TaskSubjectCreate, TaskSubjectUpdate, TaskSubjectDelete,
                     TaskList_call, TaskList_meeting, TaskList_email, TaskList_preinvoice, TaskList_invoice, TaskList_followup,
                     TaskList_contract, TaskList_catalog, TaskList_proposal )

app_name="task"

urlpatterns = [
    path('', TaskList.as_view(),name="task"),
    path('all', TaskListAll.as_view(),name="task-all"),
    path('daily', TaskList_daily.as_view(),name="task-daily"),
    path('weekly', TaskList_weekly.as_view(),name="task-weekly"),
    path('monthly', TaskList_monthly.as_view(),name="task-monthly"),

    path('call', TaskList_call.as_view(),name="task-call"),
    path('meeting', TaskList_meeting.as_view(),name="task-meeting"),
    path('email', TaskList_email.as_view(),name="task-email"),
    path('preinvoice', TaskList_preinvoice.as_view(),name="task-preinvoice"),
    path('invoice', TaskList_invoice.as_view(),name="task-invoice"),
    path('followup', TaskList_followup.as_view(),name="task-followup"),
    path('contract', TaskList_contract.as_view(),name="task-contract"),
    path('catalog', TaskList_catalog.as_view(),name="task-catalog"),
    path('proposal', TaskList_proposal.as_view(),name="task-proposal"),


    path('create/', TaskCreate.as_view(),name="task-create"),
    path('update/<int:pk>', TaskUpdate.as_view(),name="task-update"),
    path('delete/<int:pk>', TaskDelete.as_view(),name="task-delete"),

    path('tasksubject', TaskSubjectList.as_view(),name="tasksubject"),
    path('tasksubject/create/', TaskSubjectCreate.as_view(),name="tasksubject-create"),
    path('tasksubject/update/<int:pk>', TaskSubjectUpdate.as_view(),name="tasksubject-update"),
    path('tasksubject/delete/<int:pk>', TaskSubjectDelete.as_view(),name="tasksubject-delete"),

]
