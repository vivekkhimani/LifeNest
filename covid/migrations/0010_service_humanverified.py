# Generated by Django 3.2.3 on 2021-05-22 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0009_service_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='humanVerified',
            field=models.BooleanField(default=False),
        ),
    ]
