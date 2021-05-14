from django import forms
from django.contrib.auth.models import User
from covid.models import Supplier, Requester, Service


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
