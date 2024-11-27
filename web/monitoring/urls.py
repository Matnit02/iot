from django.urls import path
from .views import HomepageView, ReauthenticateDevice, ReceiveData


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('reauthenticate/', ReauthenticateDevice.as_view(), name='reauthenticate-device'),
    path('streamdata/', ReceiveData.as_view(), name='receive-data'),
]