from django import forms
from django.contrib.auth.models import User
from covid.models import Participant, Service, Spammer
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
    email = forms.EmailField(required=True, help_text="CANNOT be updated later. Will be required for password reset.")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class UpdateUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class ParticipantForm(forms.ModelForm):
    consent = forms.BooleanField(required=True,
                                 help_text="I acknowledge that the details entered by me are correct. In case of spam reports against this posting, I am bound to being banned from this platform.")

    class Meta:
        model = Participant
        fields = ('state', 'city', 'phone', 'instagramHandle', 'twitterHandle',
                  'facebookHandle', 'website', 'consent')
        exclude = ('verifiedPhone', 'verifiedEmail', 'num_scams', 'num_helps')


class UpdateParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('state', 'city', 'instagramHandle', 'twitterHandle', 'facebookHandle', 'website')
        exclude = ('verifiedPhone', 'verifiedEmail', 'num_scams', 'num_helps', 'phone', 'consent')


class SpammerForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=True,
                             help_text="Reason for reporting this phone as spam. Your spam entry may be removed if the reason is not satisfactory.")

    def __init__(self, *args, **kwargs):
        self.reporter = kwargs.pop('reporter', None)
        super(SpammerForm, self).__init__(*args, **kwargs)

    def clean(self):
        # manually verifying unique together constraint
        cleaned_data = self.cleaned_data
        get_phone = self.cleaned_data.get('phone', None)
        if not get_phone:
            return cleaned_data
        if Spammer.objects.filter(reporter=self.reporter, phone=get_phone).exists():
            raise forms.ValidationError({"phone": 'You have already reported a spam against this number. Cannot do it again.'})
        return cleaned_data

    class Meta:
        model = Spammer
        fields = ('phone', 'reason', 'consent')


class ServiceForm(forms.ModelForm):
    consent = forms.BooleanField(required=True,
                                 help_text="I acknowledge that the details entered by me are correct. In case of spam reports against this posting, I am bound to being banned from this platform.")
    pricing_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False,
                                      label="Price Specifications (Only required if the resource is paid)",
                                      help_text="Price per unit of the resource. Example: ₹x per oxygen cylinder, ₹x per ventilator bed, etc.")
    delivery_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False,
                                       label="Delivery Specification (Only required if you provide delivery)",
                                       help_text="More information required for delivery (pricing, restrictions, etc.)")
    additional_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False,
                                         help_text="Any additional details or restrictions about the resource.")

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
        exclude = ('provider', 'created', 'scam_votes', 'help_votes')
