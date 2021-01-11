from .models import Enrolled
from django import forms
from account.models import Profile
from .mixins import FieldsMixin



class EnrollForm(forms.ModelForm):
    class Meta:
        model= Enrolled
        fields= ('staff',)


