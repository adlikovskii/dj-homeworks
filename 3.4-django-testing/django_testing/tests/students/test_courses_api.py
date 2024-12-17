import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course
from django.test import override_settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    url = reverse('courses-list')
    courses = course_factory(_quantity=10)
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory(_quantity=1)
    expected_data = {
        'id': course[0].pk,
        'name': course[0].name,
        'students': []
    }

    url = reverse('courses-detail', args=[course[0].pk])
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert expected_data == data


@pytest.mark.django_db
def test_create_course(client):
    expected_json = {
        'name': 'math',
        'students': []
    }
    url = reverse('courses-list')
    response = client.post(url, data=expected_json)
    data = response.json()

    assert response.status_code == 201
    assert data.get('name') == Course.objects.get(id=data.get('id')).name


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    students = student_factory(_quantity=3)
    expected_json = {
        'id': course[0].pk,
        'name': 'math',
        'students': [student.pk for student in students]
    }
    url = reverse('courses-detail', args=[course[0].pk])
    response = client.put(url, data=expected_json)
    data = response.json()

    assert response.status_code == 200
    assert data == expected_json
    assert Student.objects.all()[0] in students


@pytest.mark.django_db
def test_partial_update_corse(client, course_factory):
    course = course_factory(_quantity=1)
    expected_json = {
        'name': 'math',
        'students': []
    }
    url = reverse('courses-detail', args=[course[0].pk])
    response = client.patch(url, data=expected_json)
    data = response.json()

    assert response.status_code == 200
    assert data.get('name') == expected_json.get('name')


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[course[0].pk])
    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.all().count() == 0


@pytest.mark.django_db
def test_filter_course(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')

    # filtering by name
    course_name = courses[0].name
    response_by_name = client.get(url, {'name': course_name})
    data_by_name = response_by_name.json()

    assert response_by_name.status_code == 200
    assert data_by_name[0]['name'] == course_name

    # filtering by id
    course_id = courses[1].id
    response_by_id = client.get(url, {'id': course_id})
    data_by_id = response_by_id.json()

    assert response_by_name.status_code == 200
    assert data_by_id[0]['id'] == course_id


@pytest.mark.django_db
@override_settings(MAX_STUDENTS_PER_COURSE=20)
def test_validate_students_per_course(client, course_factory, student_factory):
    url = reverse('courses-list')
    students = student_factory(_quantity=20)
    expected_json = {
        'name': 'math',
        'students': [student.pk for student in students]
    }

    response = client.post(url, data=expected_json)
    existence_course = Course.objects.last()

    assert response.status_code == 400
    assert existence_course is None

    students = student_factory(_quantity=19)
    expected_json = {
        'name': 'math',
        'students': [student.pk for student in students]
    }

    response = client.post(url, data=expected_json)

    assert response.status_code == 201
    assert Course.objects.last()
