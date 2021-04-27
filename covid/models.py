from django.db import models

# Create your models here.
"""
models.py
"""
from django.db import models
from datetime import date


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
    created = models.DateTimeField(default=date.today())
    isFree = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    isDelivery = models.BooleanField(default=False)


class Supplier(models.Model):
    # demographics
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created = models.DateTimeField(default=date.today())

    # contacts
    phone = models.CharField(max_length=20)
    verifiedPhone = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, blank=True)
    verifiedEmail = models.BooleanField(default=False)
    instagramHandle = models.CharField(max_length=20, blank=True)
    facebookHandle = models.CharField(max_length=20, blank=True)

    # services
    services = models.ManyToManyField(Service)


class Requester(models.Model):
    # demographics
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created = models.DateTimeField(default=date.today())

    # contacts
    phone = models.CharField(max_length=20)
    verifiedPhone = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, blank=True)
    verifiedEmail = models.BooleanField(default=False)
    instagramHandle = models.CharField(max_length=20, blank=True)
    facebookHandle = models.CharField(max_length=20, blank=True)

    # services
    services = models.ManyToManyField(Service)
