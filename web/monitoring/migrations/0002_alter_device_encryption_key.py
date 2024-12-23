# Generated by Django 5.1.2 on 2024-11-27 15:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='encryption_key',
            field=models.CharField(help_text='Encryption key used for API key encryption when needed.', max_length=44, validators=[django.core.validators.MinLengthValidator(44)]),
        ),
    ]
