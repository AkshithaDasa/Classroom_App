# Generated by Django 5.0.1 on 2024-02-01 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_of_birth',
            new_name='dob',
        ),
    ]
