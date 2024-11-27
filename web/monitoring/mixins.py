import json
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from .models import Device, DeviceSnapshot, SensorValues


class AuthenticateDevice:
    """
    Mixin to authenticate a device using an API key provided in the JSON body of a POST request.

    This mixin is designed to be used with Django class-based views to verify the presence
    and status of a `Device` API key. The mixin inspects the API key provided in the request
    body and attempts to find an active device that matches it. Based on the device's state,
    it determines whether to allow the request to proceed.

    Possible scenarios:
        - device not found: request is blocked with a 403 response.
        - device found using main key and is active: request proceeds.
        - device found using a new main key and is inactive: device reactivated and request proceeds.
        - device found using an old key and is inactive: returns inactive device response.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                api_key = data.get('api_key')
            except json.JSONDecodeError:
                return HttpResponse(status=400)

            if not api_key:
                return HttpResponse(status=403)

            device, main_key_used = Device.get_device_by_api_key(api_key=api_key)

            if device is None:
                return HttpResponse(status=403)

            if main_key_used:
                if device.is_api_key_active():
                    request.device = device
                else:
                    device.key_reactivate()
                    request.device = device

                return super().dispatch(request, *args, **kwargs)

            return JsonResponse({'success': False, 'error': 'device_deauthenticated'})

        return super().dispatch(request, *args, **kwargs)


class AnomalyDetectionMixin:
    """
     Mixin to detect and handle anomalies in device data traffic based on time and location thresholds.

    This mixin is designed to be used with Django class-based views and performs two main anomaly checks
    when handling POST requests from authenticated devices:

    1. Data Frequency Check:
        Ensures that at least a minimum interval (configured in settings) has passed since the last recorded
        data entry for the device. If the device sends data too frequently (i.e., within the configured
        interval), the device is deactivated and a response is returned indicating that the device has been deauthenticated.

    2. Location Change Limit Check:
        When a device’s latitude or longitude changes, the mixin verifies if the device has changed location more than
        a specified limit (configured in settings) within a configured time interval (also in settings). If the location
        change limit is exceeded, the device is deactivated and the server responds indicating deauthentication.

        If no `location_latitude` or `location_longitude` data is provided, the server responds with a 400 code.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            device = request.device

            last_sensor_data = SensorValues.objects.filter(device_snapshot__device=device).order_by('-timestamp').first()
            if last_sensor_data:
                min_interval = timedelta(minutes=settings.SENSOR_VALUES_MIN_INTERVAL_MINUTES)
                time_since_last_data = timezone.now() - last_sensor_data.timestamp
                if time_since_last_data < min_interval:
                    device.deactivate()
                    return JsonResponse({'success': False, 'error': 'device_deauthenticated'})

            data = request.json()
            new_latitude = data.get("location_latitude")
            new_longitude = data.get("location_longitude")

            if new_latitude is not None and new_longitude is not None:
                last_snapshot = DeviceSnapshot.objects.filter(device=device).order_by('-created_at').first()

                if last_snapshot and (last_snapshot.location_latitude != new_latitude or
                                      last_snapshot.location_longitude != new_longitude):
                    location_interval = timezone.now() - timedelta(hours=settings.LOCATION_CHANGE_INTERVAL_HOURS)
                    location_changes = DeviceSnapshot.objects.filter(device=device, created_at__gte=location_interval).count()

                    if location_changes >= settings.MAX_LOCATION_CHANGES:
                        device.deactivate()
                        return JsonResponse({'success': False, 'error': 'device_deauthenticated'})

                return super().dispatch(request, *args, **kwargs)

            return HttpResponse(status=400)

        return super().dispatch(request, *args, **kwargs)
