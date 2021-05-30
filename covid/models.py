from django.db import models

# Create your models here.
"""
models.py
"""
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone

STATE_CHOICES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chattisgarh', 'Chattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman & Nicobar', 'Andaman & Nicobar'),
    ('Chandigarh', 'Chandigarh'),
    ('Delhi', 'Delhi'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]

PAYMENT_CHOICES = [
    ('PAID', 'PAID'),
    ('FREE', 'FREE'),
]

SERVICE_CHOICES = [
    ('Oxygen', 'Oxygen'),
    ('Medications (no Remdesivir)', 'Medications (no Remdesivir)'),
    ('Remdesivir', 'Remdesivir'),
    ('Hospital Beds', 'Hospital Beds'),
    ('Ventilator Beds', 'Ventilator Beds'),
    ('Home-made Food', 'Home-made Food'),
    ('Ambulance', 'Ambulance'),
    ('Monetary Donations', 'Monetary Donations'),
    ('Plasma Donations', 'Plasma Donations'),
    ('Laboratory Testing', 'Laboratory Testing'),
    ('Vaccine Clinics', 'Vaccine Clinics'),
]


class Participant(models.Model):
    # demographics
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='Andhra Pradesh')
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phone = PhoneNumberField(max_length=20, unique=True, blank=False,
                             help_text='OTP verification will be required to create postings. Format: +919999999999')
    lastPhoneUpdate = models.DateTimeField(default=timezone.now, blank=False)
    instagramHandle = models.URLField(max_length=200, blank=True, help_text="Valid URL expected.")
    facebookHandle = models.URLField(max_length=200, blank=True, help_text="Valid URL expected.")
    twitterHandle = models.URLField(max_length=200, blank=True, help_text="Valid URL expected.")
    website = models.URLField(max_length=200, blank=True, help_text="Valid URL expected.")

    num_scams = models.IntegerField(default=0, blank=False)
    num_helps = models.IntegerField(default=0, blank=False)
    spam_reports_given = models.IntegerField(default=0, blank=False)  # refers to caller spams
    spam_reports_received = models.IntegerField(default=0, blank=False) # refers to caller spams
    verifiedPhone = models.BooleanField(default=False)
    verifiedEmail = models.BooleanField(default=False)
    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential people who might be in need of the services.')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.state.upper()}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_supplier'),
            models.Index(fields=['phone'], name='phone_supplier'),
        ]


class Spammer(models.Model):
    reporter = models.ForeignKey(Participant, on_delete=models.CASCADE)
    phone = PhoneNumberField(max_length=20, unique=False, blank=False, help_text="The spam report will not be registered if you have already filed a report for the same contact before.")
    reason = models.CharField(blank=False, max_length=500,
                              help_text="Please explain the reason for marking this number as spam.")
    date_reported = models.DateField(auto_now=True)
    consent = models.BooleanField(blank=False, default=False, help_text="I confirm that the information entered by me is correct and not trying to mislead other members on this platform in any manner.")

    class Meta:
        unique_together = ['reporter', 'phone']
        ordering = ('-date_reported',)


class Service(models.Model):
    provider = models.ForeignKey(Participant, on_delete=models.CASCADE)
    name = models.CharField(default='Oxygen', choices=SERVICE_CHOICES, max_length=70)
    price = models.CharField(default='PAID', choices=PAYMENT_CHOICES, max_length=10,
                             help_text="Is the resource paid or available for free?")
    delivery = models.BooleanField(default=False, help_text='Do you deliver?')
    delivery_type = models.CharField(default='PAID', choices=PAYMENT_CHOICES, max_length=10, blank=True,
                                     help_text="Is your delivery paid or free?")
    delivery_details = models.CharField(blank=True, max_length=200,
                                        help_text='More information required for delivery (pricing, restrictions, etc.)')
    pricing_details = models.CharField(blank=True, max_length=200, help_text="Example: xxx INR per oxygen cylinder.")
    additional_details = models.CharField(max_length=5000, blank=True,
                                          help_text="Any additional details or restrictions about the availability of your service.")
    consent = models.BooleanField(default=False,
                                  help_text="I acknowledge that the details entered by me are correct. In case of spam reports against this posting, I am bound to being banned from this platform.",
                                  blank=False)
    created = models.DateField(auto_now=True)
    scam_votes = models.ManyToManyField(Participant, related_name='scam_votes_participants', blank=True)
    help_votes = models.ManyToManyField(Participant, related_name='help_votes_participants', blank=True)

    def __str__(self):
        return self.name
