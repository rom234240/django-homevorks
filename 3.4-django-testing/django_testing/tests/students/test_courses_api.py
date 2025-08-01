import pytest
from rest_framework import status
from students.models import Course, Student

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def course_factory():
    from model_bakery.recipe import Recipe
    return Recipe(Course)

@pytest.fixture
def student_factory():
    from model_bakery.recipe import Recipe
    return Recipe(Student)

# Тесты
@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса"""
    course = course_factory.make()
    url = f"/api/v1/courses/{course.id}/"
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов"""
    courses = course_factory.make(_quantity=3)
    url = "/api/v1/courses/"
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """Фильтрация курсов по ID"""
    courses = course_factory.make(_quantity=5)
    target_id = courses[2].id
    url = f"/api/v1/courses/?id={target_id}"
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """Фильтрация курсов по имени"""
    courses = course_factory.make(_quantity=3)
    target_name = courses[1].name
    url = f"/api/v1/courses/?name={target_name}"
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == target_name

@pytest.mark.django_db
def test_create_course(api_client):
    """Создание курса"""
    url = "/api/v1/courses/"
    data = {'name': 'New Course'}
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'New Course'

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Обновление курса"""
    course = course_factory.make()
    url = f"/api/v1/courses/{course.id}/"
    data = {'name': 'Updated Course'}
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Updated Course'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Удаление курса"""
    course = course_factory.make()
    url = f"/api/v1/courses/{course.id}/"
    
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0