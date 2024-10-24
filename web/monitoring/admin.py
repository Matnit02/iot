from django.contrib import admin
from .models import Device, SensorValues


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_latitude', 'location_longitude', 'active', 'description', 'last_sensor_update')
    search_fields = ('id', 'location_latitude', 'location_longitude', 'description')
    list_filter = ('active',)
    fieldsets = (
        (None, {
            'fields': ('location_latitude', 'location_longitude', 'description')
        }),
        ('Status', {
            'fields': ('active',),
            'description': 'Control whether the device is currently active.',
        }),
    )

    def last_sensor_update(self, obj):
        last_sensor = obj.sensors.order_by('-timestamp').first()
        if last_sensor:
            return last_sensor.timestamp
        return "No sensor updates"

    last_sensor_update.short_description = 'Last Sensor Update'


@admin.register(SensorValues)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'timestamp', 'air_temperature', 'water_temperature', 'atmospheric_pressure',
                    'pm1_0', 'pm2_5', 'pm10', 'noise_level', 'light_intensity', 'weather_condition')
    search_fields = ('id', 'device', 'timestamp')
    list_filter = ('device', 'timestamp', 'air_temperature', 'water_temperature', 'atmospheric_pressure', 'pm1_0',
                   'pm2_5', 'pm10', 'noise_level', 'light_intensity', 'weather_condition')
    readonly_fields = ('timestamp',)
