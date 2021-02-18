from .models import Enrolled
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Company
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields=("name","slug","country","national_id","thumbnail", "economic_id",
		 "email","phone","office_phone", "fax", "industry","billing_address_line","billing_street",
		 "billing_city", "billing_state", "billing_postcode", "website", "description", "is_active")


class EnrollForm(forms.ModelForm):
    class Meta:
        model= Enrolled
        fields= ('staff','company')


class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=200)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')

		super(ProfileForm, self).__init__(*args, **kwargs)

		self.fields['username'].help_text = None
		
		if not user.is_superuser:
			self.fields['username'].disabled = True
			self.fields['email'].disabled = True
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name','role', 'has_sales_access', 'has_marketing_access','thumbnail']
