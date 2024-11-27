import json
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from .mixins import AuthenticateDevice, AnomalyDetectionMixin
from .models import Device, DeviceSnapshot, SensorValues


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snapshots = DeviceSnapshot.objects.all()
        reservoirs = []

        for snapshot in snapshots:
            latest_sensor = snapshot.sensors.order_by('-timestamp').first()
            if latest_sensor:
                reservoirs.append({
                    "id": snapshot.id,
                    "name": snapshot.name,
                    "coordinates": [float(snapshot.location_latitude), float(snapshot.location_longitude)],
                    "air_temperature": latest_sensor.air_temperature,
                    "water_temperature": latest_sensor.water_temperature,
                    "pressure": latest_sensor.atmospheric_pressure,
                    "noise_level": latest_sensor.noise_level,
                })

        context['reservoirs'] = reservoirs
        context['reservoirs_json'] = json.dumps(reservoirs)
        return context


class ReauthenticateDevice(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        key = data.get('key')

        device = Device(key=key)
        if device is None:
            return HttpResponse(status=403)
        elif device.is_api_key_active():
            return JsonResponse({'success': False, 'error': 'key_is_active'})

        if device.temporary_api_key is None:
            device.generate_new_api_key()

        encrypted_key = device.encode_message(device.api_key)
        return JsonResponse({'success': False, 'key': encrypted_key})


class ReceiveData(AuthenticateDevice, AnomalyDetectionMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        device = request.device

        location_latitude = data.get("location_latitude")
        location_longitude = data.get("location_longitude")
        sensor_data = data.get("data", {})
        last_snapshot = device.snapshots.order_by('-created_at').first()

        if (last_snapshot is None or last_snapshot.location_latitude != location_latitude or
                last_snapshot.location_longitude != location_longitude):
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
            noise_level=sensor_data.get("noise_level"),
            light_intensity=sensor_data.get("light_intensity"),
            weather_condition=sensor_data.get("weather_condition"),
        )

        return JsonResponse({'success': True})
