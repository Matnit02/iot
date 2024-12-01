# Generated by Django 5.1.2 on 2024-11-28 11:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_remove_sensorvalues_weather_condition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensorvalues',
            name='noise_level',
        ),
        migrations.AddField(
            model_name='sensorvalues',
            name='humidity',
            field=models.FloatField(blank=True, help_text='Relative humidity as a percentage. Must be between 0 and 100%.', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]