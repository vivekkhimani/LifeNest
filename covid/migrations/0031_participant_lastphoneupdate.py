# Generated by Django 3.2.3 on 2021-05-29 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0030_alter_participant_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='lastPhoneUpdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
