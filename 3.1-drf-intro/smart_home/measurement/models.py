from django.db import models


# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(to=Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
