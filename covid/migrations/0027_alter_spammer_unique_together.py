# Generated by Django 3.2.3 on 2021-05-26 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0026_auto_20210526_1235'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spammer',
            unique_together={('reporter', 'phone')},
        ),
    ]