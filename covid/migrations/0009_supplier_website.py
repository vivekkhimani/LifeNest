# Generated by Django 3.0.2 on 2021-04-30 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0008_auto_20210430_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='website',
            field=models.URLField(blank=True),
        ),
    ]
