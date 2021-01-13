from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Company, Enrolled

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group= None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('شما اجازه دسترسی به این صفحه را ندارید.')
        return wrapper_func
    return decorator

def company_enrolled(view_func):
    def wrapper_func(request, slug, *args, **kwargs):
        #classroom=class_room.objects.get(slug=slug)
        company= get_object_or_404(Company, slug=slug)
        if  request.user in company.staff.all() or  company.creator == request.user or request.user.is_superuser:
        #if classroom.objects.get(students=request.user.profile) or classroom.objects.get(teachers=request.user.profile):
            return view_func(request, slug, *args, **kwargs)
        else:
            return HttpResponse('شما در این شرکت عضو نیستید')
    return wrapper_func
