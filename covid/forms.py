from django import forms
from django.contrib.auth.models import User
from covid.models import Participant, Service
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username_entry = self.cleaned_data['username']
        try:
            participant = Participant.objects.get(user__username=username_entry)
            if not participant.user.is_active:
                raise forms.ValidationError("The account for this user has been deactivated.")
        except Participant.DoesNotExist as ex:
            raise forms.ValidationError("The user does not exist.")
        return username_entry


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True, help_text="Will be required for password reset.")

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


class ServiceForm(forms.ModelForm):
    pricing_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Price Specifications (Only required if the resource is paid)", help_text="Pricer per unit. Example: xxx INR per oxygen cylinder.")
    delivery_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Delivery Specification (Only required if you avail delivery)", help_text="More information required for delivery (pricing, restrictions, etc.)")
    additional_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, help_text="Any additional details or restrictions about the availability of your service.")

    class Meta:
        model = Service
        exclude = ('provider', 'created', 'humanVerified')



