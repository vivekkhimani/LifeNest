# Generated by Django 3.2.3 on 2021-05-24 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0015_auto_20210524_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='num_scams',
            field=models.IntegerField(default=0),
        ),
    ]
