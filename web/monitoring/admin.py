from django.contrib import admin
from .models import Device, DeviceSnapshot, SensorValues


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'encryption_key', 'api_key', 'api_key_active', 'temporary_api_key', 'created_at')
    search_fields = ('id', 'encryption_key', 'api_key', 'api_key_active', 'temporary_api_key', 'created_at')


@admin.register(DeviceSnapshot)
class DeviceSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'location_latitude', 'location_longitude', 'active', 'description', 'last_sensor_update',
                    'created_at')
    search_fields = ('id', 'location_latitude', 'location_longitude', 'description', 'created_at')
    list_filter = ('active',)
    readonly_fields = ('created_at',)

    def last_sensor_update(self, obj):
        last_sensor = obj.sensors.order_by('-timestamp').first()
        if last_sensor:
            return last_sensor.timestamp
        return "No sensor updates"

    last_sensor_update.short_description = 'Last Sensor Update'


@admin.register(SensorValues)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_snapshot', 'timestamp', 'air_temperature', 'water_temperature', 'atmospheric_pressure',
                    'pm1_0', 'pm2_5', 'pm10', 'noise_level', 'light_intensity', 'weather_condition')
    search_fields = ('id', 'timestamp')
    list_filter =   ('timestamp', 'air_temperature', 'water_temperature', 'atmospheric_pressure', 'pm1_0',
                     'pm2_5', 'pm10', 'noise_level', 'light_intensity', 'weather_condition')
