# Generated by Django 3.0.2 on 2021-05-14 06:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0011_auto_20210514_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='phone',
            field=models.CharField(help_text='Verification required for sign up. Format: +91-9999999999', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in format +91-9999999999.', regex='^(\\+\\d{1,3})?-?\\s?\\d{8,13}')]),
        ),
    ]
