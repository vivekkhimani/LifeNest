# Generated by Django 3.2.3 on 2021-05-26 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0028_alter_spammer_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spammer',
            options={'ordering': ('-date_reported',)},
        ),
    ]