# Generated by Django 3.0.2 on 2021-04-27 01:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=20)),
                ('lastName', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('created', models.DateTimeField(default=datetime.date(2021, 4, 26))),
                ('phone', models.CharField(max_length=20)),
                ('verifiedPhone', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('verifiedEmail', models.BooleanField(default=False)),
                ('instagramHandle', models.CharField(blank=True, max_length=20)),
                ('facebookHandle', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Oxygen', 'Oxygen'), ('Medications (no Remdesivir)', 'Medications (no Remdesivir)'), ('Remdesivir', 'Remdesivir'), ('Hospital Beds', 'Hospital Beds'), ('Ventilator Beds', 'Ventilator Beds'), ('Home-made Food', 'Home-made Food'), ('Ambulance', 'Ambulance'), ('Monetary Donations', 'Monetary Donations'), ('Plasma Donations', 'Plasma Donations'), ('Laboratory Testing', 'Laboratory Testing')], default='Oxygen', max_length=70)),
                ('created', models.DateTimeField(default=datetime.date(2021, 4, 26))),
                ('isFree', models.BooleanField(default=False)),
                ('isActive', models.BooleanField(default=True)),
                ('isDelivery', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Requestor',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isAmbulance',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isDonations',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isFoodDelivery',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isFoodOrdering',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isFree',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isHospitalBeds',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isLabTests',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isMedications',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isOxygen',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isPlasma',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isRemdevsir',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isTransportation',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='isVentilatorBeds',
        ),
        migrations.AddField(
            model_name='supplier',
            name='created',
            field=models.DateTimeField(default=datetime.date(2021, 4, 26)),
        ),
        migrations.AddField(
            model_name='requester',
            name='services',
            field=models.ManyToManyField(to='covid.Service'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='services',
            field=models.ManyToManyField(to='covid.Service'),
        ),
    ]
