import json
from math import isclose
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .mixins import AuthenticateDevice, AnomalyDetectionMixin, GetReservoirsMixin
from .models import Device, DeviceSnapshot, SensorValues


class HomepageView(GetReservoirsMixin, TemplateView):
    template_name = 'homepage.html'


class AboutView(GetReservoirsMixin, TemplateView):
    template_name = 'about.html'


class ContactView(GetReservoirsMixin, TemplateView):
    template_name = 'contact.html'


@method_decorator(csrf_exempt, name='dispatch')
class ReauthenticateDevice(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        key = data.get('key')

        device, _ = Device.get_device_by_api_key(api_key=key)
        if device is None:
            return HttpResponse(status=403)
        elif device.is_api_key_active():
            return JsonResponse({'success': False, 'error': 'key_is_active'})

        if device.temporary_api_key is None:
            device.generate_new_api_key()

        encrypted_key = device.encrypt_message(device.api_key)
        return JsonResponse({'success': True, 'key': encrypted_key})


@method_decorator(csrf_exempt, name='dispatch')
class ReceiveData(AuthenticateDevice, AnomalyDetectionMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        device = request.device

        location_latitude = data.get("location_latitude")
        location_longitude = data.get("location_longitude")
        sensor_data = data.get("data", {})

        required_fields = ['atmospheric_pressure', 'water_temperature', 'air_temperature', 'pm1_0', 'pm2_5',
                           'pm10', 'humidity', 'light_intensity']
        missing_fields = [field for field in required_fields if field not in sensor_data or sensor_data[field] is None]

        if missing_fields:
            return JsonResponse({'success': False}, status=400)
        last_snapshot = device.snapshots.order_by('-created_at').first()

        if (last_snapshot is None or not isclose(last_snapshot.location_latitude, location_latitude, rel_tol=1e-9) or
                not isclose(last_snapshot.location_longitude, location_longitude, rel_tol=1e-9)):
            device_snapshot = DeviceSnapshot.objects.create(
                device=device,
                location_latitude=location_latitude,
                location_longitude=location_longitude,
                active=True
            )
        else:
            device_snapshot = last_snapshot

        SensorValues.objects.create(
            device_snapshot=device_snapshot,
            atmospheric_pressure=sensor_data.get("atmospheric_pressure"),
            water_temperature=sensor_data.get("water_temperature"),
            air_temperature=sensor_data.get("air_temperature"),
            pm1_0=sensor_data.get("pm1_0"),
            pm2_5=sensor_data.get("pm2_5"),
            pm10=sensor_data.get("pm10"),
            humidity=sensor_data.get("humidity"),
            light_intensity=sensor_data.get("light_intensity"),
        )

        return JsonResponse({'success': True})
