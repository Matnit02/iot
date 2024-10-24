from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Device(models.Model):
    location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Latitude of the device's location in decimal degrees. Must be between -90 and 90."
    )
    location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Longitude of the device's location in decimal degrees. Must be between -180 and 180."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Additional details or notes about the device."
    )
    active = models.BooleanField(
        default=True,
        help_text="Indicates whether the device is currently operational. Depending on last update time."
    )

    def __str__(self):
        return f"Device at {self.location_latitude}, {self.location_longitude}"


class SensorValues(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='sensors',
        help_text="The device that collected this sensor data."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the sensor data was recorded."
    )
    atmospheric_pressure = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(300), MaxValueValidator(1100)],
        help_text="Atmospheric pressure in hectopascals. Must be between 300 and 1100 hPa."
    )
    water_temperature = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-50), MaxValueValidator(100)],
        help_text="Water temperature in degrees Celsius. Must be between -50 and 100°C."
    )
    air_temperature = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(-50), MaxValueValidator(60)],
        help_text="Air temperature in degrees Celsius. Must be between -50 and 60°C."
    )
    pm1_0 = models.FloatField(
        null=True,
        blank=True,
        help_text="Particulate Matter 1.0 concentration in µg/m³."
    )
    pm2_5 = models.FloatField(
        null=True,
        blank=True,
        help_text="Particulate Matter 2.5 concentration in µg/m³."
    )
    pm10 = models.FloatField(
        null=True,
        blank=True,
        help_text="Particulate Matter 10 concentration in µg/m³."
    )
    noise_level = models.FloatField(
        null=True,
        blank=True,
        help_text="Noise level measured in decibels."
    )
    light_intensity = models.FloatField(
        null=True,
        blank=True,
        help_text="Light intensity in lux, which measures brightness."
    )
    weather_condition = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Weather condition calculated on the device, e.g., 'Sunny', 'Cloudy'."
    )

    def __str__(self):
        return (f"Sensor data for device at {self.device.location_latitude}, "
                f"{self.device.location_longitude} on {self.timestamp}")
