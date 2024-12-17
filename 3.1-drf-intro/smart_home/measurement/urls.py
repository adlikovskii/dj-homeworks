from django.urls import path

from .views import SensorsView, SensorDetailView, MeasurementsView


urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensor/<pk>/', SensorDetailView.as_view()),
    path('measurements/', MeasurementsView.as_view()),
]
