# Generated by Django 3.2.3 on 2021-05-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0003_auto_20210522_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.participant'),
        ),
    ]
