# Generated by Django 3.2.3 on 2021-05-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0005_auto_20210522_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='pricing_details',
            field=models.CharField(blank=True, help_text='Example: xxx INR per oxygen cylinder.', max_length=200),
        ),
    ]
