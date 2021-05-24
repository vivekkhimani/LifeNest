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
    email = forms.EmailField(required=True, help_text="Will be required for password reset.")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class ParticipantForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, help_text="I acknowledge that the details entered by me are correct. In case of spam reports against this posting, I am bound to being banned from this platform.")

    class Meta:
        model = Participant
        fields = ('state', 'city', 'phone', 'instagramHandle', 'twitterHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'humanVerified')


class ServiceForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, help_text="I acknowledge that the details entered by me are correct. In case of spam reports against this posting, I am bound to being banned from this platform.")
    pricing_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Price Specifications (Only required if the resource is paid)", help_text="Price per unit of the resource. Example: ₹x per oxygen cylinder, ₹x per ventilator bed, etc.")
    delivery_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, label="Delivery Specification (Only required if you provide delivery)", help_text="More information required for delivery (pricing, restrictions, etc.)")
    additional_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False, help_text="Any additional details or restrictions about the resource.")

    def clean_delivery_type(self):
        delivery = self.cleaned_data['delivery']
        if not delivery:
            return ''
        return self.cleaned_data['delivery_type']

    def clean_delivery_details(self):
        delivery = self.cleaned_data['delivery']
        if not delivery:
            return ''
        return self.cleaned_data['delivery_details']

    def clean_pricing_details(self):
        price = self.cleaned_data['price']
        if price == 'FREE':
            return ''
        return self.cleaned_data['pricing_details']

    class Meta:
        model = Service
        exclude = ('provider', 'created', 'humanVerified')



