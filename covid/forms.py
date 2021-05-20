from django import forms
from django.contrib.auth.models import User
from covid.models import Supplier, Requester, Service
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class SupplierForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, help_text='I agree to provide the following details.')

    class Meta:
        model = Supplier
        fields = ('state', 'city', 'phone', 'instagramHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')


class RequesterForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, help_text='I agree to provide the following details.')

    class Meta:
        model = Requester
        fields = ('state', 'city', 'phone', 'instagramHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')
