# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import SensorDetailSerializer, SensorSerializer, MeasurementsSerializer
from .models import Sensor, Measurement


class MeasurementsView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer

    def post(self, request):
        if request.data:
            Measurement.objects.create(**request.data)
            return Response({'Status': 'Done'})


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        if request.data:
            Sensor.objects.create(**request.data)
            return Response({'status': 'OK'})


class SensorDetailView(RetrieveAPIView):
    queryset = Sensor.objects.all().prefetch_related('measurements')
    serializer_class = SensorDetailSerializer

    def patch(self, request, pk):
        if request.data:
            obj_id = pk
            Sensor.objects.filter(id=obj_id).update(description=request.data.get("description"))
            return Response({'status': 'OK'})
