from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from .filters import CourseFilter
from .models import Course
from .serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

    def perform_create(self, serializer):
        print(self, serializer)
        course = serializer.validated_data['students']
        if len(course) >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError
        return super().perform_create(serializer)
