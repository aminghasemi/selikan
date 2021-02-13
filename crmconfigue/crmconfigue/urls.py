"""crmconfigue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views
from common.views import Login, Register, activate
from payment.views import send_request
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('<slug:slug>/teams/', include('teams.urls')),
    path('<slug:slug>/contacts/', include('contacts.urls')),
    path('<slug:slug>/deals/', include('deals.urls')),
    path('<slug:slug>/leads/', include('lead.urls')),
    path('<slug:slug>/accounts/', include('accounts.urls')),
    path('<slug:slug>/opportunity/', include('opportunity.urls')),
    path('<slug:slug>/tasks/', include('tasks.urls')),
    path('<slug:slug>/payment/', include('payment.urls')),
    path('<slug:slug>/invoice/', include('invoice.urls')),
    path('<slug:slug>/docs/', include('docs.urls')),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('<int:pk>/request', send_request, name='request'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
