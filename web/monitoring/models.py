import secrets
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Device(models.Model):
    encryption_key = models.CharField(
        max_length=255,
        help_text="Encryption key used for API key encryption when needed."
    )

    api_key = models.CharField(
        max_length=255,
        unique=True,
        help_text="Primary API key for authorization of data send by device."
    )

    api_key_active = models.BooleanField(
        default=True,
        help_text="Indicates if the API key is currently active and valid."
    )

    temporary_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="A temporary API key field used when moving from old key to new one."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this device was created."
    )

    def __str__(self):
        return f"Device {self.api_key}"

    @classmethod
    def get_device_by_api_key(cls, api_key):
        """
        Retrieves a Device instance by api_key or temporary_api_key.

        Params:
            api_key (str): The API key to search for.

        Returns:
            tuple: A tuple containing the Device instance (or None if not found) and a boolean
                   indicating whether the main API key was used.
        """
        try:
            device = cls.objects.get(api_key=api_key)
            return device, True
        except cls.DoesNotExist:
            try:
                device = cls.objects.get(temporary_api_key=api_key)
                return device, False
            except cls.DoesNotExist:
                return None, False

    def key_deactivate(self):
        """Deactivates the API key by setting api_key_active to False."""
        self.api_key_active = False
        self.save()

    def key_reactivate(self):
        """Activates the API key by setting `api_key_active` to True and clearing the `api_key` field."""
        self.api_key_active = True
        self.api_key = None
        self.save()

    def is_api_key_active(self):
        """Returns True if the API key is active, False otherwise."""
        return self.api_key_active

    def generate_new_api_key(self):
        """Generates a unique, secure API key for the Device model."""
        while True:
            new_key = secrets.token_urlsafe(255)
            if not Device.objects.filter(api_key=new_key).exists():
                self.temporary_api_key = self.api_key
                self.api_key = new_key
                self.save()
                break

    def encode_message(self, message):
        pass

    def decode_message(self, message):
        # Nie wiem w sumie czy to nam jest tu potrzebne,
        # ale skoro i tak będzie na device to możesz wrzucić tutaj na przyszłość.
        # Albo po prostu usunąć tą metodę
        pass

class DeviceSnapshot(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='snapshots',
        help_text="The device this snapshot is associated with."
    )
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
        help_text="Additional details or notes about the device snapshot."
    )
    active = models.BooleanField(
        default=True,
        help_text="Indicates whether the device is currently operational. Depending on last update time."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when this snapshot was created."
    )

    def __str__(self):
        return f"Device at {self.location_latitude}, {self.location_longitude}"


class SensorValues(models.Model):
    device_snapshot = models.ForeignKey(
        DeviceSnapshot,
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
