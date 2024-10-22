from django.urls import path
from .views import TempTableView, TempMapView


urlpatterns = [
    path('map/', TempMapView.as_view(), name='map'),
    path('table/', TempTableView.as_view(), name='table'),
]