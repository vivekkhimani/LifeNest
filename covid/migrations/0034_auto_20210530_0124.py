# Generated by Django 3.2.3 on 2021-05-30 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0033_alter_participant_lastphoneupdate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerifiedPhone',
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(choices=[('Oxygen', 'Oxygen'), ('Medications (no Remdesivir)', 'Medications (no Remdesivir)'), ('Remdesivir', 'Remdesivir'), ('Hospital Beds', 'Hospital Beds'), ('Ventilator Beds', 'Ventilator Beds'), ('Home-made Food', 'Home-made Food'), ('Ambulance', 'Ambulance'), ('Monetary Donations', 'Monetary Donations'), ('Plasma Donations', 'Plasma Donations'), ('Laboratory Testing', 'Laboratory Testing'), ('Vaccine Clinics', 'Vaccine Clinics')], default='Oxygen', max_length=70),
        ),
    ]