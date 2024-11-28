from django.urls import path
from .views import HomepageView, ReauthenticateDevice, ReceiveData, AboutView


urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('about/', AboutView.as_view(), name='about'),
    path('reauthenticate/', ReauthenticateDevice.as_view(), name='reauthenticate-device'),
    path('streamdata/', ReceiveData.as_view(), name='receive-data'),
]