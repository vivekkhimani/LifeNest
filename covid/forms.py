from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from covid.models import Supplier, Requester, Service
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class MyUserChangeForm(UserChangeForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


class MyUserCreationForm(UserCreationForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('state', 'city', 'phone', 'instagramHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')


class RequesterForm(forms.ModelForm):
    class Meta:
        model = Requester
        fields = ('state', 'city', 'phone', 'instagramHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')
