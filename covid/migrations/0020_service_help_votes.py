# Generated by Django 3.2.3 on 2021-05-24 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0019_service_scam_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='help_votes',
            field=models.ManyToManyField(related_name='help_votes_participants', to='covid.Participant'),
        ),
    ]