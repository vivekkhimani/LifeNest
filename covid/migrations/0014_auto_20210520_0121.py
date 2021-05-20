# Generated by Django 3.2 on 2021-05-20 06:21

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0013_auto_20210514_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requester',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='requester',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='OTP verification will be required as next step. Format: +919999999999', max_length=20, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='OTP verification will be required as next step. Format: +919999999999', max_length=20, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='verifiedphone',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='verifiedphone',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='OTP verification will be required as next step. Format: +919999999999', max_length=20, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='OTP verification will be required as next step. Format: +919999999999', max_length=20, region=None, unique=True),
        ),
    ]
