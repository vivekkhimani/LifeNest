from django import forms
from django.contrib.auth.models import User
from covid.models import Participant, Service
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username_entry = self.cleaned_data['username']
        try:
            user = Participant.objects.get(user__username=username_entry)
        except Participant.DoesNotExist as ex:
            raise forms.ValidationError("The user does not exist.")
        return username_entry


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class ParticipantForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, help_text='I agree to provide the following details.')

    class Meta:
        model = Participant
        fields = ('state', 'city', 'phone', 'instagramHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')
