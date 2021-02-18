from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Company
from django.utils import timezone


class EnrollMixin():
    def dispatch(self, request, slug, *args, **kwargs):
        company= get_object_or_404(Company, slug=slug)
        if  request.user in company.staff.all() or  company.creator == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")
class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")
class CreatorAccessMixin():
    def dispatch(self, request, slug, *args, **kwargs):
        company= get_object_or_404(Company, slug=slug)
        if company.creator == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید.")
class SpecialCompanyMixin():
    def dispatch(self, request, *args, **kwargs):
        slug= self.kwargs.get('slug')
        company= get_object_or_404(Company, slug=slug)
        if company.access_date>timezone.now():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("مدت زمان اعتبار این شرکت به پایان رسیده است.")