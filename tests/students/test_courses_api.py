import pytest
from rest_framework.test import APIClient
from students.models import Student, Course
from model_bakery import baker

# def test_example():
#     assert False, "Just test example"

url = '/api/v1/courses/'

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client, courses_factory):
    n = 10
    courses = courses_factory(_quantity=n)
    # response = client.get(url)
    response = client.get(f'{url}+{courses[0].id}/')
    data = response.json()
    assert courses[0].name == data.get('name')
    assert response.status_code == 200
 
@pytest.mark.django_db
def test_get_list_course(client, courses_factory):
    n = 10
    courses = courses_factory(_quantity=n)
    response = client.get(url)
    data = response.json()
    assert len(data) == len(courses)
    assert response.status_code == 200

@pytest.mark.django_db
def test_fiter_id_course(client, courses_factory):
    n = 10
    courses = courses_factory(_quantity=n)
    for n, i in enumerate(courses):
        response = client.get(url, data = {id: i.id})
        data = response.json()
        assert i.id == data[n]['id']
        assert response.status_code == 200

@pytest.mark.django_db
def test_fiter_name_course(client, courses_factory):
    n = 10
    courses = courses_factory(_quantity=n)
    for n, i in enumerate(courses):
        response = client.get(url, data = {id: i.name})
        data = response.json()
        assert i.name == data[n]['name']
        assert response.status_code == 200
        
@pytest.mark.django_db
def test_post_course(client):
    response = client.post(url, data = {'name': 'course_name'}, format = 'json')
    assert response.status_code == 201 
    
@pytest.mark.django_db
def test_put_course(client, courses_factory):
      n = 10
      courses = courses_factory(_quantity=n)
      response = client.patch(f'{url}+{courses[0].id}/', data = {'name':'changed course'}, format = 'json')
      data = response.json()
      assert data['name'] == 'changed course'
      assert response.status_code == 200  

@pytest.mark.django_db
def test_delete_course(client, courses_factory):
      n = 10
      courses = courses_factory(_quantity=n)
      response = client.delete(f'{url}+{courses[0].id}/', data = {'name':'changed course'}, format = 'json')
      assert response.status_code == 204  