from django.db import models

# Create your models here.
"""
models.py
"""
from django.db import models
from django.core.validators import RegexValidator


class Supplier(models.Model):
    # demographics
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phoneRegex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in format +919999999999.")
    phone = models.CharField(max_length=20, unique=True, validators=[phoneRegex])
    verifiedPhone = models.BooleanField(default=False)
    humanVerified = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    verifiedEmail = models.BooleanField(default=False)
    instagramHandle = models.URLField(max_length=200, blank=True)
    facebookHandle = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)

    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential people who might be in need of the services.')

    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.state.upper()}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_supplier'),
            models.Index(fields=['firstName'], name='first_name_supplier'),
            models.Index(fields=['lastName'], name='last_name_supplier'),
            models.Index(fields=['phone'], name='phone_supplier'),
            models.Index(fields=['email'], name='email_supplier'),
        ]
        index_together = [
            ["firstName", "lastName"]
        ]


class Requester(models.Model):
    # demographics
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    # contacts
    phone = models.CharField(max_length=20, unique=True)
    verifiedPhone = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, blank=True, unique=True)
    verifiedEmail = models.BooleanField(default=False)
    instagramHandle = models.URLField(max_length=200, blank=True)
    facebookHandle = models.URLField(max_length=200, blank=True)

    consent = models.BooleanField(blank=False, default=False,
                                  help_text='I agree to provide the following data to the potential suppliers.')

    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.state.upper()}"

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['state'], name='state_requester'),
            models.Index(fields=['firstName'], name='first_name_requester'),
            models.Index(fields=['lastName'], name='last_name_requester'),
            models.Index(fields=['phone'], name='phone_requester'),
            models.Index(fields=['email'], name='email_requester'),
        ]
        index_together = [
            ["firstName", "lastName"]
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
