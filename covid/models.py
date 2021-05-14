from django.db import models

# Create your models here.
"""
models.py
"""
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, UserManager

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


class Supplier(models.Model):
    # demographics
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='Delhi')
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phoneRegex = RegexValidator(regex=r'^(\+\d{1,3})?-?\s?\d{8,13}',
                                message="Phone number must be entered in format +91-9999999999.")
    phone = models.CharField(max_length=20, unique=True, validators=[phoneRegex], blank=False, help_text='Verification required for sign up. Format: +91-9999999999')
    instagramHandle = models.URLField(max_length=200, blank=True)
    facebookHandle = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)

    verifiedPhone = models.BooleanField(default=False)
    humanVerified = models.BooleanField(default=False)
    verifiedEmail = models.BooleanField(default=False)
    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential people who might be in need of the services.')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.state.upper()}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_supplier'),
            models.Index(fields=['phone'], name='phone_supplier'),
        ]


class Requester(models.Model):
    # demographics
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='Delhi')
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phoneRegex = RegexValidator(regex=r'^(\+\d{1,3})?-?\s?\d{8,13}',
                                message="Phone number must be entered in format +91-9999999999.")
    phone = models.CharField(max_length=20, unique=True, validators=[phoneRegex], blank=False, help_text='Verification required for sign up. Format: +91-9999999999')
    instagramHandle = models.URLField(max_length=200, blank=True)
    facebookHandle = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)

    verifiedPhone = models.BooleanField(default=False)
    humanVerified = models.BooleanField(default=False)
    verifiedEmail = models.BooleanField(default=False)
    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential suppliers.')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.state.upper()}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_requester'),
            models.Index(fields=['phone'], name='phone_requester'),
        ]


class Volunteer(models.Model):
    # demographics
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='Delhi')
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phoneRegex = RegexValidator(regex=r'^(\+\d{1,3})?-?\s?\d{8,13}',
                                message="Phone number must be entered in format +91-9999999999.")
    phone = models.CharField(max_length=20, unique=True, validators=[phoneRegex], blank=False, help_text='Verification required for sign up. Format: +91-9999999999')
    instagramHandle = models.URLField(max_length=200, blank=True)
    facebookHandle = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)

    verifiedPhone = models.BooleanField(default=False)
    humanVerified = models.BooleanField(default=False)
    verifiedEmail = models.BooleanField(default=False)
    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential suppliers.')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.state.upper()}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_volunteer'),
            models.Index(fields=['phone'], name='phone_volunteer'),
        ]


class Service(models.Model):
    service_choices = [
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
    ]
    name = models.CharField(default='Oxygen', choices=service_choices, max_length=70)
    requester = models.ManyToManyField(Requester)
    supplier = models.ManyToManyField(Supplier)

    def __str__(self):
        return self.name
