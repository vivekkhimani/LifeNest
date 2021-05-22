# Generated by Django 3.2.3 on 2021-05-22 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0004_alter_service_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='delivery_details',
            field=models.CharField(blank=True, help_text='More information required for delivery (pricing, restrictions, etc.)', max_length=200),
        ),
        migrations.AddField(
            model_name='service',
            name='payment',
            field=models.CharField(choices=[('FREE', 'FREE'), ('PAID', 'PAID')], default='Paid', max_length=10),
        ),
        migrations.AddField(
            model_name='service',
            name='pricing_details',
            field=models.CharField(default='NA', help_text='Example: xxx INR per oxygen cylinder.', max_length=200),
        ),
    ]
