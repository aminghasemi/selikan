from .models import Enrolled
from django import forms



class EnrollForm(forms.ModelForm):
    class Meta:
        model= Enrolled
        fields= ('staff','company')


