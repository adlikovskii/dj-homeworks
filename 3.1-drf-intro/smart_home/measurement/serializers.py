from rest_framework import serializers

# TODO: опишите необходимые сериализаторы
from .models import Sensor, Measurement


class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'temperature', 'created_at']


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementsSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        depth = 1
        fields = ['id', 'name', 'description', 'measurements']
