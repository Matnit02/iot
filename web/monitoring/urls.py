from django.urls import path
from .views import TempTableView, TempMapView, ReauthenticateDevice, ReceiveData


urlpatterns = [
    path('map/', TempMapView.as_view(), name='map'),
    path('table/', TempTableView.as_view(), name='table'),
    path('reauthenticate/', ReauthenticateDevice.as_view(), name='reauthenticate-device'),
    path('streamdata/', ReceiveData.as_view(), name='receive-data'),
]