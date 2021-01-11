from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Company


class EnrollMixin():
    def dispatch(self,request, *args, **kwargs):
        if request.user.staff__user.exists() or request.user.staff__user.exists() or self.request.user.is_superuser:
            new_classworks = None

        return super().dispatch(request, *args, **kwargs)
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
