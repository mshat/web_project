from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

from django.contrib.auth.models import User
from .models import Type

from .models import Backpack

class RegistrationForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, help_text="Password length must be >= 6 chars.")

    def clean_password(self):
        password_data = self.cleaned_data['password']

        if len(password_data) < 6:
            raise ValidationError(_('Password is too short')) 
        return password_data

    def clean_login(self):
        login_data = self.cleaned_data['login']
        if User.objects.filter(username=login_data):
            raise ValidationError(_('This username already exists')) 
        return login_data

class CartAddBackpackForm(forms.Form):
    number = forms.TypedChoiceField(coerce=int)

    def __init__(self, number_choices, *args, **kwargs):
        super(CartAddBackpackForm,self).__init__(*args,**kwargs)
        self.fields['number'].choices = number_choices

class TypeCreateForm(forms.Form):
    type = forms.CharField(max_length=200, help_text="Enter a type (e.g. Tourism backpack, city backpack etc.)")

    def clean_type(self):
        type_data = self.cleaned_data['type']

        if Type.objects.filter(type=type_data):
            raise ValidationError(_('This type already exists')) 
        return type_data
